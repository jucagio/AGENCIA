import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../config/theme.dart';
import '../providers/signs_provider.dart';
import '../widgets/sign_card.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final categories = ref.watch(categoriesProvider);
    final signs = ref.watch(signsProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Teclado de Señas'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => context.go('/settings'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Search bar
            Padding(
              padding: const EdgeInsets.all(AppSpacing.s4),
              child: GestureDetector(
                onTap: () => context.go('/search'),
                child: TextField(
                  enabled: false,
                  decoration: InputDecoration(
                    hintText: 'Busca una seña...',
                    prefixIcon: const Icon(Icons.search),
                    filled: true,
                  ),
                ),
              ),
            ),
            // Categories
            categories.when(
              data: (cats) => SizedBox(
                height: 48,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.s4,
                  ),
                  itemCount: cats.length,
                  itemBuilder: (context, index) {
                    final category = cats[index];
                    final isSelected = selectedCategory == category;
                    return Padding(
                      padding: const EdgeInsets.only(right: AppSpacing.s2),
                      child: FilterChip(
                        label: Text(category),
                        selected: isSelected,
                        onSelected: (_) {
                          ref
                              .read(selectedCategoryProvider.notifier)
                              .state = category;
                        },
                      ),
                    );
                  },
                ),
              ),
              loading: () => const SizedBox(height: 48),
              error: (_, __) => const SizedBox(height: 48),
            ),
            const SizedBox(height: AppSpacing.s4),
            // Signs grid
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.s4,
              ),
              child: signs.when(
                data: (response) => GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: AppSpacing.s3,
                    crossAxisSpacing: AppSpacing.s3,
                    childAspectRatio: 165 / 180,
                  ),
                  itemCount: response.signs.length,
                  itemBuilder: (context, index) {
                    final sign = response.signs[index];
                    return SignCard(
                      sign: sign,
                      onTap: () => context.go('/sign/${sign.id}'),
                    );
                  },
                ),
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),
                error: (error, _) => Center(
                  child: Text('Error: $error'),
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Inicio'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Buscar'),
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite_border),
            label: 'Favoritos',
          ),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Config'),
        ],
        onTap: (index) {
          switch (index) {
            case 0:
              context.go('/home');
              break;
            case 1:
              context.go('/search');
              break;
            case 2:
              context.go('/favorites');
              break;
            case 3:
              context.go('/settings');
              break;
          }
        },
      ),
    );
  }
}
