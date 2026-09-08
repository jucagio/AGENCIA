import 'package:flutter/material.dart';
import '../models/sign.dart';
import '../config/theme.dart';

class SignCard extends StatelessWidget {
  final Sign sign;
  final VoidCallback onTap;

  const SignCard({
    Key? key,
    required this.sign,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 165,
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(AppRadius.lg),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.07),
              blurRadius: 6,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Video thumbnail
            Container(
              width: double.infinity,
              height: 120,
              decoration: BoxDecoration(
                color: AppColors.light200,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(AppRadius.lg),
                  topRight: Radius.circular(AppRadius.lg),
                ),
              ),
              child: sign.thumbnailUrl != null
                  ? Image.network(
                      sign.thumbnailUrl!,
                      fit: BoxFit.cover,
                    )
                  : const Center(
                      child: Icon(Icons.play_circle_outline),
                    ),
            ),
            // Content area
            Padding(
              padding: const EdgeInsets.all(AppSpacing.s3),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Sign name
                  Text(
                    sign.name,
                    style: AppTypography.h4.copyWith(
                      color: Theme.of(context).brightness == Brightness.light
                          ? AppColors.dark900
                          : Color(0xFFF9FAFB),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: AppSpacing.s2),
                  // Difficulty dots
                  Row(
                    children: List.generate(
                      5,
                      (index) => Container(
                        width: 8,
                        height: 8,
                        margin: const EdgeInsets.only(right: AppSpacing.s1),
                        decoration: BoxDecoration(
                          color: index < sign.difficulty
                              ? AppColors.primary
                              : AppColors.light200,
                          shape: BoxShape.circle,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
