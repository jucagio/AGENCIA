/// AppShell — Scaffold con Bottom Navigation Bar
/// Implementa las especificaciones de bottom nav del design system de Erik.
/// Height: 80px, 4 items, active indicator de 32x3px.
library;

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../config/routes.dart';
import '../config/theme.dart';

class AppShell extends StatelessWidget {
  const AppShell({super.key, required this.child});

  final Widget child;

  static const _tabs = [
    _TabItem(
      route: AppRoutes.home,
      label: 'Inicio',
      icon: Icons.home_outlined,
      activeIcon: Icons.home_rounded,
    ),
    _TabItem(
      route: AppRoutes.search,
      label: 'Buscar',
      icon: Icons.search_rounded,
      activeIcon: Icons.search_rounded,
    ),
    _TabItem(
      route: AppRoutes.favorites,
      label: 'Favoritos',
      icon: Icons.favorite_border_rounded,
      activeIcon: Icons.favorite_rounded,
    ),
    _TabItem(
      route: AppRoutes.settings,
      label: 'Ajustes',
      icon: Icons.settings_outlined,
      activeIcon: Icons.settings_rounded,
    ),
  ];

  int _currentIndex(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    for (int i = 0; i < _tabs.length; i++) {
      if (location.startsWith(_tabs[i].route)) return i;
    }
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    final currentIndex = _currentIndex(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: child,
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: isDark ? AppColors.dark800 : AppColors.white,
          border: Border(
            top: BorderSide(
              color: isDark ? AppColors.dark700 : AppColors.light200,
              width: 1,
            ),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withAlpha(13),
              blurRadius: 12,
              offset: const Offset(0, -4),
            ),
          ],
        ),
        child: SafeArea(
          top: false,
          child: SizedBox(
            height: 64,
            child: Row(
              children: List.generate(_tabs.length, (index) {
                return Expanded(
                  child: _NavItem(
                    tab: _tabs[index],
                    isActive: currentIndex == index,
                    onTap: () {
                      if (currentIndex != index) {
                        context.go(_tabs[index].route);
                      }
                    },
                  ),
                );
              }),
            ),
          ),
        ),
      ),
    );
  }
}

class _TabItem {
  const _TabItem({
    required this.route,
    required this.label,
    required this.icon,
    required this.activeIcon,
  });

  final String route;
  final String label;
  final IconData icon;
  final IconData activeIcon;
}

class _NavItem extends StatelessWidget {
  const _NavItem({
    required this.tab,
    required this.isActive,
    required this.onTap,
  });

  final _TabItem tab;
  final bool isActive;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final activeColor = isDark ? AppColors.primaryDark : AppColors.primary;
    final inactiveColor = AppColors.dark500;
    final color = isActive ? activeColor : inactiveColor;

    return Semantics(
      label: '${tab.label}${isActive ? ", pantalla actual" : ""}',
      button: true,
      selected: isActive,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Active indicator
            AnimatedContainer(
              duration: AppDurations.fast,
              width: isActive ? 32 : 0,
              height: 3,
              margin: const EdgeInsets.only(bottom: 6),
              decoration: BoxDecoration(
                color: activeColor,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            Icon(
              isActive ? tab.activeIcon : tab.icon,
              size: 24,
              color: color,
            ),
            const SizedBox(height: 4),
            Text(
              tab.label,
              style: AppTextStyles.label.copyWith(color: color),
            ),
          ],
        ),
      ),
    );
  }
}
