# SPRINT 0 — UPDATES DE ARQUITECTURA CONFIRMADOS

**Fecha:** 29 de Marzo, 2026
**Responsable:** Sasha
**Cambios confirmados por:** Juan Camilo Gil
**Stack base:** FastAPI + Supabase + Railway + Replicate

---

## CAMBIOS CONFIRMADOS — APLICAR A ARQUITECTURA EXISTENTE

### 1. RECOMENDACIONES IA: Claude API → Google Gemini API

**Ubicación en arquitectura actual:**
- Archivo: `ASESOR_IMAGEN_AI_ARQUITECTURA.md` línea 51
- Servicio: `app/services/recommendation_service.py`
- Endpoints afectados: `POST /api/v1/recommendations`, `GET /api/v1/recommendations/history`

**Cambios técnicos:**

#### Antes (Claude API):
```python
# app/services/recommendation_service.py
import anthropic

class RecommendationService:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    async def get_outfit_recommendations(
        self,
        user_id: str,
        wardrobe_items: List[dict],
        body_analysis: dict,
        occasion: str
    ) -> str:
        """Get Claude recommendations for outfit combinations."""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Based on wardrobe {wardrobe_items} and body type {body_analysis}, recommend outfits for {occasion}."
                }
            ]
        )
        return response.content[0].text
```

#### Después (Google Gemini API):
```python
# app/services/recommendation_service.py
import google.generativeai as genai
from google.generativeai.types import GenerativeModel
import base64

class RecommendationService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-001")

    async def get_outfit_recommendations(
        self,
        user_id: str,
        wardrobe_items: List[dict],
        body_analysis: dict,
        occasion: str,
        body_image_url: Optional[str] = None  # NEW: multimodal support
    ) -> dict:
        """
        Get Gemini recommendations with multimodal image analysis.
        Gemini excels at visual outfit matching.
        """
        # Prepare multimodal prompt
        parts = [
            f"""Eres un asesor de imagen experto. Analiza la siguiente información y crea recomendaciones de outfits:

CUERPO:
{json.dumps(body_analysis, ensure_ascii=False)}

GUARDARROPA:
{json.dumps(wardrobe_items, ensure_ascii=False)}

OCASIÓN: {occasion}

Proporciona 3 combinaciones de outfits recomendadas con:
1. Justificación basada en el tipo de cuerpo
2. Combinación de colores óptima
3. Ocasión y contexto
4. Alternativas si falta algún item
5. Presupuesto total estimado

Responde en JSON con estructura:
{{
  "recommendations": [
    {{
      "id": "rec_1",
      "items": ["item_id_1", "item_id_2", "item_id_3"],
      "reason": "...",
      "color_harmony": "...",
      "occasion_fit": "...",
      "estimated_budget": 0.0
    }}
  ],
  "color_analysis": {{
    "best_colors_for_occasion": [...],
    "avoid_combinations": [...]
  }},
  "styling_tips": ["tip1", "tip2"]
}}"""
        ]

        # Agregar imagen si disponible (ventaja Gemini)
        if body_image_url:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(requests.get(body_image_url).content).decode()
                }
            })

        response = self.model.generate_content(parts)

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback si respuesta no es JSON puro
            return {
                "recommendations": [],
                "raw_response": response.text,
                "color_analysis": {},
                "styling_tips": []
            }
```

**Credenciales:**
- Google Gemini API Key: Mismo proyecto que Google Vision API
- Modelo recomendado: `gemini-2.0-flash-001` (mejor relación velocidad/costo)
- Rate limit: 60 req/min (free tier), upgrade a 10K req/día con proyecto pagado

**Ventajas Gemini vs Claude:**
- ✅ Mejor análisis visual de prendas y combinaciones
- ✅ Soporte multimodal nativo (imagen + texto simultáneamente)
- ✅ 5x más barato que Claude Opus ($0.075 vs $0.30 por 1M tokens)
- ✅ Integración con Google Lens para análisis de moda
- ⚠️ Context window: 32K tokens (vs 200K Claude)

