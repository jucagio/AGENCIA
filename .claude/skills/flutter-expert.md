# Flutter Expert — Skill para Claude Code

## Descripcion
Skill experta en Flutter y Dart para desarrollar aplicaciones moviles cross-platform de produccion. Cubre arquitectura limpia, state management, testing, y patrones modernos de Dart 3. Optimizada para los agentes Sasha y Brook de la Agencia.

## Instrucciones

Cuando el usuario pida ayuda con Flutter o Dart, sigue estas directrices:

### Arquitectura del Proyecto

Usar **Clean Architecture** con la siguiente estructura:

```
lib/
  core/
    constants/          # Colores, strings, dimensiones
    errors/             # Failures y exceptions personalizadas
    network/            # Cliente HTTP, interceptors
    theme/              # ThemeData, TextThemes
    utils/              # Helpers y extensiones
    di/                 # Inyeccion de dependencias (get_it + injectable)
  features/
    auth/
      data/
        datasources/    # Remote (API) y Local (cache)
        models/         # DTOs con fromJson/toJson
        repositories/   # Implementacion del repositorio
      domain/
        entities/       # Entidades puras (sin dependencias)
        repositories/   # Contrato abstracto del repositorio
        usecases/       # Logica de negocio (1 caso de uso = 1 clase)
      presentation/
        bloc/           # BLoC: events, states, bloc
        pages/          # Pantallas completas
        widgets/        # Widgets reutilizables del feature
    home/
      ...misma estructura...
  app.dart              # MaterialApp / configuracion de rutas
  main.dart             # Punto de entrada + init de DI
```

### State Management — BLoC (recomendado) vs Riverpod

**BLoC (flutter_bloc) — Usar cuando:**
- El proyecto tiene logica de negocio compleja
- Se necesita trazabilidad de eventos (debugging, analytics)
- El equipo es grande y necesita patron predecible

```dart
// Event
sealed class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested({required this.email, required this.password});
}

// State
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {
  final User user;
  AuthSuccess(this.user);
}
class AuthFailure extends AuthState {
  final String message;
  AuthFailure(this.message);
}

// Bloc
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUseCase loginUseCase;

  AuthBloc(this.loginUseCase) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    final result = await loginUseCase(
      LoginParams(email: event.email, password: event.password),
    );
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (user) => emit(AuthSuccess(user)),
    );
  }
}
```

**Riverpod — Usar cuando:**
- Se necesita reactividad granular (rebuild solo lo necesario)
- Proyecto mas pequeno o prototipo rapido
- Se prefiere menos boilerplate

```dart
// Provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.read(loginUseCaseProvider));
});

class AuthNotifier extends StateNotifier<AuthState> {
  final LoginUseCase _loginUseCase;
  AuthNotifier(this._loginUseCase) : super(const AuthState.initial());

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    final result = await _loginUseCase(LoginParams(email: email, password: password));
    state = result.fold(
      (failure) => AuthState.failure(failure.message),
      (user) => AuthState.success(user),
    );
  }
}
```

### Dart 3 — Patrones Modernos

```dart
// Sealed classes para estados (reemplaza enums con data)
sealed class Result<T> {}
class Success<T> extends Result<T> {
  final T data;
  Success(this.data);
}
class Failure<T> extends Result<T> {
  final String message;
  Failure(this.message);
}

// Pattern matching con switch expressions
String describeResult(Result<User> result) => switch (result) {
  Success(data: final user) => 'Welcome ${user.name}',
  Failure(message: final msg) => 'Error: $msg',
};

// Records para retornar multiples valores
(String name, int age) getUserInfo() => ('Juan', 28);

// Destructuring
final (name, age) = getUserInfo();

// If-case para validation
if (json case {'name': String name, 'age': int age}) {
  return User(name: name, age: age);
}
```

### Navegacion — go_router (recomendado)

```dart
final router = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    final isLoggedIn = /* check auth state */;
    if (!isLoggedIn && !state.matchedLocation.startsWith('/auth')) {
      return '/auth/login';
    }
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/auth/login',
      builder: (context, state) => const LoginPage(),
    ),
    ShellRoute(
      builder: (context, state, child) => ScaffoldWithNav(child: child),
      routes: [
        GoRoute(path: '/home', builder: (_, __) => const HomePage()),
        GoRoute(path: '/profile', builder: (_, __) => const ProfilePage()),
      ],
    ),
  ],
);
```

### Conexion con APIs (FastAPI / Supabase)

**HTTP con Dio:**
```dart
class ApiClient {
  late final Dio _dio;

  ApiClient({required String baseUrl, String? token}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    ));

    _dio.interceptors.addAll([
      LogInterceptor(requestBody: true, responseBody: true),
      // Interceptor de retry
      RetryInterceptor(dio: _dio, retries: 3),
    ]);
  }

  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) =>
      _dio.get(path, queryParameters: queryParameters);

  Future<Response<T>> post<T>(String path, {dynamic data}) =>
      _dio.post(path, data: data);
}
```

