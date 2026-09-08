import 'package:freezed_annotation/freezed_annotation.dart';

part 'sign.freezed.dart';
part 'sign.g.dart';

@freezed
class Sign with _$Sign {
  const factory Sign({
    required String id,
    required String name,
    required String? description,
    required String videoUrl,
    required String? thumbnailUrl,
    required String category,
    required int difficulty, // 1-5
    required DateTime createdAt,
  }) = _Sign;

  factory Sign.fromJson(Map<String, dynamic> json) => _$SignFromJson(json);
}

@freezed
class SignsResponse with _$SignsResponse {
  const factory SignsResponse({
    required List<Sign> signs,
    required int total,
  }) = _SignsResponse;

  factory SignsResponse.fromJson(Map<String, dynamic> json) =>
      _$SignsResponseFromJson(json);
}
