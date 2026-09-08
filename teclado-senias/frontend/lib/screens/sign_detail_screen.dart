/// SignDetailScreen — detalle completo de una seña con reproductor de video
/// GET /signs/:id — muestra video, descripción, dificultad, botón de favorito
library;

import 'package:chewie/chewie.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:video_player/video_player.dart';

import '../config/theme.dart';
import '../models/sign.dart';
import '../providers/auth_provider.dart';
import '../providers/favorites_provider.dart';
import '../providers/signs_provider.dart';
import '../widgets/category_chip.dart';
import '../widgets/loading_indicator.dart';

class SignDetailScreen extends ConsumerStatefulWidget {
  const SignDetailScreen({super.key, required this.signId});

  final String signId;

  @override
  ConsumerState<SignDetailScreen> createState() => _SignDetailScreenState();
}

class _SignDetailScreenState extends ConsumerState<SignDetailScreen> {
  VideoPlayerController? _videoController;
  ChewieController? _chewieController;
  bool _videoReady = false;

  @override
  void dispose() {
    _chewieController?.dispose();
    _videoController?.dispose();
    super.dispose();
  }

  Future<void> _initVideo(String videoUrl) async {
    if (_videoController != null) return;

    _videoController = VideoPlayerController.networkUrl(Uri.parse(videoUrl));
    await _videoController!.initialize();

    _chewieController = ChewieController(
      videoPlayerController: _videoController!,
      autoPlay: true,
      looping: true,
      showControlsOnInitialize: false,
      aspectRatio: _videoController!.value.aspectRatio,
      placeholder: Container(color: AppColors.dark700),
      materialProgressColors: ChewieProgressColors(
        playedColor: AppColors.primary,
        handleColor: AppColors.primary,
        backgroundColor: AppColors.light200,
        bufferedColor: AppColors.primary.withAlpha(77),
      ),
    );

    if (mounted) setState(() => _videoReady = true);
  }

  @override
  Widget build(BuildContext context) {
    final signAsync = ref.watch(signDetailProvider(widget.signId));

    return Scaffold(
      body: signAsync.when(
        loading: () => const FullScreenLoader(message: 'Cargando seña...'),
        error: (err, _) => Scaffold(
          appBar: AppBar(),
          body: ErrorState(
            message: 'No se pudo cargar la seña.',
            onRetry: () => ref.invalidate(signDetailProvider(widget.signId)),
          ),
        ),
        data: (sign) => _buildDetail(context, sign),
      ),
    );
  }

