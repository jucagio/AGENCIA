/// Constantes globales de la app — Teclado de Señas
library;

class AppConstants {
  AppConstants._();

  // ---------------------------------------------------------------------------
  // API
  // ---------------------------------------------------------------------------

  /// URL base del backend de Sasha (FastAPI).
  /// Cambiar a la URL de producción antes de release.
  static const String apiBaseUrl = 'http://localhost:8000/api/v1';

  /// Timeout de las peticiones HTTP (segundos)
  static const int connectTimeoutSec = 15;
  static const int receiveTimeoutSec = 30;

  // ---------------------------------------------------------------------------
  // Auth
  // ---------------------------------------------------------------------------

  /// Keys de flutter_secure_storage
  static const String kAccessToken = 'access_token';
  static const String kRefreshToken = 'refresh_token';

  // ---------------------------------------------------------------------------
  // Paginación
  // ---------------------------------------------------------------------------

  static const int defaultPageSize = 20;
  static const int maxPageSize = 50;

  // ---------------------------------------------------------------------------
  // Sign language
  // ---------------------------------------------------------------------------

  static const String defaultLanguageCode = 'co-csn';

  static const Map<String, String> difficultyLabels = {
    'beginner': 'Básico',
    'intermediate': 'Intermedio',
    'advanced': 'Avanzado',
  };

  static const Map<String, int> difficultyLevel = {
    'beginner': 1,
    'intermediate': 3,
    'advanced': 5,
  };

  // ---------------------------------------------------------------------------
  // UI
  // ---------------------------------------------------------------------------

  /// Mínimo de chars para lanzar búsqueda automática
  static const int searchMinLength = 1;

  /// Debounce de búsqueda en milisegundos
  static const int searchDebounceMsec = 400;

  /// Duración de snackbars (ms)
  static const int snackbarDurationMsec = 3500;
}
