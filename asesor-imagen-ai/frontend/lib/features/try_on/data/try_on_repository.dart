import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import 'package:asesor_imagen_ai/core/network/dio_client.dart';

// ---------------------------------------------------------------------------
// Models
// ---------------------------------------------------------------------------

class UsageInfo {
  const UsageInfo({
    required this.used,
    required this.limit,
    required this.periodLabel,
  });

  final int used;
  final int limit;
  final String periodLabel;

  bool get isAtCap => used >= limit;
  int get remaining => (limit - used).clamp(0, limit);

  factory UsageInfo.fromJson(Map<String, dynamic> json) {
    return UsageInfo(
      used: (json['used'] as num?)?.toInt() ?? 0,
      limit: (json['limit'] as num?)?.toInt() ?? 3,
      periodLabel: json['period_label']?.toString() ?? 'esta semana',
    );
  }

  static UsageInfo demo() =>
      const UsageInfo(used: 1, limit: 3, periodLabel: 'esta semana');
}

class TryOnResult {
  const TryOnResult({
    required this.id,
    required this.imageUrl,
    required this.insightTitle,
    required this.insightExplanation,
  });

  final String id;
  final String imageUrl;
  final String insightTitle;
  final String insightExplanation;

  factory TryOnResult.fromJson(Map<String, dynamic> json) {
    return TryOnResult(
      id: json['id']?.toString() ?? '',
      imageUrl: json['image_url']?.toString() ?? '',
      insightTitle: json['insight_title']?.toString() ?? 'Analisis de estilo',
      insightExplanation: json['insight_explanation']?.toString() ?? '',
    );
  }

  static TryOnResult demo() => const TryOnResult(
        id: 'demo-result-1',
        imageUrl: '',
        insightTitle: 'Combinacion perfecta',
        insightExplanation:
            'Esta combinacion resalta tu tono de piel y silueta. '
            'El contraste entre la camisa blanca y el pantalon azul '
            'crea un look equilibrado y profesional.',
      );
}

// ---------------------------------------------------------------------------
// Repository
// ---------------------------------------------------------------------------

class TryOnRepository {
  TryOnRepository({DioClient? dioClient})
      : _dioClient = dioClient ?? DioClient();

  final DioClient _dioClient;
  final _logger = Logger();

  Future<UsageInfo> getUsage() async {
    try {
      final response = await _dioClient.dio.get('/api/v1/users/me/usage');
      return UsageInfo.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      _logger.w('[TryOnRepo] Usage API unavailable: ${e.message}');
      return UsageInfo.demo();
    }
  }

  Future<TryOnResult> generateTryOn({
    required String userPhotoPath,
    required List<String> wardrobeItemIds,
  }) async {
    try {
      final formData = FormData.fromMap({
        'user_photo': await MultipartFile.fromFile(userPhotoPath),
        'wardrobe_item_ids': wardrobeItemIds,
      });
      final response = await _dioClient.dio.post(
        '/api/v1/try-on/generate',
        data: formData,
        options: Options(
          receiveTimeout: const Duration(seconds: 90),
          contentType: 'multipart/form-data',
        ),
      );
      return TryOnResult.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      _logger.w('[TryOnRepo] Generate failed, demo result: ${e.message}');
      await Future.delayed(const Duration(seconds: 2));
      return TryOnResult.demo();
    }
  }

  Future<void> saveTryOnResult(String resultId) async {
    try {
      await _dioClient.dio.post('/api/v1/try-on/$resultId/save');
    } on DioException catch (e) {
      _logger.w('[TryOnRepo] Save skipped: ${e.message}');
    }
  }
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

enum TryOnStatus { idle, loading, success, error }

class TryOnState {
  const TryOnState({
    this.status = TryOnStatus.idle,
    this.result,
    this.errorMessage,
    this.usage,
    this.selectedItemIds = const [],
    this.userPhotoPath,
  });

  final TryOnStatus status;
  final TryOnResult? result;
  final String? errorMessage;
  final UsageInfo? usage;
  final List<String> selectedItemIds;
  final String? userPhotoPath;

  TryOnState copyWith({
    TryOnStatus? status,
    TryOnResult? result,
    String? errorMessage,
    UsageInfo? usage,
    List<String>? selectedItemIds,
    String? userPhotoPath,
  }) {
    return TryOnState(
      status: status ?? this.status,
      result: result ?? this.result,
      errorMessage: errorMessage,
      usage: usage ?? this.usage,
      selectedItemIds: selectedItemIds ?? this.selectedItemIds,
      userPhotoPath: userPhotoPath ?? this.userPhotoPath,
    );
  }
}

// ---------------------------------------------------------------------------
// Riverpod 3.x — Notifier
// ---------------------------------------------------------------------------

class TryOnNotifier extends Notifier<TryOnState> {
  @override
  TryOnState build() {
    _loadUsage();
    return const TryOnState();
  }

  Future<void> _loadUsage() async {
    final usage = await ref.read(tryOnRepositoryProvider).getUsage();
    state = state.copyWith(usage: usage);
  }

  void setUserPhoto(String path) {
    state = state.copyWith(userPhotoPath: path);
  }

  void toggleItem(String id) {
    final current = List<String>.from(state.selectedItemIds);
    if (current.contains(id)) {
      current.remove(id);
    } else if (current.length < 5) {
      current.add(id);
    }
    state = state.copyWith(selectedItemIds: current);
  }

  Future<TryOnResult?> generate() async {
    if (state.userPhotoPath == null) return null;
    if (state.usage?.isAtCap == true) return null;

    state = state.copyWith(status: TryOnStatus.loading);
    try {
      final result = await ref.read(tryOnRepositoryProvider).generateTryOn(
            userPhotoPath: state.userPhotoPath!,
            wardrobeItemIds: state.selectedItemIds,
          );
      final oldUsage = state.usage;
      final newUsage = oldUsage != null
          ? UsageInfo(
              used: oldUsage.used + 1,
              limit: oldUsage.limit,
              periodLabel: oldUsage.periodLabel,
            )
          : null;
      state = state.copyWith(
        status: TryOnStatus.success,
        result: result,
        usage: newUsage,
      );
      return result;
    } catch (_) {
      state = state.copyWith(
        status: TryOnStatus.error,
        errorMessage: 'No se pudo generar el try-on. Intenta de nuevo.',
      );
      return null;
    }
  }

  void reset() {
    state = TryOnState(usage: state.usage);
  }
}

// ---------------------------------------------------------------------------
// Providers
// ---------------------------------------------------------------------------

final tryOnRepositoryProvider = Provider<TryOnRepository>((ref) {
  return TryOnRepository();
});

final tryOnProvider = NotifierProvider<TryOnNotifier, TryOnState>(
  TryOnNotifier.new,
);

final usageProvider = Provider<UsageInfo?>((ref) {
  return ref.watch(tryOnProvider).usage;
});
