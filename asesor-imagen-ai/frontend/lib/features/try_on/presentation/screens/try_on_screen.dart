import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:share_plus/share_plus.dart' show Share;

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';
import 'package:asesor_imagen_ai/features/try_on/data/try_on_repository.dart';
import 'package:asesor_imagen_ai/features/wardrobe/data/wardrobe_repository.dart';
import 'package:asesor_imagen_ai/widgets/upload_zone.dart';
import 'package:asesor_imagen_ai/widgets/wardrobe_grid.dart';
import 'package:asesor_imagen_ai/widgets/ai_insight_chip.dart';

// ---------------------------------------------------------------------------
// TryOnScreen — diseño Stitch (Erik aprobado)
// Layout: Row(Sidebar 200px | MainContent scrollable)
// Secciones: Tu Foto upload | Tu Ropa grid | Generar botón | Tu Look resultado
// ---------------------------------------------------------------------------

class TryOnScreen extends ConsumerWidget {
  const TryOnScreen({super.key});

  static const routeName = '/try-on';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final screenWidth = MediaQuery.of(context).size.width;
    final showSidebar = screenWidth >= 600;

    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      body: SafeArea(
        child: Row(
          children: [
            // Sidebar — solo en pantallas >= 600px (tablet/web)
            if (showSidebar) const _StitchSidebar(),

            // Main content
            Expanded(
              child: _TryOnMainContent(showHeader: !showSidebar),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Sidebar — replicación fiel del diseño Stitch
// ---------------------------------------------------------------------------

class _StitchSidebar extends StatelessWidget {
  const _StitchSidebar();

  static const _primaryBlue = Color(0xFF0058BE);
  static const _activeBg = Color(0xFFEBF2FF);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 200,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(
          right: BorderSide(color: Color(0xFFE5E7EB), width: 1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Logo
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 24),
            child: Row(
              children: [
                ShaderMask(
                  shaderCallback: (bounds) => const LinearGradient(
                    colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
                  ).createShader(bounds),
                  child: const Icon(Icons.auto_awesome,
                      size: 20, color: Colors.white),
                ),
                const SizedBox(width: 8),
                const Text(
                  'StyleAI',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: _primaryBlue,
                  ),
                ),
              ],
            ),
          ),

          // Nav items
          _SidebarNavItem(
            icon: Icons.auto_awesome,
            label: 'Virtual Try-On',
            isActive: true,
            activeBlue: _primaryBlue,
            activeBg: _activeBg,
          ),
          _SidebarNavItem(
            icon: Icons.checkroom_outlined,
            label: 'My Wardrobe',
            isActive: false,
            activeBlue: _primaryBlue,
            activeBg: _activeBg,
          ),
          _SidebarNavItem(
            icon: Icons.bar_chart_outlined,
            label: 'Style Insights',
            isActive: false,
            activeBlue: _primaryBlue,
            activeBg: _activeBg,
          ),
          _SidebarNavItem(
            icon: Icons.collections_bookmark_outlined,
            label: 'Collections',
            isActive: false,
            activeBlue: _primaryBlue,
            activeBg: _activeBg,
          ),
        ],
      ),
    );
  }
}

class _SidebarNavItem extends StatelessWidget {
  const _SidebarNavItem({
    required this.icon,
    required this.label,
    required this.isActive,
    required this.activeBlue,
    required this.activeBg,
  });

