// TODO(Sasha): Actualizar rutas cuando estén disponibles en el contrato de API.
// Ref: asesor-imagen-ai/backend — FastAPI router definitions.

/// Rutas de la API REST del backend.
/// Todas las rutas son relativas a [Env.apiBaseUrl].
abstract final class ApiConstants {
  // Auth
  static const String authLogin = '/auth/login';
  static const String authRegister = '/auth/register';
  static const String authRefresh = '/auth/refresh';
  static const String authLogout = '/auth/logout';

  // Wardrobe
  static const String wardrobeItems = '/wardrobe/items';
  static const String wardrobeUpload = '/wardrobe/upload';

  // Body Analysis
  static const String bodyAnalysis = '/body-analysis';
  static const String bodyAnalysisUpload = '/body-analysis/upload';

  // Virtual Try-On
  static const String tryOn = '/try-on';
  static const String tryOnGenerate = '/try-on/generate';

  // Recommendations
  static const String recommendations = '/recommendations';

  // Subscription
  static const String subscriptionPlans = '/subscription/plans';
  static const String subscriptionCreate = '/subscription/create';
  static const String subscriptionCancel = '/subscription/cancel';

  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 60); // Try-on puede tardar
}
