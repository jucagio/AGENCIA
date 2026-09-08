import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';
import 'package:asesor_imagen_ai/features/wardrobe/data/wardrobe_repository.dart';

const _itemTypes = [
  'shirt',
  'pants',
  'dress',
  'jacket',
  'skirt',
  'shoes',
  'accessory',
];

const _typeLabels = {
  'shirt': 'Camisa / Camiseta',
  'pants': 'Pantalon',
  'dress': 'Vestido',
  'jacket': 'Blazer / Chaqueta',
  'skirt': 'Falda',
  'shoes': 'Zapatos',
  'accessory': 'Accesorio',
};

class WardrobeScreen extends ConsumerWidget {
  const WardrobeScreen({super.key});

  static const routeName = '/wardrobe';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final wardrobeAsync = ref.watch(wardrobeProvider);

    return Scaffold(
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(24, 24, 24, 16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Mi Armario',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.w700,
                          ),
                    ),
                    FilledButton.icon(
                      onPressed: () => _showAddItemModal(context, ref),
                      style: FilledButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                        ),
                      ),
                      icon: const Icon(Icons.add, size: 18),
                      label: const Text('Agregar'),
                    ),
                  ],
                ),
              ),
            ),
            wardrobeAsync.when(
              loading: () => const SliverFillRemaining(
                child: Center(child: CircularProgressIndicator()),
              ),
              error: (e, _) => SliverFillRemaining(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error_outline, size: 48, color: AppColors.error),
                      const SizedBox(height: 8),
                      Text('Error al cargar el armario'),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: () => ref.read(wardrobeProvider.notifier).fetchItems(),
                        child: const Text('Reintentar'),
                      ),
                    ],
                  ),
                ),
              ),
              data: (items) => items.isEmpty
                  ? SliverFillRemaining(
                      child: _EmptyWardrobe(
                        onAdd: () => _showAddItemModal(context, ref),
                      ),
                    )
                  : SliverPadding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      sliver: SliverGrid(
                        gridDelegate:
                            const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          crossAxisSpacing: 12,
                          mainAxisSpacing: 12,
                          childAspectRatio: 0.85,
                        ),
                        delegate: SliverChildBuilderDelegate(
                          (context, index) {
                            final item = items[index];
                            return _WardrobeCard(
                              item: item,
                              onDelete: () => ref
                                  .read(wardrobeProvider.notifier)
                                  .deleteItem(item.id),
                            );
                          },
                          childCount: items.length,
                        ),
                      ),
                    ),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 24)),
          ],
        ),
      ),
    );
  }

  void _showAddItemModal(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(DesignTokens.radiusXLarge),
        ),
      ),
      builder: (ctx) => _AddItemSheet(
        onSave: (name, type, color, imagePath) async {
          await ref.read(wardrobeProvider.notifier).addItem(
                name: name,
                type: type,
                color: color,
                imageUrl: imagePath,
              );
          if (ctx.mounted) Navigator.pop(ctx);
        },
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Sub-widgets
// ---------------------------------------------------------------------------

class _WardrobeCard extends StatelessWidget {
  const _WardrobeCard({required this.item, required this.onDelete});
  final WardrobeItem item;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
      ),
      child: Stack(
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image / color placeholder
              Expanded(
                child: ClipRRect(
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(DesignTokens.radiusLarge),
                  ),
                  child: item.imageUrl != null && item.imageUrl!.isNotEmpty
                      ? Image.network(item.imageUrl!, fit: BoxFit.cover)
                      : Container(
                          color: _parseColor(item.color),
                          child: Icon(
                            _typeIcon(item.type),
                            size: 48,
                            color: Colors.white.withOpacity(0.7),
                          ),
                        ),
                ),
              ),
              // Info
              Padding(
                padding: const EdgeInsets.all(10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.name,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                          ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      _typeLabels[item.type] ?? item.type,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: Colors.grey[500],
                          ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          // Delete button
          Positioned(
            top: 8,
            right: 8,
            child: GestureDetector(
              onTap: () => _confirmDelete(context),
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.9),
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 4,
                    )
                  ],
                ),
                child: Icon(Icons.close, size: 16, color: AppColors.error),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _confirmDelete(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
        ),
        title: const Text('Eliminar prenda'),
        content: Text('Eliminar "${item.name}" de tu armario?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: AppColors.error),
            onPressed: () {
              Navigator.pop(ctx);
              onDelete();
            },
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
  }

  Color _parseColor(String? hex) {
    if (hex == null) return Colors.grey[400]!;
    try {
      return Color(int.parse('FF${hex.replaceAll('#', '')}', radix: 16));
    } catch (_) {
      return Colors.grey[400]!;
    }
  }

  IconData _typeIcon(String type) {
    switch (type) {
      case 'shoes':
        return Icons.directions_walk;
      case 'accessory':
        return Icons.watch;
      default:
        return Icons.checkroom;
    }
  }
}

class _EmptyWardrobe extends StatelessWidget {
  const _EmptyWardrobe({required this.onAdd});
  final VoidCallback onAdd;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(40),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.checkroom_outlined, size: 72, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text(
              'Tu armario esta vacio',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: Colors.grey[600],
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              'Agrega tus prendas para empezar a generar outfits',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[500],
                  ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: onAdd,
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.primary,
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                ),
              ),
              icon: const Icon(Icons.add),
              label: const Text('Agregar primera prenda'),
            ),
          ],
        ),
      ),
    );
  }
}

