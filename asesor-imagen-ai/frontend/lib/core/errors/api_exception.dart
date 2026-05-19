/// Excepción lanzada por [DioClient] antes de convertirse en [Failure].
/// No debe escapar de la capa de datos.
final class ApiException implements Exception {
  const ApiException({
    required this.message,
    this.statusCode,
    this.errors,
  });

  final String message;
  final int? statusCode;
  final Map<String, List<String>>? errors;

  @override
  String toString() =>
      'ApiException(statusCode: $statusCode, message: $message)';
}