**Endpoints afectados - UPDATE requerido:**
```python
# app/api/v1/endpoints/recommendations.py

@router.post("/recommendations")
async def get_recommendations(
    request: RecommendationRequest,  # wardrobe_items, body_analysis, occasion, body_image (NEW)
    current_user: User = Depends(get_current_user),
    recommendation_service: RecommendationService = Depends()
) -> RecommendationResponse:
    """
    NEW: Gemini multimodal recommendations.
    Puede incluir imagen del cuerpo para análisis visual.
    """
    result = await recommendation_service.get_outfit_recommendations(
        user_id=current_user.id,
        wardrobe_items=request.items,
        body_analysis=request.body_analysis,
        occasion=request.occasion,
        body_image_url=request.body_image_url  # NEW
    )

    # Log para analytics
    await analytics_service.log_event(
        user_id=current_user.id,
        event_type="recommendation_generated",
        metadata={
            "model": "gemini-2.0-flash",
            "occasion": request.occasion,
            "items_count": len(request.items)
        }
    )

    return RecommendationResponse(**result)
```

**Schemas NEW:**
```python
# app/schemas/recommendations.py

class RecommendationRequest(BaseModel):
    items: List[dict]  # wardrobe items
    body_analysis: dict  # measurements, body_shape, skin_tone
    occasion: str  # casual, work, date, party, outdoor
    body_image_url: Optional[str] = None  # NEW: for multimodal analysis

class OutfitRecommendation(BaseModel):
    id: str
    items: List[str]
    reason: str
    color_harmony: str
    occasion_fit: str
    estimated_budget: float

class RecommendationResponse(BaseModel):
    recommendations: List[OutfitRecommendation]
    color_analysis: dict
    styling_tips: List[str]
    model_used: str = "gemini-2.0-flash"
    generated_at: datetime
```

**Testing:**
```python
# tests/api/test_recommendations.py

@pytest.mark.asyncio
async def test_gemini_multimodal_recommendations():
    """Test Gemini with image + text input."""
    service = RecommendationService(api_key=GEMINI_API_KEY)

    result = await service.get_outfit_recommendations(
        user_id="test_user",
        wardrobe_items=[{"id": "shirt_1", "color": "blue"}],
        body_analysis={"body_shape": "pear", "skin_tone": "medium"},
        occasion="work",
        body_image_url="https://..."  # NEW
    )

    assert "recommendations" in result
    assert len(result["recommendations"]) == 3
    assert "color_analysis" in result
```

---

### 2. PAGOS: Stripe/Mercado Pago → PSE (PayU) + Google Pay

**Ubicación en arquitectura actual:**
- Archivo: `ASESOR_IMAGEN_AI_ARQUITECTURA.md` líneas 253-257
- Servicio: `app/services/subscription_service.py`
- Tabla DB: `users.subscription_id`
- Endpoints afectados: `/api/v1/subscriptions/*`

**Cambios en Database Schema:**

#### Antes:
```sql
-- users table
subscription_id TEXT,  -- Stripe or Mercado Pago subscription ID
```

#### Después:
```sql
-- users table (UPDATE)
ALTER TABLE public.users ADD COLUMN payment_method TEXT; -- 'pse', 'google_pay', 'card'
ALTER TABLE public.users ADD COLUMN payu_customer_id TEXT; -- PayU customer reference
ALTER TABLE public.users ADD COLUMN payu_subscription_id TEXT; -- PayU subscription token

-- NEW: Payments table (track every transaction)
CREATE TABLE public.payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'COP',  -- Colombian Peso for PSE
  status TEXT NOT NULL, -- 'pending', 'completed', 'failed', 'declined'
  payment_method TEXT NOT NULL, -- 'pse', 'google_pay', 'card'
  payu_reference_code TEXT UNIQUE,
  payu_transaction_id TEXT,
  payu_response TEXT,  -- Full response JSON from PayU
  subscription_period TEXT, -- 'monthly', 'annual'
  receipt_url TEXT,
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own payments" ON payments FOR SELECT
  TO authenticated USING (user_id = auth.uid());
CREATE INDEX idx_payments_user_created ON payments(user_id, created_at DESC);
CREATE INDEX idx_payments_status ON payments(status);

-- NEW: Receipts table
CREATE TABLE public.receipts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  payment_id UUID NOT NULL REFERENCES payments(id),
  user_id UUID NOT NULL REFERENCES users(id),
  receipt_number TEXT UNIQUE,
  amount DECIMAL(10, 2),
  currency TEXT,
  payment_date TIMESTAMPTZ,
  receipt_url TEXT,
  pdf_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.receipts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own receipts" ON receipts FOR SELECT
  TO authenticated USING (user_id = auth.uid());
```

