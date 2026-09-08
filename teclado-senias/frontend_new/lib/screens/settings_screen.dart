/// SettingsScreen — configuración de cuenta, tema y accesibilidad
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../config/routes.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';

// ---------------------------------------------------------------------------
// Provider de tema (persiste en sesión)
// ---------------------------------------------------------------------------

final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.system);

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authStateProvider).valueOrNull;
    final themeMode = ref.watch(themeModeProvider);
    final isAuth = user != null;

    return Scaffold(
      appBar: AppBar(title: const Text('Ajustes')),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s4),
        children: [
          // Perfil
          if (isAuth) ...[
            _SectionHeader(title: 'Cuenta'),
            _ProfileCard(user: user!),
            const SizedBox(height: AppSpacing.s4),
          ] else ...[
            _SectionHeader(title: 'Cuenta'),
            _AuthCard(),
            const SizedBox(height: AppSpacing.s4),
          ],

          // Apariencia
          _SectionHeader(title: 'Apariencia'),
          _SettingsCard(
            children: [
              _ThemeSelector(
                currentMode: themeMode,
                onChanged: (mode) =>
                    ref.read(themeModeProvider.notifier).state = mode,
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.s4),

          // Accesibilidad
          _SectionHeader(title: 'Accesibilidad'),
          _SettingsCard(
            children: [
              ListTile(
                leading: const Icon(Icons.text_fields_rounded, size: 24),
                title: const Text('Tamaño de texto'),
                subtitle: const Text('Usa la configuración del sistema'),
                trailing: const Icon(Icons.open_in_new_rounded, size: 20),
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text(
                          'Ajusta el tamaño de texto en Ajustes > Accesibilidad del dispositivo'),
                    ),
                  );
                },
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.contrast_rounded, size: 24),
                title: const Text('Alto contraste'),
                subtitle: const Text(
                    'Diseñado para WCAG AAA — siempre activo'),
                trailing: Icon(
                  Icons.check_circle_rounded,
                  color: AppColors.success,
                  size: 20,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.s4),

          // Acerca de
          _SectionHeader(title: 'Acerca de'),
          _SettingsCard(
            children: [
              ListTile(
                leading: const Icon(Icons.info_outline_rounded, size: 24),
                title: const Text('Versión de la app'),
                trailing: Text(
                  '1.0.0',
                  style: AppTextStyles.bodySm.copyWith(
                    color: Theme.of(context)
                        .colorScheme
                        .onSurface
                        .withAlpha(153),
                  ),
                ),
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.sign_language_outlined, size: 24),
                title: const Text('Lengua de señas colombiana (LSC)'),
                subtitle:
                    const Text('Variante: co-csn'),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.s4),

          // Cerrar sesión
          if (isAuth) ...[
            _SectionHeader(title: 'Sesión'),
            _SettingsCard(
              children: [
                ListTile(
                  leading: const Icon(
                    Icons.logout_rounded,
                    size: 24,
                    color: AppColors.error,
                  ),
                  title: Text(
                    'Cerrar sesión',
                    style: AppTextStyles.body
                        .copyWith(color: AppColors.error),
                  ),
                  onTap: () => _showLogoutDialog(context, ref),
                ),
              ],
            ),
          ],

          const SizedBox(height: AppSpacing.s12),
        ],
      ),
    );
  }

  void _showLogoutDialog(BuildContext context, WidgetRef ref) {
    showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        shape: const RoundedRectangleBorder(
          borderRadius: AppRadius.borderXxl,
        ),
        title: const Text('Cerrar sesión'),
        content: const Text(
            '¿Estás seguro que quieres cerrar sesión?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.error,
              foregroundColor: AppColors.white,
              minimumSize: Size.zero,
              padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.s4, vertical: AppSpacing.s2),
            ),
            onPressed: () async {
              Navigator.of(context).pop();
              await ref.read(authStateProvider.notifier).logout();
              if (context.mounted) context.go(AppRoutes.home);
            },
            child: const Text('Cerrar sesión'),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Componentes internos de settings
// ---------------------------------------------------------------------------

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title});
  final String title;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(
        left: AppSpacing.s2,
        bottom: AppSpacing.s2,
      ),
      child: Text(
        title.toUpperCase(),
        style: AppTextStyles.overline.copyWith(
          color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
        ),
      ),
    );
  }
}

class _SettingsCard extends StatelessWidget {
  const _SettingsCard({required this.children});
  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: AppRadius.borderLg,
        border: Border.all(
          color: Theme.of(context).colorScheme.outline,
        ),
      ),
      clipBehavior: Clip.hardEdge,
      child: Column(children: children),
    );
  }
}

class _ProfileCard extends StatelessWidget {
  const _ProfileCard({required this.user});
  final dynamic user;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.s4),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: AppRadius.borderLg,
        border: Border.all(color: Theme.of(context).colorScheme.outline),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 28,
            backgroundColor: AppColors.primary.withAlpha(26),
            backgroundImage: user.avatarUrl != null
                ? NetworkImage(user.avatarUrl!)
                : null,
            child: user.avatarUrl == null
                ? Text(
                    user.nameOrEmail[0].toUpperCase(),
                    style: AppTextStyles.h3.copyWith(
                      color: AppColors.primary,
                    ),
                  )
                : null,
          ),
          const SizedBox(width: AppSpacing.s4),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  user.nameOrEmail,
                  style: AppTextStyles.h4.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
                Text(
                  user.email,
                  style: AppTextStyles.bodySm.copyWith(
                    color: Theme.of(context)
                        .colorScheme
                        .onSurface
                        .withAlpha(153),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _AuthCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.s4),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: AppRadius.borderLg,
        border: Border.all(color: Theme.of(context).colorScheme.outline),
      ),
      child: Row(
        children: [
          Icon(
            Icons.person_outline_rounded,
            size: 48,
            color: Theme.of(context).colorScheme.onSurface.withAlpha(77),
          ),
          const SizedBox(width: AppSpacing.s4),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'No has iniciado sesión',
                  style: AppTextStyles.h4.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
                const SizedBox(height: AppSpacing.s2),
                GestureDetector(
                  onTap: () => context.go(AppRoutes.login),
                  child: Text(
                    'Ingresar',
                    style: AppTextStyles.body.copyWith(
                      color: AppColors.primary,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ThemeSelector extends StatelessWidget {
  const _ThemeSelector({
    required this.currentMode,
    required this.onChanged,
  });

  final ThemeMode currentMode;
  final void Function(ThemeMode) onChanged;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s4,
        vertical: AppSpacing.s3,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.palette_outlined, size: 24),
              const SizedBox(width: AppSpacing.s3),
              Text('Tema', style: AppTextStyles.body),
            ],
          ),
          const SizedBox(height: AppSpacing.s3),
          SegmentedButton<ThemeMode>(
            selected: {currentMode},
            onSelectionChanged: (modes) => onChanged(modes.first),
            segments: const [
              ButtonSegment(
                value: ThemeMode.light,
                icon: Icon(Icons.light_mode_rounded, size: 18),
                label: Text('Claro'),
              ),
              ButtonSegment(
                value: ThemeMode.system,
                icon: Icon(Icons.brightness_auto_rounded, size: 18),
                label: Text('Auto'),
              ),
              ButtonSegment(
                value: ThemeMode.dark,
                icon: Icon(Icons.dark_mode_rounded, size: 18),
                label: Text('Oscuro'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
