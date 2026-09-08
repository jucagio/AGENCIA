import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/auth_service.dart';

final authServiceProvider = Provider((ref) => AuthService());

final isLoggedInProvider = FutureProvider<bool>((ref) async {
  final authService = ref.watch(authServiceProvider);
  return authService.isLoggedIn();
});

final currentUserProvider = Provider((ref) {
  final authService = ref.watch(authServiceProvider);
  return authService.getCurrentUser();
});

final loginProvider = FutureProvider.family<void, (String, String)>((ref, args) async {
  final authService = ref.watch(authServiceProvider);
  final (email, password) = args;
  await authService.login(email, password);
  ref.invalidate(isLoggedInProvider);
  ref.invalidate(currentUserProvider);
});

final logoutProvider = FutureProvider<void>((ref) async {
  final authService = ref.watch(authServiceProvider);
  await authService.logout();
  ref.invalidate(isLoggedInProvider);
  ref.invalidate(currentUserProvider);
});