**Cambios en Services:**

#### Antes:
```python
# Stripe checkout → PayU initialization flow
class SubscriptionService:
    def __init__(self, stripe_key: str, mp_token: str):
        # Stripe + Mercado Pago
```

#### Después:
```python
# app/services/payment_service.py (RENAMED from subscription_service.py)

import httpx
import hmac
import hashlib
from typing import Literal

class PaymentService:
    """
    PayU API integration for PSE + Google Pay.
    Docs: https://developers.payulatam.com/es/
    """

    def __init__(
        self,
        payu_merchant_id: str,
        payu_account_id: str,
        payu_api_key: str,
        payu_api_login: str,
        environment: Literal["sandbox", "production"] = "sandbox"
    ):
        self.merchant_id = payu_merchant_id
        self.account_id = payu_account_id
        self.api_key = payu_api_key
        self.api_login = payu_api_login

        if environment == "sandbox":
            self.base_url = "https://sandbox.payulatam.com/payments-api/4.0"
            self.reports_url = "https://sandbox.reporting-api.payulatam.com"
        else:
            self.base_url = "https://api.payulatam.com/payments-api/4.0"
            self.reports_url = "https://reporting-api.payulatam.com"

    def _generate_signature(
        self,
        reference_code: str,
        amount: float,
        currency: str
    ) -> str:
        """
        PayU requires HMAC-SHA256 signature for request authentication.
        Formula: SHA256(apiKey~merchantId~referenceCode~amount~currency)
        """
        message = f"{self.api_key}~{self.merchant_id}~{reference_code}~{amount}~{currency}"
        signature = hashlib.sha256(message.encode()).hexdigest()
        return signature

    async def create_pse_payment_session(
        self,
        user_id: str,
        email: str,
        amount: float,
        reference_code: str,  # Unique per transaction
        description: str,  # "Premium Monthly Subscription"
        full_name: str,
        phone: str
    ) -> dict:
        """
        Create PSE payment session for Colombian users.
        PSE = Sistema de Pagos Electrónicos (banks in Colombia).

        Flow:
        1. Backend generates session
        2. Flutter webview opens PayU hosted payment form
        3. User selects bank and authenticates
        4. PayU sends webhook to confirm
        5. Backend updates subscription
        """

        signature = self._generate_signature(
            reference_code,
            amount,
            "COP"  # Colombian Peso
        )

        payload = {
            "language": "es",
            "command": "SUBMIT_TRANSACTION",
            "merchant": {
                "apiKey": self.api_key,
                "apiLogin": self.api_login
            },
            "transaction": {
                "order": {
                    "accountId": self.account_id,
                    "referenceCode": reference_code,
                    "description": description,
                    "language": "es",
                    "signature": signature,
                    "notifyUrl": f"https://api.example.com/webhook/payu",  # Webhook URL
                    "shippingAddress": {
                        "city": "Bogotá",
                        "country": "CO",
                        "postalCode": "110111",
                        "state": "Cundinamarca"
                    },
                    "buyer": {
                        "merchantBuyerId": user_id,
                        "fullName": full_name,
                        "emailAddress": email,
                        "contactPhone": phone
                    },
                    "additionalValues": {
                        "TX_VALUE": {
                            "value": amount,
                            "currency": "COP"
                        },
                        "TX_TAX": {"value": 0, "currency": "COP"},
                        "TX_TAX_RETURN_BASE": {"value": 0, "currency": "COP"}
                    }
                },
                "payer": {
                    "merchantPayerId": user_id,
                    "fullName": full_name,
                    "emailAddress": email,
                    "contactPhone": phone,
                    "billingAddress": {
                        "city": "Bogotá",
                        "country": "CO",
                        "postalCode": "110111",
                        "state": "Cundinamarca"
                    }
                },
                "type": "AUTHORIZATION_AND_CAPTURE",
                "paymentMethod": "PSE",  # PSE para transferencia electrónica
                "paymentCountry": "CO",
                "ipAddress": "192.168.1.1"  # Obtener del request
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments",
                json=payload
            )

        result = response.json()

        if result.get("code") == "SUCCESS":
            return {
                "transaction_id": result["transactionResponse"]["transactionId"],
                "reference_code": reference_code,
                "payu_url": result["transactionResponse"].get("redirectUrl"),
                "status": "PENDING_AUTHORIZATION"
            }
        else:
            raise Exception(f"PayU error: {result.get('error')}")

    async def create_google_pay_token_payment(
        self,
        user_id: str,
        email: str,
        amount: float,
        reference_code: str,
        google_pay_token: str,  # Viene del cliente Flutter
        full_name: str
    ) -> dict:
        """
        Google Pay token → PayU direct charge.
        User selects payment method in Google Pay, we get encrypted token.
        """

        signature = self._generate_signature(
            reference_code,
            amount,
            "COP"
        )

        payload = {
            "language": "es",
            "command": "SUBMIT_TRANSACTION",
            "merchant": {
                "apiKey": self.api_key,
                "apiLogin": self.api_login
            },
            "transaction": {
                "order": {
                    "accountId": self.account_id,
                    "referenceCode": reference_code,
                    "description": "Premium Subscription",
                    "language": "es",
                    "signature": signature,
                    "buyer": {
                        "fullName": full_name,
                        "emailAddress": email
                    },
                    "additionalValues": {
                        "TX_VALUE": {"value": amount, "currency": "COP"},
                        "TX_TAX": {"value": 0, "currency": "COP"},
                        "TX_TAX_RETURN_BASE": {"value": 0, "currency": "COP"}
                    }
                },
                "payer": {
                    "fullName": full_name,
                    "emailAddress": email
                },
                "creditCard": {
                    "securityCode": google_pay_token  # Token encriptado de Google Pay
                },
                "type": "AUTHORIZATION_AND_CAPTURE",
                "paymentMethod": "GOOGLEPAY",
                "paymentCountry": "CO"
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments",
                json=payload
            )

        result = response.json()
        return {
            "transaction_id": result["transactionResponse"]["transactionId"],
            "reference_code": reference_code,
            "status": result["transactionResponse"]["responseCode"]
        }

    async def handle_payu_webhook(
        self,
        event: dict,
        user_repository: "UserRepository",
        payment_repository: "PaymentRepository"
    ) -> None:
        """
        Handle PayU webhook callbacks.
        Events: CONFIRMED, REJECTED, EXPIRED, PENDING
        """
        event_type = event.get("type")
        reference_code = event.get("transaction", {}).get("order", {}).get("referenceCode")

        if event_type == "TRANSACTION":
            response_code = event.get("transaction", {}).get("responseCode")

            if response_code == "APPROVED":
                # Mark subscription as active
                payment = await payment_repository.update_by_reference(
                    reference_code,
                    status="completed",
                    payu_transaction_id=event.get("transaction", {}).get("transactionId")
                )

                await user_repository.update_subscription(
                    user_id=payment.user_id,
                    status="active",
                    tier="premium_monthly"
                )

            elif response_code == "DECLINED":
                await payment_repository.update_by_reference(
                    reference_code,
                    status="failed",
                    error_message=event.get("transaction", {}).get("errorMessage")
                )

    async def cancel_subscription(
        self,
        user_id: str
    ) -> None:
        """Cancel recurrent payment (if any)."""
        # PayU no tiene "suscripciones" automáticas como Stripe
        # Cada mes se cobra manualmente o se programa un pago recurrente
        # Para cancelar: solo marcar user.subscription_status = 'cancelled'
        pass
```

