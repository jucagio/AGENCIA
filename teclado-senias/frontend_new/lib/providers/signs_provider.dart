import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/signs_service.dart';
import '../models/sign.dart';

final signsServiceProvider = Provider((ref) => SignsService());

final categoriesProvider = FutureProvider<List<String>>((ref) async {
  final signsService = ref.watch(signsServiceProvider);
  final categories = await signsService.getCategories();
  return ['Todas', ...categories];
});

final selectedCategoryProvider = StateProvider<String>((ref) => 'Todas');

final signsProvider = FutureProvider<SignsResponse>((ref) async {
  final signsService = ref.watch(signsServiceProvider);
  final category = ref.watch(selectedCategoryProvider);
  return signsService.getSignsByCategory(
    category == 'Todas' ? null : category,
  );
});

final searchQueryProvider = StateProvider<String>((ref) => '');

final searchResultsProvider = FutureProvider<SignsResponse>((ref) async {
  final query = ref.watch(searchQueryProvider);
  if (query.isEmpty) {
    return SignsResponse(signs: [], total: 0);
  }
  final signsService = ref.watch(signsServiceProvider);
  final category = ref.watch(selectedCategoryProvider);
  return signsService.searchSigns(
    query,
    category: category == 'Todas' ? null : category,
  );
});

final signDetailProvider = FutureProvider.family<Sign, String>((ref, id) async {
  final signsService = ref.watch(signsServiceProvider);
  return signsService.getSignDetail(id);
});

final relatedSignsProvider =
    FutureProvider.family<SignsResponse, String>((ref, id) async {
  final signsService = ref.watch(signsServiceProvider);
  return signsService.getRelatedSigns(id);
});
