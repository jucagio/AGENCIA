import 'api_service.dart';
import '../models/sign.dart';

class SignsService {
  final ApiService _api = ApiService();

  Future<SignsResponse> getSignsByCategory(String? category) async {
    final params = <String, dynamic>{};
    if (category != null && category != 'Todas') {
      params['category'] = category;
    }
    final data = await _api.get('/signs', queryParameters: params);
    return SignsResponse.fromJson(data as Map<String, dynamic>);
  }

  Future<SignsResponse> searchSigns(String query, {String? category}) async {
    final params = <String, dynamic>{'q': query};
    if (category != null) {
      params['category'] = category;
    }
    final data = await _api.get('/signs/search', queryParameters: params);
    return SignsResponse.fromJson(data as Map<String, dynamic>);
  }

  Future<Sign> getSignDetail(String id) async {
    final data = await _api.get('/signs/$id');
    return Sign.fromJson(data as Map<String, dynamic>);
  }

  Future<SignsResponse> getRelatedSigns(String id) async {
    final data =
        await _api.get('/signs/$id/related', queryParameters: {'limit': 6});
    return SignsResponse.fromJson(data as Map<String, dynamic>);
  }

  Future<List<String>> getCategories() async {
    final data = await _api.get('/categories');
    return List<String>.from(data as List);
  }
}