**Endpoints NEW/UPDATED:**

```python
# app/api/v1/endpoints/subscriptions.py

@router.get("/plans")
async def get_subscription_plans() -> List[SubscriptionPlan]:
    """
    Available plans:
    - Free: $0/month, 5 analyses/month
    - Premium Monthly: $4.99 COP/month
    - Premium Annual: $49.99 COP/year (save 16%)
    """
    return [
        SubscriptionPlan(
            id="free",
            name="Gratis",
            price=0,
            currency="COP",
            features=["5 análisis/mes", "Guardarropa básico"]
        ),
        SubscriptionPlan(
            id="premium_monthly",
            name="Premium Mensual",
            price=19990,  # ~$5 USD en COP
            currency="COP",
            features=["Análisis ilimitados", "Try-on ilimitado", "Recomendaciones IA"]
        ),
        SubscriptionPlan(
            id="premium_annual",
            name="Premium Anual",
            price=199900,  # ~$50 USD, save 16%
            currency="COP",
            features=["Análisis ilimitados", "Try-on ilimitado", "Recomendaciones IA", "Soporte prioritario"]
        )
    ]

@router.post("/checkout/pse")
async def create_pse_checkout(
    request: PSECheckoutRequest,  # plan_id, phone
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends()
) -> PSECheckoutResponse:
    """
    PSE payment flow:
    1. Generate unique reference code
    2. Create PayU session
    3. Return webview URL for Flutter to open
    4. User completes payment in bank website
    5. PayU webhook confirms
    """
    import uuid
    from datetime import datetime

    reference_code = f"SUB_{current_user.id}_{datetime.now().timestamp()}"

    session = await payment_service.create_pse_payment_session(
        user_id=current_user.id,
        email=current_user.email,
        amount=19990,  # Premium monthly in COP
        reference_code=reference_code,
        description="Premium Monthly Subscription",
        full_name=current_user.full_name,
        phone=request.phone
    )

    # Save pending payment
    await payment_repository.create(
        user_id=current_user.id,
        amount=19990,
        currency="COP",
        status="pending",
        payment_method="pse",
        payu_reference_code=reference_code,
        subscription_period="monthly"
    )

    return PSECheckoutResponse(
        reference_code=reference_code,
        payu_webview_url=session["payu_url"],
        expires_at=datetime.now() + timedelta(minutes=15)
    )

@router.post("/checkout/google-pay")
async def create_google_pay_checkout(
    request: GooglePayCheckoutRequest,  # google_pay_token, plan_id
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends()
) -> GooglePayCheckoutResponse:
    """
    Google Pay direct charge (no webview needed).
    User selects card in Google Pay → we get encrypted token.
    """
    reference_code = f"SUB_{current_user.id}_{datetime.now().timestamp()}"

    result = await payment_service.create_google_pay_token_payment(
        user_id=current_user.id,
        email=current_user.email,
        amount=19990,
        reference_code=reference_code,
        google_pay_token=request.google_pay_token,
        full_name=current_user.full_name
    )

    # Save payment result
    payment = await payment_repository.create(
        user_id=current_user.id,
        amount=19990,
        currency="COP",
        status=result["status"].lower(),
        payment_method="google_pay",
        payu_transaction_id=result["transaction_id"],
        payu_reference_code=reference_code,
        subscription_period="monthly"
    )

    # If approved, mark subscription as active
    if result["status"] == "APPROVED":
        await user_repository.update_subscription(
            user_id=current_user.id,
            status="active",
            tier="premium_monthly",
            payment_method="google_pay"
        )

    return GooglePayCheckoutResponse(
        status=result["status"],
        message="Pago procesado exitosamente" if result["status"] == "APPROVED" else "Pago rechazado"
    )

@router.post("/webhook/payu")
async def payu_webhook(
    request: Request,
    payment_service: PaymentService = Depends()
):
    """
    PayU sends webhook when transaction completes.
    Signature validation required.
    """
    body = await request.json()

    # Validate signature (important for security)
    # PayU includes X-PayU-Signature header

    await payment_service.handle_payu_webhook(
        event=body,
        user_repository=user_repository,
        payment_repository=payment_repository
    )

    return {"status": "received"}

@router.get("/status")
async def get_subscription_status(
    current_user: User = Depends(get_current_user)
) -> SubscriptionStatus:
    """Get current subscription tier, renewal date, etc."""
    return SubscriptionStatus(
        tier=current_user.subscription_tier,
        status=current_user.subscription_status,
        payment_method=current_user.payment_method,
        renewal_date=current_user.next_renewal_date,
        features=get_features_for_tier(current_user.subscription_tier)
    )

@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends()
) -> dict:
    """Cancel premium subscription (downgrade to free)."""
    await user_repository.update_subscription(
        user_id=current_user.id,
        status="cancelled",
        tier="free"
    )

    await analytics_service.log_event(
        user_id=current_user.id,
        event_type="subscription_cancelled"
    )

    return {"message": "Suscripción cancelada"}
```

