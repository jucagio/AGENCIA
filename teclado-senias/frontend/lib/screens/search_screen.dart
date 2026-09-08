/// SearchScreen — búsqueda de señas + panel de traducción de texto
/// GET /signs/search + POST /signs/translate (auth requerido)
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../config/routes.dart';
import '../config/theme.dart';
import '../models/sign.dart';
import '../providers/auth_provider.dart';
import '../providers/signs_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/search_bar.dart';
import '../widgets/sign_card.dart';

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _translateCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _translateCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isAuth = ref.watch(authStateProvider).valueOrNull != null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Buscar'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Buscar seña'),
            Tab(text: 'Traducir texto'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _SearchTab(),
          isAuth
              ? _TranslateTab(translateCtrl: _translateCtrl)
              : _AuthRequiredTab(
                  message: 'Inicia sesión para usar la traducción de texto',
                ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Tab 1 — Búsqueda por palabra
// ---------------------------------------------------------------------------

class _SearchTab extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final searchState = ref.watch(searchProvider);
    final notifier = ref.read(searchProvider.notifier);

    return Column(
      children: [
        // Search bar
        Padding(
          padding: const EdgeInsets.all(AppSpacing.s4),
          child: AppSearchBar(
            hintText: 'Escribe una palabra en español...',
            autofocus: true,
            onChanged: (query) => notifier.search(query),
            onClear: notifier.clear,
          ),
        ),

        // Resultados
        Expanded(
          child: searchState.when(
            loading: () => const Center(child: AppLoadingIndicator(size: 32)),
            error: (err, _) => ErrorState(
              message: 'No se pudo realizar la búsqueda. Intenta de nuevo.',
              onRetry: null,
            ),
            data: (results) {
              if (results == null) {
                return _SearchPlaceholder();
              }
              if (results.isEmpty) {
                return EmptyState(
                  message:
                      'No encontramos señas para "${notifier.lastQuery}".\nIntenta con otra palabra.',
                  icon: Icons.search_off_rounded,
                );
              }
              return _SearchResults(signs: results);
            },
          ),
        ),
      ],
    );
  }
}

class _SearchPlaceholder extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.sign_language_outlined,
              size: 72,
              color:
                  Theme.of(context).colorScheme.onSurface.withAlpha(51),
            ),
            const SizedBox(height: AppSpacing.s4),
            Text(
              'Busca cualquier palabra en español\ny encuentra su seña',
              textAlign: TextAlign.center,
              style: AppTextStyles.body.copyWith(
                color:
                    Theme.of(context).colorScheme.onSurface.withAlpha(153),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SearchResults extends StatelessWidget {
  const _SearchResults({required this.signs});
  final List<Sign> signs;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.s3),
            child: Text(
              '${signs.length} resultado${signs.length == 1 ? "" : "s"}',
              style: AppTextStyles.bodySm.copyWith(
                color: Theme.of(context)
                    .colorScheme
                    .onSurface
                    .withAlpha(153),
              ),
            ),
          ),
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 0.72,
              ),
              itemCount: signs.length,
              itemBuilder: (context, i) => SignCard(sign: signs[i]),
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Tab 2 — Traducción de texto a señas
// ---------------------------------------------------------------------------

class _TranslateTab extends ConsumerWidget {
  const _TranslateTab({required this.translateCtrl});
  final TextEditingController translateCtrl;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final translationState = ref.watch(translationProvider);
    final notifier = ref.read(translationProvider.notifier);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.s4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Input de texto
          TextField(
            controller: translateCtrl,
            maxLines: 4,
            maxLength: 1000,
            textInputAction: TextInputAction.newline,
            style: AppTextStyles.bodyLg,
            decoration: InputDecoration(
              hintText: 'Escribe una frase para traducir...\nEj: hola cómo estás',
              alignLabelWithHint: true,
              counterStyle: AppTextStyles.caption,
            ),
          ),
          const SizedBox(height: AppSpacing.s4),

          // Botón traducir
          ElevatedButton.icon(
            onPressed: translationState.isLoading
                ? null
                : () => notifier.translate(translateCtrl.text),
            icon: translationState.isLoading
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2.5,
                      valueColor:
                          AlwaysStoppedAnimation<Color>(AppColors.white),
                    ),
                  )
                : const Icon(Icons.translate_rounded, size: 20),
            label: const Text('Traducir'),
          ),
          const SizedBox(height: AppSpacing.s6),

          // Resultado
          translationState.when(
            loading: () => const Center(child: AppLoadingIndicator(size: 32)),
            error: (err, _) => ErrorState(
              message: 'No se pudo traducir el texto. Intenta de nuevo.',
              onRetry: null,
            ),
            data: (result) {
              if (result == null) return const SizedBox.shrink();
              return _TranslationResult(result: result);
            },
          ),
        ],
      ),
    );
  }
}

class _TranslationResult extends StatelessWidget {
  const _TranslationResult({required this.result});
  final dynamic result;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Resumen
        Container(
          padding: const EdgeInsets.all(AppSpacing.s4),
          decoration: BoxDecoration(
            color: AppColors.infoBg,
            borderRadius: AppRadius.borderMd,
            border: Border.all(color: AppColors.info.withAlpha(77)),
          ),
          child: Row(
            children: [
              const Icon(Icons.info_outline_rounded,
                  size: 20, color: AppColors.info),
              const SizedBox(width: AppSpacing.s2),
              Expanded(
                child: Text(
                  '${result.matchCount} de ${result.totalWords} palabras encontradas',
                  style: AppTextStyles.bodySm.copyWith(color: AppColors.info),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: AppSpacing.s4),

        // Palabras sin seña
        if (result.unmatchedWords.isNotEmpty) ...[
          Text(
            'Palabras sin seña disponible:',
            style: AppTextStyles.label.copyWith(
              color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
            ),
          ),
          const SizedBox(height: AppSpacing.s2),
          Wrap(
            spacing: AppSpacing.s2,
            runSpacing: AppSpacing.s2,
            children: result.unmatchedWords
                .map<Widget>((w) => Chip(
                      label: Text(w),
                      backgroundColor: AppColors.warningBg,
                      labelStyle: AppTextStyles.bodySm
                          .copyWith(color: AppColors.warning),
                    ))
                .toList(),
          ),
          const SizedBox(height: AppSpacing.s5),
        ],

        // Señas encontradas
        if (result.matchedSigns.isNotEmpty) ...[
          Text(
            'Señas encontradas:',
            style: AppTextStyles.label.copyWith(
              color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
            ),
          ),
          const SizedBox(height: AppSpacing.s3),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 0.72,
            ),
            itemCount: result.matchedSigns.length,
            itemBuilder: (context, i) => SignCard(
              sign: result.matchedSigns[i],
              showFavoriteButton: false,
            ),
          ),
        ],
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// Estado de auth requerida
// ---------------------------------------------------------------------------

class _AuthRequiredTab extends StatelessWidget {
  const _AuthRequiredTab({required this.message});
  final String message;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.lock_outline_rounded,
              size: 64,
              color: Theme.of(context).colorScheme.onSurface.withAlpha(77),
            ),
            const SizedBox(height: AppSpacing.s4),
            Text(
              message,
              textAlign: TextAlign.center,
              style: AppTextStyles.body.copyWith(
                color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
              ),
            ),
            const SizedBox(height: AppSpacing.s6),
            ElevatedButton(
              onPressed: () => context.go(AppRoutes.login),
              child: const Text('Iniciar sesión'),
            ),
          ],
        ),
      ),
    );
  }
}
