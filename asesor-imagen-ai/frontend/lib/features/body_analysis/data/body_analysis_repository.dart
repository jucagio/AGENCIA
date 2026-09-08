import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import 'package:asesor_imagen_ai/core/network/dio_client.dart';

// ---------------------------------------------------------------------------
// Model
// ---------------------------------------------------------------------------

class BodyAnalysisResult {
  const BodyAnalysisResult({
    required this.skinTone,
    required this.bodyShape,
    required this.colorPalette,
    required this.recommendations,
  });

  final String skinTone;
  final String bodyShape;
  final List<String> colorPalette;
  final List<String> recommendations;

  factory BodyAnalysisResult.fromJson(Map<String, dynamic> json) {
    return BodyAnalysisResult(
      skinTone: json['skin_tone']?.toString() ?? '',
      bodyShape: json['body_shape']?.toString() ?? '',
      colorPalette: (json['color_palette'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      recommendations: (json['recommendations'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }

  static BodyAnalysisResult demo() => const BodyAnalysisResult(
        skinTone: 'Tono calido — Oliva claro',
        bodyShape: 'Triangulo invertido — hombros mas anchos que caderas',
        colorPalette: ['#D4A574', '#8B6914', '#2D5A27', '#1A3A5C', '#8B2252'],
        recommendations: [
          'Opta por pantalones de pierna ancha para equilibrar proporciones',
          'Los colores tierra realzan tu tono de piel naturalmente',
          'Evita los hombros con relleno — ya tienes estructura natural',
          'El azul marino es tu color neutro ideal',
          'Las telas fluidas te favorecen mas que las rigidas',
        ],
      );
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

enum BodyAnalysisStatus { idle, loading, success, error }

class BodyAnalysisState {
  const BodyAnalysisState({
    this.status = BodyAnalysisStatus.idle,
    this.result,
    this.errorMessage,
    this.photoPath,
  });

  final BodyAnalysisStatus status;
  final BodyAnalysisResult? result;
  final String? errorMessage;
  final String? photoPath;

  BodyAnalysisState copyWith({
    BodyAnalysisStatus? status,
    BodyAnalysisResult? result,
    String? errorMessage,
    String? photoPath,
  }) {
    return BodyAnalysisState(
      status: status ?? this.status,
      result: result ?? this.result,
      errorMessage: errorMessage,
      photoPath: photoPath ?? this.photoPath,
    );
  }
}

// ---------------------------------------------------------------------------
// Repository
// ---------------------------------------------------------------------------

class BodyAnalysisRepository {
  BodyAnalysisRepository({DioClient? dioClient})
      : _dioClient = dioClient ?? DioClient();

  final DioClient _dioClient;
  final _logger = Logger();

  Future<BodyAnalysisResult> analyze(String photoPath) async {
    try {
      final formData = FormData.fromMap({
        'photo': await MultipartFile.fromFile(photoPath),
      });
      final response = await _dioClient.dio.post(
        '/api/v1/body-analysis',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
          receiveTimeout: const Duration(seconds: 60),
        ),
      );
      return BodyAnalysisResult.fromJson(
          response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      _logger.w('[BodyAnalysis] API unavailable, demo result: ${e.message}');
      await Future.delayed(const Duration(seconds: 2));
      return BodyAnalysisResult.demo();
    }
  }
}

// ---------------------------------------------------------------------------
// Riverpod 3.x — Notifier
// ---------------------------------------------------------------------------

class BodyAnalysisNotifier extends Notifier<BodyAnalysisState> {
  @override
  BodyAnalysisState build() => const BodyAnalysisState();

  void setPhoto(String path) {
    state = state.copyWith(photoPath: path);
  }

  Future<void> analyze() async {
    if (state.photoPath == null) return;
    state = state.copyWith(status: BodyAnalysisStatus.loading);
    try {
      final result =
          await ref.read(bodyAnalysisRepositoryProvider).analyze(state.photoPath!);
      state = state.copyWith(status: BodyAnalysisStatus.success, result: result);
    } catch (_) {
      state = state.copyWith(
        status: BodyAnalysisStatus.error,
        errorMessage: 'Error al analizar. Intenta de nuevo.',
      );
    }
  }

  void reset() {
    state = const BodyAnalysisState();
  }
}

// ---------------------------------------------------------------------------
// Providers
// ---------------------------------------------------------------------------

final bodyAnalysisRepositoryProvider =
    Provider<BodyAnalysisRepository>((ref) => BodyAnalysisRepository());

final bodyAnalysisProvider =
    NotifierProvider<BodyAnalysisNotifier, BodyAnalysisState>(
  BodyAnalysisNotifier.new,
);
