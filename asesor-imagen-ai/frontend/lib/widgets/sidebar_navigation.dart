import 'package:flutter/material.dart';
import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';

// ---------------------------------------------------------------------------
// Sidebar Navigation — diseño Stitch validado por Erik
// Muestra items verticales con ítem activo resaltado en azul #0058BE
// En mobile: se usa como NavigationRail colapsado.
// ---------------------------------------------------------------------------

enum SidebarItem {
  virtualTryOn,
  myWardrobe,
  styleInsights,
  collections,
}

class SidebarNavigation extends StatelessWidget {
  const SidebarNavigation({
    super.key,
    required this.selectedItem,
    required this.onItemSelected,
    this.collapsed = false,
  });

  final SidebarItem selectedItem;
  final ValueChanged<SidebarItem> onItemSelected;
  final bool collapsed;

  static const _primaryBlue = Color(0xFF0058BE);
  static const _inactiveGrey = Color(0xFF6B7280);
  static const _activeBg = Color(0xFFEBF2FF);

  static const _items = [
    _SidebarItemDef(
      item: SidebarItem.virtualTryOn,
      icon: Icons.auto_awesome_outlined,
      activeIcon: Icons.auto_awesome,
      label: 'Virtual Try-On',
    ),
    _SidebarItemDef(
      item: SidebarItem.myWardrobe,
      icon: Icons.checkroom_outlined,
      activeIcon: Icons.checkroom,
      label: 'My Wardrobe',
    ),
    _SidebarItemDef(
      item: SidebarItem.styleInsights,
      icon: Icons.bar_chart_outlined,
      activeIcon: Icons.bar_chart,
      label: 'Style Insights',
    ),
    _SidebarItemDef(
      item: SidebarItem.collections,
      icon: Icons.collections_bookmark_outlined,
      activeIcon: Icons.collections_bookmark,
      label: 'Collections',
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      width: collapsed ? 64 : 200,
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(
          right: BorderSide(color: Colors.grey.shade200, width: 1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Logo area
          Padding(
            padding: EdgeInsets.fromLTRB(
              collapsed ? 12 : 20,
              24,
              collapsed ? 12 : 20,
              16,
            ),
            child: collapsed
                ? ShaderMask(
                    shaderCallback: (bounds) =>
                        AppColors.primaryGradient.createShader(bounds),
                    child: const Icon(Icons.auto_awesome,
                        size: 28, color: Colors.white),
                  )
                : Row(
                    children: [
                      ShaderMask(
                        shaderCallback: (bounds) =>
                            AppColors.primaryGradient.createShader(bounds),
                        child: const Icon(Icons.auto_awesome,
                            size: 22, color: Colors.white),
                      ),
                      const SizedBox(width: 8),
                      const Text(
                        'StyleAI',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF0058BE),
                        ),
                      ),
                    ],
                  ),
          ),

          const SizedBox(height: 8),

          // Nav items
          Expanded(
            child: ListView(
              padding: EdgeInsets.symmetric(
                horizontal: collapsed ? 8 : 12,
                vertical: 0,
              ),
              children: _items.map((def) {
                final isActive = selectedItem == def.item;
                return _SidebarNavItem(
                  def: def,
                  isActive: isActive,
                  collapsed: collapsed,
                  primaryBlue: _primaryBlue,
                  inactiveGrey: _inactiveGrey,
                  activeBg: _activeBg,
                  onTap: () => onItemSelected(def.item),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}

class _SidebarNavItem extends StatelessWidget {
  const _SidebarNavItem({
    required this.def,
    required this.isActive,
    required this.collapsed,
    required this.primaryBlue,
    required this.inactiveGrey,
    required this.activeBg,
    required this.onTap,
  });

  final _SidebarItemDef def;
  final bool isActive;
  final bool collapsed;
  final Color primaryBlue;
  final Color inactiveGrey;
  final Color activeBg;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            padding: EdgeInsets.symmetric(
              horizontal: collapsed ? 8 : 12,
              vertical: 10,
            ),
            decoration: BoxDecoration(
              color: isActive ? activeBg : Colors.transparent,
              borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
            ),
            child: collapsed
                ? Center(
                    child: Icon(
                      isActive ? def.activeIcon : def.icon,
                      size: 20,
                      color: isActive ? primaryBlue : inactiveGrey,
                    ),
                  )
                : Row(
                    children: [
                      Icon(
                        isActive ? def.activeIcon : def.icon,
                        size: 18,
                        color: isActive ? primaryBlue : inactiveGrey,
                      ),
                      const SizedBox(width: 10),
                      Text(
                        def.label,
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: isActive ? FontWeight.w600 : FontWeight.w400,
                          color: isActive ? primaryBlue : inactiveGrey,
                        ),
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}

class _SidebarItemDef {
  const _SidebarItemDef({
    required this.item,
    required this.icon,
    required this.activeIcon,
    required this.label,
  });

  final SidebarItem item;
  final IconData icon;
  final IconData activeIcon;
  final String label;
}