**Schemas NEW:**

```python
# app/schemas/payments.py

class PSECheckoutRequest(BaseModel):
    plan_id: str  # 'premium_monthly' or 'premium_annual'
    phone: str  # User's phone number

class PSECheckoutResponse(BaseModel):
    reference_code: str
    payu_webview_url: str
    expires_at: datetime

class GooglePayCheckoutRequest(BaseModel):
    plan_id: str
    google_pay_token: str  # Encrypted token from Google Pay

class GooglePayCheckoutResponse(BaseModel):
    status: str  # 'APPROVED', 'DECLINED', 'PENDING'
    message: str

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price: float
    currency: str
    features: List[str]

class SubscriptionStatus(BaseModel):
    tier: str
    status: str
    payment_method: Optional[str]
    renewal_date: Optional[datetime]
    features: List[str]
```

**Credenciales PayU (obtener de PayU):**
```
PAYU_MERCHANT_ID = "..." (numérico)
PAYU_ACCOUNT_ID = "..." (para Colombia)
PAYU_API_KEY = "..." (secreto)
PAYU_API_LOGIN = "..." (usuario)
PAYU_ENVIRONMENT = "sandbox" (durante desarrollo)
```

**Ventajas PSE + Google Pay vs Stripe:**
- ✅ PSE: Mejor penetración en Colombia (preferencia local)
- ✅ Google Pay: Integración nativa Flutter, menor fricción
- ✅ Costos: 1.9% + $500 COP fijo (vs 2.9% Stripe)
- ⚠️ PSE requiere webview (no automatizado como Stripe)
- ⚠️ Google Pay requiere setup especial en Flutter

