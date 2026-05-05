# Mockup 02 — Login / Register
**Viewport:** 375x812px | **Supabase Auth: email + Google + Apple**

---

## Login Screen

```
┌─────────────────────────────────────┐
│ ←                                   │  ← Back nav (si viene de onboarding)
│                                     │
│                                     │
│                                     │
│  Bienvenida de vuelta               │  ← Playfair Display 40px bold
│                                     │     neutral.900 / neutral.50
│  Continúa donde lo dejaste.         │  ← Plus Jakarta 16px, neutral.500
│                                     │
│                                     │  ← Espacio 32px
│                                     │
│  ┌─────────────────────────────┐    │  ← Input: Email
│  │ ✉  Correo electrónico       │    │     outlined variant
│  │                             │    │     height: 52px
│  └─────────────────────────────┘    │     leading icon: mail (20px)
│                                     │
│  ┌─────────────────────────────┐    │  ← Input: Password
│  │ 🔒  Contraseña              │    │     trailing icon: eye toggle
│  │                         👁  │    │     
│  └─────────────────────────────┘    │
│                                     │
│  ¿Olvidaste tu contraseña?          │  ← Alineado a la derecha
│                                     │     Plus Jakarta 14px, primary.500
│                                     │     tappable, ghost
│  ┌─────────────────────────────┐    │
│  │         Iniciar sesión      │    │  ← Button primary large (56px)
│  └─────────────────────────────┘    │     full width
│                                     │
│  ─────────── o continúa con ──────  │  ← Divider con texto
│                                     │     neutral.300 + neutral.500 text
│                                     │
│  ┌──────────────────────────┐       │  ← Google SSO button
│  │  [G] Continuar con Google│       │     outlined, fondo neutral.50
│  └──────────────────────────┘       │     logo Google oficial
│                                     │
│  ┌──────────────────────────┐       │  ← Apple SSO button
│  │  [] Continuar con Apple  │       │     fondo negro en light mode
│  └──────────────────────────┘       │     fondo blanco en dark mode (HIG)
│                                     │
│  ¿No tienes cuenta?  Regístrate     │  ← Centered
│                                     │     "Regístrate" en primary.500
└─────────────────────────────────────┘
```

**Comportamientos clave:**
- Input email: keyboard type `emailAddress`, autocapitalize `none`
- Input password: `obscureText: true`, toggle visibility
- Botón Google: `supabase.auth.signInWithOAuth(OAuthProvider.google)`
- Botón Apple: solo visible en iOS (Flutter Platform check)
- On success: navigate a Home, clearStack

---

## Register Screen

```
┌─────────────────────────────────────┐
│ ←                                   │
│                                     │
│  Crea tu cuenta                     │  ← Playfair Display 36px bold
│                                     │
│  Es gratis para empezar.            │  ← Plus Jakarta 16px, neutral.500
│                                     │
│  ┌─────────────────────────────┐    │  ← Input: Nombre
│  │ 👤  ¿Cómo te llamamos?      │    │     textCapitalization: words
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← Input: Email
│  │ ✉  Correo electrónico       │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← Input: Password
│  │ 🔒  Contraseña              │    │     con reglas visibles (ver abajo)
│  │                         👁  │    │
│  └─────────────────────────────┘    │
│                                     │
│  ● 8 caracteres mínimo              │  ← Password strength checklist
│  ○ Una mayúscula                    │     ● = cumplido (primary.500)
│  ○ Un número o símbolo              │     ○ = pendiente (neutral.400)
│                                     │     aparece al primer keystroke
│  ┌─────────────────────────────┐    │
│  │           Crear cuenta      │    │  ← Button primary large
│  └─────────────────────────────┘    │     disabled hasta que form es válido
│                                     │
│  ─────────── o regístrate con ────  │
│                                     │
│  [G] Google    [] Apple             │  ← Side by side si caben
│                                     │     (en 375px: apilados)
│                                     │
│  Al registrarte aceptas los         │  ← Términos: Plus Jakarta 12px
│  Términos de uso y la Política      │     neutral.500
│  de Privacidad                      │     Links: primary.500
│                                     │
│  ¿Ya tienes cuenta?  Inicia sesión  │
└─────────────────────────────────────┘
```

---

## Forgot Password Screen

```
┌─────────────────────────────────────┐
│ ←                                   │
│                                     │
│                                     │
│      [ÍCONO: envelope open]         │  ← Lucide `mail-open`, 64px
│                                     │     color: secondary.400
│  Recupera tu contraseña             │  ← Plus Jakarta 28px, semibold
│                                     │
│  Ingresa tu email y te enviamos     │  ← Plus Jakarta 16px, neutral.500
│  un link para resetearla.           │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ ✉  Correo electrónico       │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │       Enviar link           │    │
│  └─────────────────────────────┘    │
│                                     │
│  ← Volver al inicio de sesión       │  ← ghost link, left-aligned
│                                     │
└─────────────────────────────────────┘
```

**Estado post-envío:**

```
┌─────────────────────────────────────┐
│ ←                                   │
│                                     │
│      [ÍCONO: check-circle]          │  ← verde success, 64px, animado
│                                     │     scale 0→1, bounce spring
│  Revisa tu email                    │
│                                     │
│  Enviamos el link a                 │
│  camila@gmail.com                   │  ← email en semibold
│                                     │
│  ¿No llegó?  Reenviar en 58s        │  ← countdown timer
│                                     │     "Reenviar" deshabilitado
│                                     │     hasta que expire
│                                     │
│  ← Volver al inicio de sesión       │
│                                     │
└─────────────────────────────────────┘
```