  final IconData icon;
  final String label;
  final bool isActive;
  final Color activeBlue;
  final Color activeBg;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: isActive ? activeBg : Colors.transparent,
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
        ),
        child: Row(
          children: [
            Icon(
              icon,
              size: 17,
              color: isActive ? activeBlue : const Color(0xFF9CA3AF),
            ),
            const SizedBox(width: 10),
            Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: isActive ? FontWeight.w600 : FontWeight.w400,
                color: isActive ? activeBlue : const Color(0xFF9CA3AF),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Main Content — columna scrollable con las 3 secciones + resultado
// ---------------------------------------------------------------------------

class _TryOnMainContent extends ConsumerStatefulWidget {
  const _TryOnMainContent({required this.showHeader});

  final bool showHeader;

  @override
  ConsumerState<_TryOnMainContent> createState() => _TryOnMainContentState();
}

class _TryOnMainContentState extends ConsumerState<_TryOnMainContent> {
  final _scrollController = ScrollController();

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final tryOnState = ref.watch(tryOnProvider);
    final wardrobeAsync = ref.watch(wardrobeProvider);

    return CustomScrollView(
      controller: _scrollController,
      slivers: [
        // Header — solo en mobile (sin sidebar)
        if (widget.showHeader)
          SliverToBoxAdapter(
            child: _MobileHeader(tryOnState: tryOnState),
          ),

        // Padding top en tablet/desktop
        if (!widget.showHeader)
          const SliverToBoxAdapter(child: SizedBox(height: 24)),

        // Título sección (tablet/desktop)
        if (!widget.showHeader)
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 4),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Virtual Try-On',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF111827),
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        'Pruebate un look con inteligencia artificial',
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey[500],
                        ),
                      ),
                    ],
                  ),
                  if (tryOnState.usage != null)
                    _UsageChip(usage: tryOnState.usage!),
                ],
              ),
            ),
          ),

        // ---------------------------------------------------------------
        // Sección 1 — Tu Foto
        // ---------------------------------------------------------------
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 20, 24, 0),
            child: UploadZone(
              photoPath: tryOnState.userPhotoPath,
              onPhotoSelected: (path) =>
                  ref.read(tryOnProvider.notifier).setUserPhoto(path),
            ),
          ),
        ),

        // ---------------------------------------------------------------
        // Sección 2 — Tu Ropa (wardrobe grid)
        // ---------------------------------------------------------------
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 20, 24, 0),
            child: wardrobeAsync.when(
              loading: () => const _WardrobeGridSkeleton(),
              error: (e, _) => _WardrobeGridError(message: e.toString()),
              data: (items) => WardrobeGrid(
                items: items,
                selectedIds: tryOnState.selectedItemIds,
                onToggle: (id) =>
                    ref.read(tryOnProvider.notifier).toggleItem(id),
              ),
            ),
          ),
        ),

        // ---------------------------------------------------------------
        // Sección 3 — Botón Generar Outfit Ideal
        // ---------------------------------------------------------------
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 20, 24, 0),
            child: _GenerateOutfitButton(
              tryOnState: tryOnState,
              onGenerate: () => ref.read(tryOnProvider.notifier).generate(),
              onScrollToResult: () => _scrollToResult(),
            ),
          ),
        ),

        // ---------------------------------------------------------------
        // Sección 4 — Tu Look (resultado inline)
        // ---------------------------------------------------------------
        if (tryOnState.status == TryOnStatus.loading ||
            tryOnState.result != null)
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 28, 24, 0),
              child: _TuLookResult(
                key: const Key('tu-look-result'),
                tryOnState: tryOnState,
                onSave: () => _onSave(context, ref),
                onShare: () => _onShare(tryOnState.result),
              ),
            ),
          ),

        // Banner soft cap
        if (tryOnState.usage?.isAtCap == true)
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 16, 24, 0),
              child: _SoftCapBanner(
                onUpgrade: () => _showUpgradeSheet(context),
              ),
            ),
          ),

        const SliverToBoxAdapter(child: SizedBox(height: 40)),
      ],
    );
  }

  void _scrollToResult() {
    Future.delayed(const Duration(milliseconds: 300), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 600),
          curve: Curves.easeOutCubic,
        );
      }
    });
  }

  void _onSave(BuildContext context, WidgetRef ref) {
    final result = ref.read(tryOnProvider).result;
    if (result == null) return;
    ref.read(tryOnRepositoryProvider).saveTryOnResult(result.id);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Look guardado en tu armario'),
        backgroundColor: AppColors.success,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
        ),
      ),
    );
  }

  void _onShare(TryOnResult? result) {
    if (result == null) return;
    Share.share(
      'Mira este look generado con Asesor de Imagen AI!\n${result.insightTitle}',
    );
  }

  void _showUpgradeSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(DesignTokens.radiusXLarge),
        ),
      ),
      builder: (_) => const _UpgradeSheet(),
    );
  }
}

// ---------------------------------------------------------------------------
// Mobile header con Usage chip
// ---------------------------------------------------------------------------

class _MobileHeader extends StatelessWidget {
  const _MobileHeader({required this.tryOnState});

  final TryOnState tryOnState;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Virtual Try-On',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFF111827),
                ),
              ),
              if (tryOnState.usage != null)
                _UsageChip(usage: tryOnState.usage!),
            ],
          ),
          const SizedBox(height: 2),
          Text(
            'Pruebate un look con inteligencia artificial',
            style: TextStyle(fontSize: 12, color: Colors.grey[500]),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Botón "Generar Outfit Ideal" — gradiente #0058BE → #9466FF
// ---------------------------------------------------------------------------

class _GenerateOutfitButton extends StatelessWidget {
  const _GenerateOutfitButton({
    required this.tryOnState,
    required this.onGenerate,
    required this.onScrollToResult,
  });

  final TryOnState tryOnState;
  final Future<TryOnResult?> Function() onGenerate;
  final VoidCallback onScrollToResult;

  static const _gradientStart = Color(0xFF0058BE);
  static const _gradientEnd = Color(0xFF9466FF);

  bool get _canGenerate =>
      tryOnState.userPhotoPath != null &&
      tryOnState.selectedItemIds.isNotEmpty &&
      tryOnState.usage?.isAtCap != true &&
      tryOnState.status != TryOnStatus.loading;

  @override
  Widget build(BuildContext context) {
    final isLoading = tryOnState.status == TryOnStatus.loading;

    return SizedBox(
      height: 52,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: _canGenerate
              ? const LinearGradient(
                  colors: [_gradientStart, _gradientEnd],
                  begin: Alignment.centerLeft,
                  end: Alignment.centerRight,
                )
              : const LinearGradient(
                  colors: [Color(0xFFD1D5DB), Color(0xFFD1D5DB)]),
          borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
          boxShadow: _canGenerate
              ? [
                  BoxShadow(
                    color: _gradientStart.withOpacity(0.35),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ]
              : [],
        ),
        child: ElevatedButton.icon(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            disabledBackgroundColor: Colors.transparent,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
            ),
          ),
          onPressed: _canGenerate
              ? () async {
                  final result = await onGenerate();
                  if (result != null) onScrollToResult();
                }
              : null,
          icon: isLoading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: Colors.white,
                  ),
                )
              : const Icon(Icons.auto_awesome, color: Colors.white, size: 18),
          label: Text(
            isLoading ? 'Generando outfit...' : 'Generar Outfit Ideal',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 15,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.2,
            ),
          ),
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Sección "Tu Look" — resultado inline en pantalla
// ---------------------------------------------------------------------------