class _AddItemSheet extends StatefulWidget {
  const _AddItemSheet({required this.onSave});

  final Future<void> Function(
    String name,
    String type,
    String? color,
    String? imagePath,
  ) onSave;

  @override
  State<_AddItemSheet> createState() => _AddItemSheetState();
}

class _AddItemSheetState extends State<_AddItemSheet> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  String _selectedType = 'shirt';
  String? _imagePath;
  bool _isSaving = false;

  @override
  void dispose() {
    _nameCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickImage(ImageSource source) async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: source, imageQuality: 80);
    if (picked != null) setState(() => _imagePath = picked.path);
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isSaving = true);
    await widget.onSave(_nameCtrl.text.trim(), _selectedType, null, _imagePath);
    if (mounted) setState(() => _isSaving = false);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 24,
        right: 24,
        top: 24,
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
      ),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Handle
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              'Nueva prenda',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 20),

            // Image picker
            GestureDetector(
              onTap: () => _showImageSourcePicker(),
              child: Container(
                height: 100,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                  border: Border.all(
                    color: AppColors.primary.withOpacity(0.2),
                    style: BorderStyle.solid,
                  ),
                ),
                child: _imagePath != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                        child: Image.file(File(_imagePath!), fit: BoxFit.cover),
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.add_photo_alternate_outlined,
                              color: AppColors.primary, size: 28),
                          const SizedBox(height: 4),
                          Text('Foto de la prenda (opcional)',
                              style: TextStyle(
                                  color: Colors.grey[500], fontSize: 12)),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 16),

            // Name
            TextFormField(
              controller: _nameCtrl,
              textCapitalization: TextCapitalization.words,
              decoration: InputDecoration(
                labelText: 'Nombre de la prenda',
                hintText: 'Ej: Camisa blanca de lino',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                ),
                filled: true,
              ),
              validator: (v) =>
                  (v == null || v.isEmpty) ? 'Ingresa un nombre' : null,
            ),
            const SizedBox(height: 16),

            // Type dropdown
            DropdownButtonFormField<String>(
              initialValue: _selectedType,
              decoration: InputDecoration(
                labelText: 'Tipo de prenda',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                ),
                filled: true,
              ),
              borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
              items: _itemTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(_typeLabels[type] ?? type),
                );
              }).toList(),
              onChanged: (v) {
                if (v != null) setState(() => _selectedType = v);
              },
            ),
            const SizedBox(height: 24),

            // Save
            SizedBox(
              height: 52,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: AppColors.primaryGradient,
                  borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                ),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.transparent,
                    shadowColor: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                    ),
                  ),
                  onPressed: _isSaving ? null : _submit,
                  child: _isSaving
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : const Text(
                          'Guardar prenda',
                          style: TextStyle(
                              color: Colors.white, fontWeight: FontWeight.w600),
                        ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showImageSourcePicker() {
    showModalBottomSheet(
      context: context,
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt_outlined),
              title: const Text('Camara'),
              onTap: () {
                Navigator.pop(ctx);
                _pickImage(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_outlined),
              title: const Text('Galeria'),
              onTap: () {
                Navigator.pop(ctx);
                _pickImage(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }
}
