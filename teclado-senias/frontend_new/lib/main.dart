import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'config/theme.dart';
import 'config/routes.dart';

void main() {
  runApp(
    const ProviderScope(
      child: TecladoDeSignosApp(),
    ),
  );
}

class TecladoDeSignosApp extends ConsumerWidget {
  const TecladoDeSignosApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'Teclado de Señas',
      theme: lightTheme(),
      darkTheme: darkTheme(),
      routerDelegate: router.routerDelegate,
      routeInformationParser: router.routeInformationParser,
      routeInformationProvider: router.routeInformationProvider,
      debugShowCheckedModeBanner: false,
    );
  }
}