---

### 3. STACK CONFIRMADO — SIN CAMBIOS EN ARQUITECTURA BASE

**Ya validado:**
- ✅ FastAPI (backend)
- ✅ Supabase (PostgreSQL + Auth + Storage)
- ✅ Railway (deploy)
- ✅ Replicate (virtual try-on)
- ✅ Google Vision API (body analysis)

**NUEVO agregado:**
- ✅ Google Gemini API (recomendaciones IA)
- ✅ PayU API (pagos PSE + Google Pay)

---

## IMPACTO EN ARQUITECTURA

### Ficheros a ACTUALIZAR:

| Archivo | Cambios | Prioridad |
|---------|---------|-----------|
| `app/services/recommendation_service.py` | Claude → Gemini API, multimodal support | ALTA |
| `app/services/subscription_service.py` | RENOMBRAR a `payment_service.py`, reescribir completamente | ALTA |
| `app/api/v1/endpoints/subscriptions.py` | PSE + Google Pay endpoints, webhooks | ALTA |
| `app/schemas/payments.py` | NEW: PSE/Google Pay request/response models | ALTA |
| Database schema (Supabase migrations) | NEW: payments, receipts tables; ALTER users | ALTA |
| `app/config.py` | NEW: PAYU_* environment variables | MEDIA |
| `app/dependencies.py` | PaymentService initialization | MEDIA |
| `.env.example` | NEW: PAYU_* and GEMINI_API_KEY | BAJA |
| `tests/api/test_recommendations.py` | Actualizar para Gemini multimodal | MEDIA |
| `tests/api/test_subscriptions.py` | NEW: PSE/Google Pay flow tests | MEDIA |

