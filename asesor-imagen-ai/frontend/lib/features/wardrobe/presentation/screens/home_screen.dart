import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';
import 'package:asesor_imagen_ai/features/try_on/presentation/screens/try_on_screen.dart';
import 'package:asesor_imagen_ai/features/body_analysis/presentation/screens/body_analysis_screen.dart';
import 'package:asesor_imagen_ai/features/wardrobe/presentation/screens/wardrobe_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/profile_screen.dart';

// ---------------------------------------------------------------------------
// Shell screen — holds BottomNavigationBar + persistent auth state
// ---------------------------------------------------------------------------

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  static const routeName = '/home';

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  int _currentIndex = 0;

  static const _tabs = [
    _TabDef(label: 'Try-On', icon: Icons.auto_awesome_outlined, activeIcon: Icons.auto_awesome),
    _TabDef(label: 'Analisis', icon: Icons.person_search_outlined, activeIcon: Icons.person_search),
    _TabDef(label: 'Armario', icon: Icons.checkroom_outlined, activeIcon: Icons.checkroom),
    _TabDef(label: 'Perfil', icon: Icons.account_circle_outlined, activeIcon: Icons.account_circle),
  ];

  late final List<Widget> _screens = [
    const TryOnScreen(),
    const BodyAnalysisScreen(),
    const WardrobeScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        backgroundColor: Theme.of(context).colorScheme.surface,
        elevation: 0,
        indicatorColor: AppColors.primary.withOpacity(0.12),
        destinations: _tabs.map((tab) {
          return NavigationDestination(
            icon: Icon(tab.icon),
            selectedIcon: Icon(tab.activeIcon, color: AppColors.primary),
            label: tab.label,
          );
        }).toList(),
      ),
    );
  }
}

class _TabDef {
  const _TabDef({
    required this.label,
    required this.icon,
    required this.activeIcon,
  });
  final String label;
  final IconData icon;
  final IconData activeIcon;
}
