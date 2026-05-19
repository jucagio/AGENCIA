import 'package:dio/dio.dart';
import 'package:logger/logger.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import 'package:asesor_imagen_ai/core/constants/api_constants.dart';
import 'package:asesor_imagen_ai/core/config/env.dart';
import 'package:asesor_imagen_ai/core/errors/api_exception.dart';

/// Cliente HTTP centralizado basado en Dio.
/// Incluye:
///  - Interceptor de autenticación (JWT desde Supabase session)
///  - Interceptor de logging (solo en debug)
///  - Manejo uniforme de errores → [ApiException]
///
/// TODO(Sasha): Confirmar si el backend espera 'Bearer' o un header custom.
class DioClient {
  DioClient({Logger? logger}) : _logger = logger ?? Logger() {
    _dio = Dio(
      BaseOptions(
        baseUrl: Env.apiBaseUrl,
        connectTimeout: ApiConstants.connectTimeout,
        receiveTimeout: ApiConstants.receiveTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    )
      ..interceptors.add(_authInterceptor())
      ..interceptors.add(_loggingInterceptor());
  }

  late final Dio _dio;
  final Logger _logger;

  Dio get dio => _dio;

  // ---------------------------------------------------------------------------
  // Interceptors
  // ---------------------------------------------------------------------------

  Interceptor _authInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) {
        final session = Supabase.instance.client.auth.currentSession;
        if (session != null) {
          options.headers['Authorization'] = 'Bearer ${session.accessToken}';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        // 401 → intentar refrescar sesión una vez
        if (error.response?.statusCode == 401) {
          try {
            await Supabase.instance.client.auth.refreshSession();
            final session = Supabase.instance.client.auth.currentSession;
            if (session != null) {
              error.requestOptions.headers['Authorization'] =
                  'Bearer ${session.accessToken}';
              final retryResponse = await _dio.fetch(error.requestOptions);
              return handler.resolve(retryResponse);
            }
          } catch (_) {
            // Refresh falló → dejar que el error propague
          }
        }
        handler.next(error);
      },
    );
  }

  Interceptor _loggingInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) {
        _logger.d('[DioClient] → ${options.method} ${options.path}');
        handler.next(options);
      },
      onResponse: (response, handler) {
        _logger.d(
          '[DioClient] ← ${response.statusCode} ${response.requestOptions.path}',
        );
        handler.next(response);
      },
      onError: (error, handler) {
        _logger.e(
          '[DioClient] ERROR ${error.response?.statusCode} ${error.requestOptions.path}',
          error: error,
        );
        handler.next(error);
      },
    );
  }

  // ---------------------------------------------------------------------------
  // Error mapping
  // ---------------------------------------------------------------------------

  static ApiException mapDioError(DioException error) {
    return switch (error.type) {
      DioExceptionType.connectionTimeout ||
      DioExceptionType.sendTimeout ||
      DioExceptionType.receiveTimeout =>
        const ApiException(message: 'Tiempo de espera agotado. Verifica tu conexión.'),
      DioExceptionType.connectionError =>
        const ApiException(message: 'Sin conexión a internet.'),
      DioExceptionType.badResponse => ApiException(
          message: _parseMessage(error.response),
          statusCode: error.response?.statusCode,
          errors: _parseErrors(error.response),
        ),
      _ => ApiException(message: error.message ?? 'Error inesperado'),
    };
  }

  static String _parseMessage(Response<dynamic>? response) {
    try {
      final data = response?.data as Map<String, dynamic>?;
      return (data?['message'] as String?) ?? 'Error del servidor';
    } catch (_) {
      return 'Error del servidor';
    }
  }

  static Map<String, List<String>>? _parseErrors(Response<dynamic>? response) {
    try {
      final data = response?.data as Map<String, dynamic>?;
      final errors = data?['errors'] as Map<String, dynamic>?;
      return errors?.map(
        (key, value) => MapEntry(
          key,
          (value as List).map((e) => e.toString()).toList(),
        ),
      );
    } catch (_) {
      return null;
    }
  }
}
