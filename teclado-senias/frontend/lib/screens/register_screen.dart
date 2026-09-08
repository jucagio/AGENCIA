/// Pantalla de registro — POST /auth/register
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../config/routes.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();
  bool _obscurePassword = true;
  bool _obscureConfirm = true;
  bool _isLoading = false;
  String? _errorMessage;
  Map<String, String> _fieldErrors = {};

  @override
  void dispose() {
    _nameCtrl.dispose();
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    _confirmCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() => _fieldErrors = {});
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await ref.read(authStateProvider.notifier).register(
            email: _emailCtrl.text.trim(),
            password: _passwordCtrl.text,
            name: _nameCtrl.text.trim(),
          );
      if (mounted) context.go(AppRoutes.home);
    } on ApiException catch (e) {
      setState(() {
        if (e.fields != null && e.fields!.isNotEmpty) {
          _fieldErrors = e.fields!;
        } else {
          _errorMessage = e.message;
        }
      });
    } catch (_) {
      setState(
          () => _errorMessage = 'Ocurrió un error inesperado. Intenta de nuevo.');
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crear cuenta'),
        leading: BackButton(
          onPressed: () => context.go(AppRoutes.login),
        ),
      ),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.s4,
              vertical: AppSpacing.s6,
            ),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 480),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Crea tu cuenta',
                    style: AppTextStyles.h1.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: AppSpacing.s2),
                  Text(
                    'Accede a favoritos y traducciones personalizadas',
                    style: AppTextStyles.body.copyWith(
                      color: Theme.of(context)
                          .colorScheme
                          .onSurface
                          .withAlpha(153),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: AppSpacing.s6),

                  if (_errorMessage != null) _ErrorBanner(message: _errorMessage!),

                  Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Nombre
                        _FieldLabel(text: 'Nombre completo'),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _nameCtrl,
                          keyboardType: TextInputType.name,
                          textCapitalization: TextCapitalization.words,
                          textInputAction: TextInputAction.next,
                          autofillHints: const [AutofillHints.name],
                          style: AppTextStyles.body,
                          decoration: InputDecoration(
                            hintText: 'María López',
                            prefixIcon: const Icon(Icons.person_outline_rounded, size: 20),
                            errorText: _fieldErrors['name'],
                          ),
                          validator: (v) {
                            if (v == null || v.trim().isEmpty) {
                              return 'El nombre es requerido';
                            }
                            if (v.trim().length < 2) {
                              return 'El nombre debe tener al menos 2 caracteres';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: AppSpacing.s5),

                        // Email
                        _FieldLabel(text: 'Correo electrónico'),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _emailCtrl,
                          keyboardType: TextInputType.emailAddress,
                          textInputAction: TextInputAction.next,
                          autocorrect: false,
                          autofillHints: const [AutofillHints.newUsername],
                          style: AppTextStyles.body,
                          decoration: InputDecoration(
                            hintText: 'tu@correo.com',
                            prefixIcon: const Icon(Icons.mail_outline_rounded, size: 20),
                            errorText: _fieldErrors['email'],
                          ),
                          validator: (v) {
                            if (v == null || v.trim().isEmpty) {
                              return 'El correo es requerido';
                            }
                            if (!v.contains('@') || !v.contains('.')) {
                              return 'Ingresa un correo válido';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: AppSpacing.s5),

                        // Contraseña
                        _FieldLabel(text: 'Contraseña'),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _passwordCtrl,
                          obscureText: _obscurePassword,
                          textInputAction: TextInputAction.next,
                          autofillHints: const [AutofillHints.newPassword],
                          style: AppTextStyles.body,
                          decoration: InputDecoration(
                            hintText: '••••••••',
                            prefixIcon: const Icon(Icons.lock_outline_rounded, size: 20),
                            helperText:
                                'Mínimo 8 caracteres, 1 mayúscula y 1 número',
                            errorText: _fieldErrors['password'],
                            suffixIcon: GestureDetector(
                              behavior: HitTestBehavior.opaque,
                              onTap: () => setState(
                                  () => _obscurePassword = !_obscurePassword),
                              child: Padding(
                                padding: const EdgeInsets.all(10),
                                child: Icon(
                                  _obscurePassword
                                      ? Icons.visibility_outlined
                                      : Icons.visibility_off_outlined,
                                  size: 20,
                                  semanticLabel: _obscurePassword
                                      ? 'Mostrar contraseña'
                                      : 'Ocultar contraseña',
                                ),
                              ),
                            ),
                          ),
                          validator: (v) {
                            if (v == null || v.isEmpty) {
                              return 'La contraseña es requerida';
                            }
                            if (v.length < 8) {
                              return 'Mínimo 8 caracteres';
                            }
                            if (!v.contains(RegExp(r'[A-Z]'))) {
                              return 'Debe contener al menos una mayúscula';
                            }
                            if (!v.contains(RegExp(r'[0-9]'))) {
                              return 'Debe contener al menos un número';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: AppSpacing.s5),

                        // Confirmar contraseña
                        _FieldLabel(text: 'Confirmar contraseña'),
                        const SizedBox(height: 6),
                        TextFormField(
                          controller: _confirmCtrl,
                          obscureText: _obscureConfirm,
                          textInputAction: TextInputAction.done,
                          autofillHints: const [AutofillHints.newPassword],
                          style: AppTextStyles.body,
                          onFieldSubmitted: (_) => _submit(),
                          decoration: InputDecoration(
                            hintText: '••••••••',
                            prefixIcon: const Icon(Icons.lock_outline_rounded, size: 20),
                            suffixIcon: GestureDetector(
                              behavior: HitTestBehavior.opaque,
                              onTap: () => setState(
                                  () => _obscureConfirm = !_obscureConfirm),
                              child: Padding(
                                padding: const EdgeInsets.all(10),
                                child: Icon(
                                  _obscureConfirm
                                      ? Icons.visibility_outlined
                                      : Icons.visibility_off_outlined,
                                  size: 20,
                                ),
                              ),
                            ),
                          ),
                          validator: (v) {
                            if (v != _passwordCtrl.text) {
                              return 'Las contraseñas no coinciden';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: AppSpacing.s8),

                        ElevatedButton(
                          onPressed: _isLoading ? null : _submit,
                          child: _isLoading
                              ? const SizedBox(
                                  height: 20,
                                  width: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2.5,
                                    valueColor: AlwaysStoppedAnimation<Color>(
                                        AppColors.white),
                                  ),
                                )
                              : const Text('Crear cuenta'),
                        ),
                        const SizedBox(height: AppSpacing.s4),

                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              '¿Ya tienes cuenta? ',
                              style: AppTextStyles.body.copyWith(
                                color: Theme.of(context)
                                    .colorScheme
                                    .onSurface
                                    .withAlpha(153),
                              ),
                            ),
                            TextButton(
                              onPressed: () => context.go(AppRoutes.login),
                              child: const Text('Inicia sesión'),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _FieldLabel extends StatelessWidget {
  const _FieldLabel({required this.text});
  final String text;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: AppTextStyles.label.copyWith(
        color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
      ),
    );
  }
}

class _ErrorBanner extends StatelessWidget {
  const _ErrorBanner({required this.message});
  final String message;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppSpacing.s5),
      padding: const EdgeInsets.all(AppSpacing.s4),
      decoration: BoxDecoration(
        color: AppColors.errorBg,
        borderRadius: AppRadius.borderMd,
        border: Border.all(color: AppColors.error.withAlpha(77)),
      ),
      child: Row(
        children: [
          const Icon(Icons.error_outline_rounded,
              size: 20, color: AppColors.error),
          const SizedBox(width: AppSpacing.s2),
          Expanded(
            child: Text(
              message,
              style: AppTextStyles.bodySm.copyWith(color: AppColors.error),
            ),
          ),
        ],
      ),
    );
  }
}
