# ⌨️ CONTEXTO — Proyecto Teclado de Señas MVP

**Cargado cuando trabajas en `/teclado-senias/`**

## Estado actual (2026-04-11)

✅ **COMPLETADO:** Android APK compilado (61MB), 40+ endpoints, 7 screens, WCAG AA
✅ **TESTADO:** APK instalado & ejecutado en dispositivo, sin crashes
🔄 **PRÓXIMA FASE:** Re-integración Supabase + testing QA

## Documentación de referencia

- [MVP COMPLETADO](../../MEMORIA.md) — Full delivery checklist
- [TESTING RESULTS](../../MEMORIA.md) — APK execution log
- Memoria: `proyectos/teclado_senias.md`

## Stack actual

- **Mobile:** Flutter (Dart 3)
- **Backend:** FastAPI (Python) + Supabase
- **BD:** PostgreSQL (Supabase)
- **APIs:** 40+ endpoints en FastAPI
- **Auth:** JWT (implementado)

## Principales features

1. **7 Screens:** onboarding, home, translate, history, settings, profile, lessons
2. **Traducción:** Palabras → Señas (gestos, video)
3. **Historial:** Guardado local + nube
4. **Lecciones:** Módulos de aprendizaje
5. **WCAG AA:** Accesibilidad para sordomudos

## Próximas acciones

1. Migrar BD a Supabase (desde SQLite local)
2. Conectar Flutter ↔ APIs FastAPI
3. Testing QA en dispositivos reales
4. Preparar for App Store / Google Play

## Contactos

- **Producto:** Juan Camilo Gil
- **Tech Lead:** Sasha (Backend) / Brook (Frontend)
- **Testing:** Ego

---

**Cargado automáticamente cuando:** pathway contiene `teclado-senias`  
**Owner:** Jarvis | **Agentes:** Sasha, Brook, Alejo