class _TuLookResult extends StatelessWidget {
  const _TuLookResult({
    super.key,
    required this.tryOnState,
    required this.onSave,
    required this.onShare,
  });

  final TryOnState tryOnState;
  final VoidCallback onSave;
  final VoidCallback onShare;

  @override
  Widget build(BuildContext context) {
    final result = tryOnState.result;
    final isLoading = tryOnState.status == TryOnStatus.loading;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Divider
        Container(
          height: 1,
          color: const Color(0xFFE5E7EB),
          margin: const EdgeInsets.only(bottom: 24),
        ),

        // Card resultado
        AIInsightCard(
          imageUrl: result?.imageUrl ?? '',
          insightTitle: result?.insightTitle ?? '',
          insightExplanation: result?.insightExplanation ?? '',
          isLoading: isLoading,
          onSave: onSave,
          onShare: onShare,
        ),
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// Usage chip
// ---------------------------------------------------------------------------

class _UsageChip extends StatelessWidget {
  const _UsageChip({required this.usage});

  final UsageInfo usage;

  @override
  Widget build(BuildContext context) {
    final color = usage.isAtCap ? AppColors.error : const Color(0xFF0058BE);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(DesignTokens.radiusFull),
        border: Border.all(color: color.withOpacity(0.25)),
      ),
      child: Text(
        '${usage.used}/${usage.limit} intentos',
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: color,
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Wardrobe skeleton / error states
// ---------------------------------------------------------------------------

class _WardrobeGridSkeleton extends StatelessWidget {
  const _WardrobeGridSkeleton();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Tu Ropa',
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w600,
            color: Color(0xFF374151),
          ),
        ),
        const SizedBox(height: 10),
        Row(
          children: List.generate(
            5,
            (i) => Expanded(
              child: Padding(
                padding: EdgeInsets.only(right: i < 4 ? 8 : 0),
                child: AspectRatio(
                  aspectRatio: 0.75,
                  child: Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFFF3F4F6),
                      borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class _WardrobeGridError extends StatelessWidget {
  const _WardrobeGridError({required this.message});
  final String message;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.error.withOpacity(0.05),
        borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
        border: Border.all(color: AppColors.error.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          Icon(Icons.warning_amber_outlined,
              color: AppColors.error, size: 18),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              'No se pudo cargar tu armario. Usando items de muestra.',
              style: TextStyle(
                fontSize: 12,
                color: AppColors.error,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Soft cap banner + upgrade sheet (reutilizados del diseño anterior)
// ---------------------------------------------------------------------------

class _SoftCapBanner extends StatelessWidget {
  const _SoftCapBanner({required this.onUpgrade});
  final VoidCallback onUpgrade;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.warning.withOpacity(0.08),
        borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
        border: Border.all(color: AppColors.warning.withOpacity(0.35)),
      ),
      child: Row(
        children: [
          Icon(Icons.lock_clock_outlined, color: AppColors.warning, size: 18),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              'Has alcanzado tu limite semanal gratuito.',
              style: TextStyle(
                fontSize: 12,
                color: AppColors.warning,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          TextButton(
            onPressed: onUpgrade,
            child: const Text('Upgrade',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
          ),
        ],
      ),
    );
  }
}

class _UpgradeSheet extends StatelessWidget {
  const _UpgradeSheet();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Center(
            child: Container(
              width: 40,
              height: 4,
              margin: const EdgeInsets.only(bottom: 24),
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          ShaderMask(
            shaderCallback: (bounds) => const LinearGradient(
              colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
            ).createShader(bounds),
            child: const Icon(Icons.workspace_premium,
                size: 48, color: Colors.white),
          ),
          const SizedBox(height: 16),
          Text(
            'Desbloquea intentos ilimitados',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w700,
                ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            'Con Premium obtenes try-ons ilimitados, analisis de cuerpo avanzado y recomendaciones personalizadas.',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          DecoratedBox(
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
                begin: Alignment.centerLeft,
                end: Alignment.centerRight,
              ),
              borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
            ),
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.transparent,
                shadowColor: Colors.transparent,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                ),
              ),
              onPressed: () => Navigator.pop(context),
              child: const Text(
                'Ver planes Premium',
                style: TextStyle(
                    color: Colors.white, fontWeight: FontWeight.w600),
              ),
            ),
          ),
          const SizedBox(height: 12),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Ahora no'),
          ),
          const SizedBox(height: 8),
        ],
      ),
    );
  }
}