  Widget _buildDetail(BuildContext context, SignDetail sign) {
    // Iniciar video cuando se carga el detalle
    if (!_videoReady && sign.videoUrl.isNotEmpty) {
      WidgetsBinding.instance.addPostFrameCallback(
        (_) => _initVideo(sign.videoUrl),
      );
    }

    final isAuth = ref.watch(authStateProvider).valueOrNull != null;
    final favoritesState = ref.watch(favoritesProvider);
    final isFavorite = favoritesState.isFavorite(sign.id);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return CustomScrollView(
      slivers: [
        // AppBar expandible con video
        SliverAppBar(
          expandedHeight: 280,
          pinned: true,
          leading: Semantics(
            label: 'Volver',
            button: true,
            child: const BackButton(),
          ),
          actions: [
            if (isAuth)
              Padding(
                padding: const EdgeInsets.only(right: AppSpacing.s2),
                child: _FavoriteIconButton(
                  signId: sign.id,
                  isFavorite: isFavorite,
                ),
              ),
          ],
          flexibleSpace: FlexibleSpaceBar(
            background: _VideoSection(
              videoReady: _videoReady,
              chewieController: _chewieController,
              isDark: isDark,
            ),
          ),
        ),

        // Contenido
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.s6),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Palabra principal
                Text(
                  sign.word,
                  style: AppTextStyles.h1.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                  semanticsLabel: 'Seña: ${sign.word}',
                ),
                const SizedBox(height: AppSpacing.s3),

                // Dificultad
                if (sign.difficultyLevel > 0) ...[
                  DifficultyDots(
                    level: sign.difficultyLevel,
                    showLabel: true,
                    dotSize: 12,
                  ),
                  const SizedBox(height: AppSpacing.s4),
                ],

                // Código de idioma
                Wrap(
                  spacing: AppSpacing.s2,
                  children: [
                    _InfoChip(
                      icon: Icons.language_rounded,
                      label: sign.languageCode.toUpperCase(),
                    ),
                    if (sign.difficulty != null)
                      _InfoChip(
                        icon: Icons.bar_chart_rounded,
                        label: sign.difficultyLabel,
                      ),
                  ],
                ),

                if (sign.description != null &&
                    sign.description!.isNotEmpty) ...[
                  const SizedBox(height: AppSpacing.s6),
                  const Divider(),
                  const SizedBox(height: AppSpacing.s4),
                  Text(
                    'Descripción',
                    style: AppTextStyles.h3.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.s3),
                  Text(
                    sign.description!,
                    style: AppTextStyles.bodyLg.copyWith(
                      color: Theme.of(context)
                          .colorScheme
                          .onSurface
                          .withAlpha(204),
                    ),
                  ),
                ],

                // Botón de favorito en el cuerpo (accesibilidad)
                if (isAuth) ...[
                  const SizedBox(height: AppSpacing.s8),
                  OutlinedButton.icon(
                    onPressed: () {
                      final notifier = ref.read(favoritesProvider.notifier);
                      if (isFavorite) {
                        notifier.removeFavorite(sign.id);
                      } else {
                        notifier.addFavorite(sign.id);
                      }
                    },
                    icon: Icon(
                      isFavorite
                          ? Icons.favorite_rounded
                          : Icons.favorite_border_rounded,
                      size: 20,
                      color: isFavorite ? AppColors.error : null,
                    ),
                    label: Text(
                      isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos',
                    ),
                    style: isFavorite
                        ? OutlinedButton.styleFrom(
                            foregroundColor: AppColors.error,
                            side: const BorderSide(color: AppColors.error, width: 2),
                          )
                        : null,
                  ),
                ],

                const SizedBox(height: AppSpacing.s10),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// Sección de video con Chewie
// ---------------------------------------------------------------------------

class _VideoSection extends StatelessWidget {
  const _VideoSection({
    required this.videoReady,
    required this.chewieController,
    required this.isDark,
  });

  final bool videoReady;
  final ChewieController? chewieController;
  final bool isDark;

  @override
  Widget build(BuildContext context) {
    if (!videoReady || chewieController == null) {
      return Container(
        color: isDark ? AppColors.dark800 : AppColors.light200,
        child: const Center(
          child: AppLoadingIndicator(size: 40, semanticLabel: 'Cargando video'),
        ),
      );
    }

    return Chewie(controller: chewieController!);
  }
}

// ---------------------------------------------------------------------------
// Chip de info (idioma, dificultad)
// ---------------------------------------------------------------------------

class _InfoChip extends StatelessWidget {
  const _InfoChip({required this.icon, required this.label});
  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s3,
        vertical: AppSpacing.s1,
      ),
      decoration: BoxDecoration(
        color: isDark ? AppColors.dark700 : AppColors.light200,
        borderRadius: AppRadius.borderFull,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14,
              color: Theme.of(context).colorScheme.onSurface.withAlpha(153)),
          const SizedBox(width: 4),
          Text(
            label,
            style: AppTextStyles.caption.copyWith(
              color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Botón favorito en el AppBar
// ---------------------------------------------------------------------------

class _FavoriteIconButton extends ConsumerWidget {
  const _FavoriteIconButton({
    required this.signId,
    required this.isFavorite,
  });

  final String signId;
  final bool isFavorite;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Semantics(
      label: isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos',
      button: true,
      child: IconButton(
        onPressed: () {
          final notifier = ref.read(favoritesProvider.notifier);
          if (isFavorite) {
            notifier.removeFavorite(signId);
          } else {
            notifier.addFavorite(signId);
          }
        },
        icon: Icon(
          isFavorite ? Icons.favorite_rounded : Icons.favorite_border_rounded,
          color: isFavorite ? AppColors.error : null,
        ),
        tooltip: isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos',
      ),
    );
  }
}