### Ficheros SIN CAMBIOS:

- `app/main.py` — No cambios de estructura
- `app/core/security.py` — JWT sigue igual
- `app/api/v1/endpoints/auth.py` — Sin cambios
- `app/api/v1/endpoints/wardrobe.py` — Sin cambios
- `app/api/v1/endpoints/tryons.py` — Sin cambios
- `app/schemas/auth.py` — Sin cambios
- Database: tablas auth, users (columnas), wardrobe_items, outfits, tryons, body_analysis — Sin cambios

---

## RESUMEN DE TRABAJO — SPRINT 0

### BLOQUE 1 — Arquitectura Final (30h)

1. **Gemini Integration** (8h)
   - Actualizar RecommendationService
   - Crear prompts optimizados para Gemini
   - Endpoint POST /recommendations con multimodal
   - Tests de multimodal analysis

2. **PayU Integration** (12h)
   - Crear PaymentService (PSE + Google Pay)
   - Endpoints: /checkout/pse, /checkout/google-pay, /webhook/payu
   - Schemas for payments
   - Signature validation

3. **Database Migrations** (5h)
   - Crear `payments` table
   - Crear `receipts` table
   - ALTER `users` table (payment_method, payu_*)
   - Índices y RLS policies

4. **OpenAPI 3.0 Spec Update** (5h)
   - Actualizar endpoints de recommendations (multimodal)
   - Actualizar endpoints de payments (PSE/Google Pay)
   - Documento completo 40+ endpoints

### BLOQUE 2 — Infrastructure (40h)
- Supabase, Railway, GitHub, FastAPI boilerplate
- (Sin cambios por Gemini/PayU)

### BLOQUE 3 — Documentación (5h)
- Sprint 0 Deliverables
- Integration guides (Gemini + PayU)

**Total Sprint 0: 75 horas**

---

## CREDENCIALES NECESARIAS

**Confirmadas/Disponibles:**
- ✅ Google Vision API: `...`
- ✅ Replicate: `<REDACTED_REPLICATE>`
- ✅ Supabase: `https://qzmjhxhhgdakvsnhbsze.supabase.co` + keys
- ✅ Google Gemini: Mismo proyecto Vision

**A CREAR esta semana:**
- ⏳ PayU Sandbox: Contactar a PayU para credentials
  - PAYU_MERCHANT_ID
  - PAYU_ACCOUNT_ID (Colombia)
  - PAYU_API_KEY
  - PAYU_API_LOGIN

---

## GO/NO-GO — VIERNES 4 DE ABRIL

**Entregables Sprint 0:**
1. ✅ OpenAPI 3.0 spec (Gemini + PayU updates)
2. ✅ GitHub repo privado con boilerplate FastAPI
3. ✅ Supabase migrations (payments + receipts tables)
4. ✅ PaymentService + RecommendationService code
5. ✅ Railway staging environment
6. ✅ Docker setup + CI/CD basics
7. ✅ SPRINT_0_DELIVERABLES.md
8. ✅ Integration guides (Gemini + PayU)

**Go/No-Go Decision:**
- ✅ Go → Sprint 1 arranca Apr 8
- 🔴 No-Go → Extend Sprint 0

---

## PREGUNTAS CRÍTICAS PARA JARVIS

1. **PayU Sandbox:** ¿Ya tienes contacto o lo creamos esta semana?
2. **Flutter Version:** ¿Latest stable o especific (e.g., 3.24)?
3. **CI/CD:** GitHub Actions standard o custom setup?
4. **Gemini Rate Limits:** ¿Free tier (60 req/min) es suficiente para MVP o pagamos upgrade?

---

**Documento creado:** 29 de Marzo, 2026
**Próxima revisión:** 4 de Abril, 2026 (fin Sprint 0)
