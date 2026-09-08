/// SearchBarWidget — barra de búsqueda según especificaciones de Erik
/// Height: 52px, border radius xl (16px), background light-100
library;

import 'dart:async';
import 'package:flutter/material.dart';
import '../config/constants.dart';
import '../config/theme.dart';

class AppSearchBar extends StatefulWidget {
  const AppSearchBar({
    super.key,
    this.initialValue = '',
    this.onChanged,
    this.onSubmitted,
    this.onClear,
    this.hintText = 'Buscar señas...',
    this.autofocus = false,
    this.enabled = true,
  });

  final String initialValue;
  final void Function(String query)? onChanged;
  final void Function(String query)? onSubmitted;
  final VoidCallback? onClear;
  final String hintText;
  final bool autofocus;
  final bool enabled;

  @override
  State<AppSearchBar> createState() => _AppSearchBarState();
}

class _AppSearchBarState extends State<AppSearchBar> {
  late TextEditingController _controller;
  Timer? _debounce;
  bool _hasText = false;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.initialValue);
    _hasText = widget.initialValue.isNotEmpty;
    _controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    _debounce?.cancel();
    _controller.removeListener(_onTextChanged);
    _controller.dispose();
    super.dispose();
  }

  void _onTextChanged() {
    final text = _controller.text;
    setState(() => _hasText = text.isNotEmpty);

    if (widget.onChanged == null) return;

    _debounce?.cancel();
    _debounce = Timer(
      const Duration(milliseconds: AppConstants.searchDebounceMsec),
      () {
        if (mounted) widget.onChanged!(text);
      },
    );
  }

  void _clear() {
    _controller.clear();
    widget.onClear?.call();
    widget.onChanged?.call('');
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark ? AppColors.dark700 : AppColors.light100;
    final textColor = isDark ? const Color(0xFFF9FAFB) : AppColors.dark900;
    final hintColor = AppColors.dark500;
    final iconColor = AppColors.dark500;

    return Semantics(
      label: widget.hintText,
      textField: true,
      child: SizedBox(
        height: 52,
        child: TextField(
          controller: _controller,
          autofocus: widget.autofocus,
          enabled: widget.enabled,
          textInputAction: TextInputAction.search,
          onSubmitted: widget.onSubmitted,
          style: AppTextStyles.body.copyWith(color: textColor),
          decoration: InputDecoration(
            hintText: widget.hintText,
            hintStyle: AppTextStyles.body.copyWith(color: hintColor),
            filled: true,
            fillColor: bgColor,
            contentPadding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.s4,
              vertical: 0,
            ),
            border: OutlineInputBorder(
              borderRadius: AppRadius.borderXl,
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: AppRadius.borderXl,
              borderSide: BorderSide.none,
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: AppRadius.borderXl,
              borderSide: const BorderSide(
                color: AppColors.primary,
                width: 1.5,
              ),
            ),
            prefixIcon: Padding(
              padding: const EdgeInsets.only(left: 16, right: 8),
              child: Icon(
                Icons.search_rounded,
                size: 20,
                color: iconColor,
                semanticLabel: 'Buscar',
              ),
            ),
            prefixIconConstraints: const BoxConstraints(
              minWidth: 44,
              minHeight: 44,
            ),
            suffixIcon: _hasText
                ? GestureDetector(
                    behavior: HitTestBehavior.opaque,
                    onTap: _clear,
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: Icon(
                        Icons.close_rounded,
                        size: 20,
                        color: iconColor,
                        semanticLabel: 'Limpiar búsqueda',
                      ),
                    ),
                  )
                : null,
            suffixIconConstraints: const BoxConstraints(
              minWidth: 44,
              minHeight: 44,
            ),
          ),
        ),
      ),
    );
  }
}