**Supabase Flutter SDK:**
```dart
// Inicializacion en main.dart
await Supabase.initialize(
  url: const String.fromEnvironment('SUPABASE_URL'),
  anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
);

// Uso
final supabase = Supabase.instance.client;

// Auth
final response = await supabase.auth.signInWithPassword(
  email: email,
  password: password,
);

// Query con RLS (automatico con el token del usuario)
final data = await supabase
    .from('orders')
    .select('*, items(*)')
    .eq('status', 'active')
    .order('created_at', ascending: false)
    .limit(20);

// Realtime
supabase
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at')
    .listen((data) {
      // Actualizar UI
    });

// Storage
final file = File('path/to/image.jpg');
await supabase.storage
    .from('avatars')
    .upload('user_${user.id}/avatar.jpg', file);
```

### Testing

**Unit Tests:**
```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
void main() {
  late LoginUseCase useCase;
  late MockAuthRepository mockRepo;

  setUp(() {
    mockRepo = MockAuthRepository();
    useCase = LoginUseCase(mockRepo);
  });

  test('should return User when login succeeds', () async {
    when(mockRepo.login(any, any)).thenAnswer((_) async => Right(tUser));

    final result = await useCase(LoginParams(email: 'test@test.com', password: '123'));

    expect(result, Right(tUser));
    verify(mockRepo.login('test@test.com', '123'));
  });
}
```

**Widget Tests:**
```dart
testWidgets('LoginPage shows error on failure', (tester) async {
  final bloc = MockAuthBloc();
  when(() => bloc.state).thenReturn(AuthFailure('Invalid credentials'));

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<AuthBloc>.value(
        value: bloc,
        child: const LoginPage(),
      ),
    ),
  );

  expect(find.text('Invalid credentials'), findsOneWidget);
});
```

**Integration Tests:**
```dart
// integration_test/app_test.dart
void main() {
  testWidgets('full login flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(const Key('email')), 'test@test.com');
    await tester.enterText(find.byKey(const Key('password')), 'password123');
    await tester.tap(find.byKey(const Key('loginButton')));
    await tester.pumpAndSettle();

    expect(find.text('Home'), findsOneWidget);
  });
}
```

### Paquetes Esenciales (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  # State Management
  flutter_bloc: ^8.1.0          # BLoC pattern
  # O riverpod: ^2.5.0          # Alternativa a BLoC
  equatable: ^2.0.0             # Comparacion de objetos
  # Navegacion
  go_router: ^14.0.0            # Routing declarativo
  # Network
  dio: ^5.4.0                   # HTTP client
  supabase_flutter: ^2.5.0      # Supabase SDK
  # DI
  get_it: ^7.6.0                # Service locator
  injectable: ^2.3.0            # Code generation para DI
  # Funcional
  dartz: ^0.10.1                # Either, Option, etc.
  # Storage local
  shared_preferences: ^2.2.0    # Key-value simple
  hive: ^2.2.0                  # BD local rapida
  # UI
  flutter_screenutil: ^5.9.0    # Responsive design
  cached_network_image: ^3.3.0  # Cache de imagenes
  shimmer: ^3.0.0               # Loading placeholders

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0             # Testing de BLoCs
  mocktail: ^1.0.0              # Mocking
  injectable_generator: ^2.4.0  # DI code gen
  build_runner: ^2.4.0          # Code generation
  flutter_lints: ^3.0.0         # Linting rules
  integration_test:
    sdk: flutter
```

### Comandos Frecuentes

```bash
# Crear proyecto
flutter create --org com.agencia my_app

# Generar codigo (DI, freezed, json_serializable)
dart run build_runner build --delete-conflicting-outputs

# Tests
flutter test                              # Unit + widget tests
flutter test integration_test/            # Integration tests
flutter test --coverage                   # Coverage report

# Build
flutter build apk --release               # Android APK
flutter build appbundle --release          # Android AAB (Play Store)
flutter build ios --release                # iOS
flutter build web --release                # Web

# Analisis
flutter analyze                            # Linting
dart fix --apply                           # Auto-fix issues
```

### Mejores Practicas

1. **Nunca poner logica en widgets.** Los widgets solo renderizan estado. La logica va en BLoC/Riverpod.
2. **Un archivo, una responsabilidad.** No mezclar modelos, widgets y logica en el mismo archivo.
3. **Usar const constructors** en todos los widgets que no cambien.
4. **Manejar todos los estados**: initial, loading, success, failure, empty. Nunca dejar estados sin cubrir.
5. **Responsive design**: Usar ScreenUtil o LayoutBuilder, nunca dimensiones hardcodeadas.
6. **Null safety estricto**: No usar `!` (bang operator) a menos que sea absolutamente seguro. Preferir `??` o pattern matching.
7. **Temas**: Definir todo en ThemeData. No usar colores o estilos hardcodeados en widgets.
8. **Assets**: Generar constantes para assets con flutter_gen o manualmente en una clase Assets.
9. **Internacionalizacion**: Usar flutter_localizations desde el inicio si hay chance de multi-idioma.
10. **Performance**: Usar RepaintBoundary en listas largas, const widgets, y evitar rebuilds innecesarios.
