/// Fallo de dominio — tipado para evitar excepciones sin manejar.
/// Usar en casos de uso y repositorios para retornar errores tipados.
///
/// Implementación con Dart 3 sealed class nativo.
/// No requiere code generation (freezed removido para evitar bloqueo de build_runner).
sealed class Failure {
  const Failure();
}

/// Error de red (sin conexión, timeout, DNS)
final class NetworkFailure extends Failure {
  const NetworkFailure({
    required this.message,
    this.statusCode,
  });

  final String message;
  final int? statusCode;

  @override
  String toString() =>
      'NetworkFailure(message: $message, statusCode: $statusCode)';
}

/// Credenciales inválidas o sesión expirada
final class AuthFailure extends Failure {
  const AuthFailure({required this.message});

  final String message;

  @override
  String toString() => 'AuthFailure(message: $message)';
}

/// El servidor retornó un error conocido
final class ServerFailure extends Failure {
  const ServerFailure({
    required this.message,
    required this.statusCode,
  });

  final String message;
  final int statusCode;

  @override
  String toString() =>
      'ServerFailure(message: $message, statusCode: $statusCode)';
}

/// El usuario no tiene permisos para la operación
final class PermissionFailure extends Failure {
  const PermissionFailure({required this.message});

  final String message;

  @override
  String toString() => 'PermissionFailure(message: $message)';
}

/// Dato no encontrado
final class NotFoundFailure extends Failure {
  const NotFoundFailure({required this.resource});

  final String resource;

  @override
  String toString() => 'NotFoundFailure(resource: $resource)';
}

/// Error de validación (campos inválidos)
final class ValidationFailure extends Failure {
  const ValidationFailure({required this.errors});

  final Map<String, List<String>> errors;

  @override
  String toString() => 'ValidationFailure(errors: $errors)';
}

/// Error inesperado
final class UnknownFailure extends Failure {
  const UnknownFailure({required this.message});

  final String message;

  @override
  String toString() => 'UnknownFailure(message: $message)';
}
