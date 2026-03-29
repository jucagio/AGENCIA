# ASESOR DE IMAGEN AI — Arquitectura Técnica Completa (MVP 14 semanas)

**Proyecto:** Asesor de Imagen con Virtual Try-On
**Timeline:** 14 semanas (Sprint 0 a 13)
**Objetivo:** 50K usuarios, día 1
**Stack:** FastAPI + Flutter + Supabase + Replicate + Claude API
**Modelo:** Freemium ($4.99-8.99/mes premium)

---

## 1. ARQUITECTURA TÉCNICA DETALLADA

### 1.1 Backend — FastAPI + Supabase

```
app/
├── main.py                          # FastAPI app, startup, middleware
├── config.py                        # Pydantic BaseSettings
├── dependencies.py                  # DB session, auth, external clients
├── core/
│   ├── security.py                  # JWT, password hashing, auth
│   ├── exceptions.py                # Custom exceptions
│   └── middleware.py                # CORS, rate limiting, logging
├── api/
│   └── v1/
│       ├── router.py                # Main router
│       └── endpoints/
│           ├── auth.py              # Login, register, social oauth
│           ├── users.py             # Profile, preferences, subscription
│           ├── wardrobe.py          # Upload, categorize, list clothes
│           ├── analysis.py          # Body analysis, color matching
│           ├── tryons.py            # Virtual try-on requests
│           ├── recommendations.py   # Outfit suggestions (Claude API)
│           ├── subscriptions.py     # Stripe/Mercado Pago webhooks
│           └── analytics.py         # User behavior tracking
├── models/
│   ├── user.py                      # User, subscription status
│   ├── wardrobe.py                  # Clothing items, categories
│   ├── outfit.py                    # Saved outfits, try-ons
│   └── analysis.py                  # Body analysis results
├── schemas/
│   ├── auth.py                      # LoginRequest, RegisterRequest
│   ├── user.py                      # UserResponse, ProfileUpdate
│   ├── wardrobe.py                  # ClothingItem, WardrobeResponse
│   └── common.py                    # PaginatedResponse, ErrorResponse
├── services/
│   ├── auth_service.py              # Login, register, JWT tokens
│   ├── user_service.py              # Profile management
│   ├── body_analysis_service.py     # Google Vision + MediaPipe integration
│   ├── wardrobe_service.py          # Clothing catalogation
│   ├── recommendation_service.py    # Claude API for suggestions
│   ├── tryon_service.py             # Replicate API for virtual try-on
│   ├── subscription_service.py      # Stripe/Mercado Pago integration
│   ├── storage_service.py           # Supabase Storage operations
│   └── analytics_service.py         # Event tracking
├── repositories/
│   ├── user_repository.py
│   ├── wardrobe_repository.py
│   ├── outfit_repository.py
│   └── analysis_repository.py
├── utils/
│   ├── validators.py
│   ├── pagination.py
│   ├── image_processing.py          # Resize, compress, format conversion
│   └── cache.py                     # Redis-like caching logic
└── tests/
    ├── conftest.py
    └── api/
        ├── test_auth.py
        ├── test_wardrobe.py
        └── test_tryons.py
```

### 1.2 Database Schema (PostgreSQL vía Supabase)

```sql
-- Users table
CREATE TABLE public.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  full_name TEXT NOT NULL,
  avatar_url TEXT,
  google_oauth_id TEXT UNIQUE,
  subscription_tier TEXT DEFAULT 'free', -- 'free', 'premium_monthly', 'premium_annual'
  subscription_status TEXT DEFAULT 'active', -- 'active', 'cancelled', 'past_due'
  subscription_id TEXT, -- Stripe/Mercado Pago subscription ID
  body_shape TEXT, -- 'pear', 'apple', 'hourglass', 'rectangle', 'inverted_triangle'
  skin_tone TEXT, -- 'fair', 'light', 'medium', 'olive', 'tan', 'dark'
  color_preferences TEXT[], -- Colors user prefers
  budget_range TEXT, -- '$50-100', '$100-250', '$250-500', '$500+'
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own profile" ON users FOR SELECT
  TO authenticated USING (id = auth.uid());

-- Body analysis results
CREATE TABLE public.body_analysis (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  height_cm INT,
  weight_kg INT,
  measurements JSONB, -- {bust: 90, waist: 70, hips: 95, shoulder: 40}
  body_landmarks JSONB, -- MediaPipe keypoints (26 joints)
  color_analysis JSONB, -- Best colors based on skin tone
  style_notes TEXT,
  image_url TEXT, -- Reference photo for analysis
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.body_analysis ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own analysis" ON body_analysis FOR SELECT
  TO authenticated USING (user_id = auth.uid());

-- Wardrobe items
CREATE TABLE public.wardrobe_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category TEXT NOT NULL, -- 'shirt', 'pants', 'dress', 'jacket', 'shoes', 'accessories'
  sub_category TEXT, -- 't-shirt', 'jeans', 'blazer', 'sneakers'
  color TEXT NOT NULL,
  size TEXT, -- 'XS', 'S', 'M', 'L', 'XL', 'XXL'
  brand TEXT,
  price DECIMAL(10, 2),
  purchase_date DATE,
  condition TEXT, -- 'excellent', 'good', 'fair'
  image_url TEXT, -- Stored in Supabase Storage
  image_features JSONB, -- Color palette, style, pattern (from vision API)
  is_favorite BOOLEAN DEFAULT false,
  is_archived BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.wardrobe_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own wardrobe" ON wardrobe_items FOR SELECT
  TO authenticated USING (user_id = auth.uid());
CREATE POLICY "Users manage own wardrobe" ON wardrobe_items FOR INSERT
  TO authenticated WITH CHECK (user_id = auth.uid());

-- Saved outfits
CREATE TABLE public.outfits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  occasion TEXT, -- 'casual', 'work', 'date', 'party', 'outdoor'
  season TEXT, -- 'spring', 'summer', 'fall', 'winter'
  description TEXT,
  items JSONB, -- [{item_id: uuid, position: 1}, ...]
  created_outfit_image_url TEXT, -- Composite image with all items
  likes INT DEFAULT 0,
  rating DECIMAL(3, 2), -- User self-rating
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.outfits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own outfits" ON outfits FOR SELECT
  TO authenticated USING (user_id = auth.uid());

-- Virtual try-on results
CREATE TABLE public.tryons (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  wardrobe_item_id UUID REFERENCES wardrobe_items(id),
  outfit_id UUID REFERENCES outfits(id),
  body_image_url TEXT, -- User's reference photo
  item_image_url TEXT, -- Clothing item
  result_image_url TEXT, -- Virtual try-on result from Replicate
  model_used TEXT, -- 'replicate:model-v2', etc.
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.tryons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own tryons" ON tryons FOR SELECT
  TO authenticated USING (user_id = auth.uid());

-- User analytics
CREATE TABLE public.analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  event_type TEXT, -- 'wardrobe_upload', 'body_analysis', 'tryon_generated', 'recommendation_viewed'
  metadata JSONB, -- Additional data per event
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_wardrobe_user_id ON wardrobe_items(user_id);
CREATE INDEX idx_wardrobe_category ON wardrobe_items(category);
CREATE INDEX idx_wardrobe_user_category ON wardrobe_items(user_id, category);
CREATE INDEX idx_outfits_user_id ON outfits(user_id);
CREATE INDEX idx_tryons_user_id ON tryons(user_id);
CREATE INDEX idx_body_analysis_user_id ON body_analysis(user_id);
CREATE INDEX idx_analytics_user_created ON analytics_events(user_id, created_at DESC);
```

### 1.3 API Endpoints (FastAPI)

```python
# AUTH
POST   /api/v1/auth/register            # Email + password
POST   /api/v1/auth/login               # Email + password → JWT
POST   /api/v1/auth/login/google        # OAuth flow
POST   /api/v1/auth/login/apple         # OAuth flow
POST   /api/v1/auth/refresh             # Refresh token → new JWT
POST   /api/v1/auth/logout              # Logout
POST   /api/v1/auth/forgot-password     # Send reset email
POST   /api/v1/auth/reset-password      # Reset with token

# USERS
GET    /api/v1/users/me                 # Current user profile
PATCH  /api/v1/users/me                 # Update profile
GET    /api/v1/users/me/preferences     # Color, style, budget preferences
PATCH  /api/v1/users/me/preferences     # Update preferences
DELETE /api/v1/users/me                 # Delete account

# BODY ANALYSIS
POST   /api/v1/analysis/upload          # Upload body photo
GET    /api/v1/analysis/latest          # Get latest analysis
POST   /api/v1/analysis/measure         # Manual measurements input
GET    /api/v1/analysis/history         # All analysis records

# WARDROBE
POST   /api/v1/wardrobe/upload          # Upload clothing photo (auto-categorize)
GET    /api/v1/wardrobe                 # List all items (paginated)
GET    /api/v1/wardrobe/{item_id}       # Get item details
PATCH  /api/v1/wardrobe/{item_id}       # Update item (color, size, etc)
DELETE /api/v1/wardrobe/{item_id}       # Archive/delete item
GET    /api/v1/wardrobe/category/{cat}  # List by category
GET    /api/v1/wardrobe/search?q=blue   # Search items

# OUTFITS
POST   /api/v1/outfits                  # Create outfit (select items)
GET    /api/v1/outfits                  # List user outfits
GET    /api/v1/outfits/{outfit_id}      # Get outfit details
PATCH  /api/v1/outfits/{outfit_id}      # Update outfit
DELETE /api/v1/outfits/{outfit_id}      # Delete outfit
POST   /api/v1/outfits/{outfit_id}/rate # Rate outfit

# VIRTUAL TRY-ON
POST   /api/v1/tryons                   # Generate try-on (item + body photo)
GET    /api/v1/tryons                   # List past try-ons
GET    /api/v1/tryons/{tryon_id}        # Get try-on result

# RECOMMENDATIONS
POST   /api/v1/recommendations          # Ask Claude for outfit suggestions
GET    /api/v1/recommendations/history  # Past recommendations

# SUBSCRIPTIONS
GET    /api/v1/subscriptions/plans      # Available plans
POST   /api/v1/subscriptions/checkout   # Create Stripe/MP session
GET    /api/v1/subscriptions/status     # Current subscription
POST   /api/v1/subscriptions/cancel     # Cancel subscription
POST   /api/v1/subscriptions/webhook    # Stripe/Mercado Pago webhook

# ANALYTICS (admin only)
GET    /api/v1/analytics/dau            # Daily active users
GET    /api/v1/analytics/events         # Event tracking
GET    /api/v1/analytics/funnels        # Conversion funnels
```

### 1.4 Flutter Mobile App

```dart
lib/
├── core/
│   ├── constants/
│   │   ├── colors.dart
│   │   ├── strings.dart
│   │   └── dimensions.dart
│   ├── errors/
│   │   ├── failures.dart
│   │   └── exceptions.dart
│   ├── network/
│   │   ├── api_client.dart             # Dio + interceptors
│   │   └── endpoints.dart              # API routes
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── text_themes.dart
│   ├── utils/
│   │   ├── extensions.dart
│   │   ├── image_picker_utils.dart
│   │   ├── validators.dart
│   │   └── storage_helper.dart
│   └── di/
│       └── service_locator.dart        # get_it setup
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── auth_remote_datasource.dart
│   │   │   │   └── auth_local_datasource.dart
│   │   │   ├── models/
│   │   │   │   ├── user_model.dart
│   │   │   │   └── auth_response_model.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_usecase.dart
│   │   │       ├── register_usecase.dart
│   │   │       └── google_signin_usecase.dart
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── auth_bloc.dart
│   │       │   ├── auth_event.dart
│   │       │   └── auth_state.dart
│   │       ├── pages/
│   │       │   ├── login_page.dart
│   │       │   ├── register_page.dart
│   │       │   └── onboarding_page.dart
│   │       └── widgets/
│   │           ├── auth_button.dart
│   │           └── custom_text_field.dart
│   │
│   ├── body_analysis/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   └── analysis_datasource.dart
│   │   │   ├── models/
│   │   │   │   └── body_analysis_model.dart
│   │   │   └── repositories/
│   │   │       └── analysis_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── body_analysis.dart
│   │   │   ├── repositories/
│   │   │   │   └── analysis_repository.dart
│   │   │   └── usecases/
│   │   │       ├── upload_body_photo_usecase.dart
│   │   │       └── get_body_analysis_usecase.dart
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── body_analysis_bloc.dart
│   │       │   ├── body_analysis_event.dart
│   │       │   └── body_analysis_state.dart
│   │       ├── pages/
│   │       │   ├── body_analysis_page.dart
│   │       │   └── analysis_result_page.dart
│   │       └── widgets/
│   │           ├── camera_widget.dart
│   │           └── body_measurement_form.dart
│   │
│   ├── wardrobe/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── wardrobe_bloc.dart
│   │       │   └── ...
│   │       ├── pages/
│   │       │   ├── wardrobe_page.dart
│   │       │   ├── upload_item_page.dart
│   │       │   └── item_detail_page.dart
│   │       └── widgets/
│   │           ├── wardrobe_grid.dart
│   │           └── item_card.dart
│   │
│   ├── outfits/
│   │   └── presentation/
│   │       ├── pages/
│   │       │   ├── outfits_page.dart
│   │       │   ├── create_outfit_page.dart
│   │       │   └── outfit_detail_page.dart
│   │       └── widgets/
│   │           ├── outfit_builder.dart
│   │           └── outfit_card.dart
│   │
│   ├── tryons/
│   │   └── presentation/
│   │       ├── pages/
│   │       │   ├── tryon_page.dart
│   │       │   └── tryon_result_page.dart
│   │       └── widgets/
│   │           └── tryon_view.dart
│   │
│   ├── recommendations/
│   │   └── presentation/
│   │       ├── pages/
│   │       │   └── recommendation_page.dart
│   │       └── widgets/
│   │           └── recommendation_card.dart
│   │
│   └── subscription/
│       └── presentation/
│           ├── pages/
│           │   └── subscription_page.dart
│           └── widgets/
│               └── plan_card.dart
│
├── app.dart                            # MaterialApp, routing
└── main.dart                           # Entry point, DI init
```

**Key Screens (Flutter):**

1. **Auth Screens:**
   - Login / Register (email + password)
   - Google/Apple OAuth
   - Forgot password
   - Onboarding (preferences, body type)

2. **Body Analysis Screen:**
   - Camera to upload body photo
   - Manual measurements input
   - Display analysis results (color palette, style recommendations)
   - Revisit past analyses

3. **Wardrobe Screens:**
   - Grid of uploaded clothing items
   - Camera to upload new item (auto-categorize with Vision API)
   - Item detail (edit color, size, brand, price)
   - Filter by category, color, season
   - Mark favorites

4. **Outfit Builder Screen:**
   - Drag-and-drop items to create outfit
   - Preview on body model
   - Save as outfit
   - Rate outfits

5. **Virtual Try-On Screen:**
   - Select item from wardrobe
   - Select outfit to try with
   - Request try-on (calls Replicate API)
   - View result
   - Save/share result

6. **Recommendations Screen:**
   - Chat-like interface
   - Ask Claude: "Outfit ideas for work meeting"
   - Display AI-generated suggestions with items from wardrobe
   - Buy suggested items (link to Shein, Amazon)

7. **Subscription Screen:**
   - Plans display (free, $4.99/mo, $8.99/mo)
   - Stripe/Mercado Pago payment
   - Manage subscription

### 1.5 External APIs Integration

#### Google Vision API (Body Detection + Image Catalogation)

```python
# app/services/body_analysis_service.py
from google.cloud import vision
import json

class BodyAnalysisService:
    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()

    async def analyze_body_photo(self, image_path: str) -> dict:
        """
        Analyze user's body photo to detect:
        - Pose landmarks (body shape estimation)
        - Color palette (for color analysis)
        - Overall body proportions
        """
        with open(image_path, 'rb') as f:
            image_data = f.read()

        image = vision.Image(content=image_data)
        response = self.vision_client.document_text_detection(image=image)

        # Extract body landmarks via pose detection
        # Return: {body_shape: 'pear', measurements: {...}, colors: [...]}
        return self._extract_body_data(response)

    async def detect_clothing_features(self, image_url: str) -> dict:
        """
        Detect clothing item features:
        - Color (dominant colors)
        - Material (texture analysis)
        - Pattern (solid, striped, floral)
        - Style (formal, casual, sporty)
        """
        image = vision.Image(source=vision.ImageSource(image_uri=image_url))
        response = self.vision_client.label_detection(image=image)

        labels = [label.description for label in response.label_annotations]
        # Parse labels to extract style info
        return {
            'colors': self._extract_colors(image),
            'pattern': self._detect_pattern(labels),
            'style': self._detect_style(labels),
            'material': self._detect_material(labels),
        }

# Pricing: $1.50 per 1,000 requests (label detection)
#          $2.25 per 1,000 requests (object localization)
```

#### Replicate API (Virtual Try-On)

```python
# app/services/tryon_service.py
import replicate

class TryOnService:
    async def generate_virtual_tryon(
        self,
        body_image_url: str,
        item_image_url: str,
        garment_type: str  # 'top', 'bottom', 'dress', 'full-body'
    ) -> str:
        """
        Generate virtual try-on using Replicate's try-on model.
        Returns URL to result image.
        """
        input_data = {
            "background": body_image_url,
            "items": [item_image_url],
            "garment_type": garment_type,
        }

        output = replicate.run(
            "antonioferrari/yolo-virtual-try-on:v2",  # Example model
            input=input_data
        )

        return output[0]  # Result image URL

# Pricing: $0.01 - $0.05 per inference (varies by model)
# Estimate: ~50K users * 5 try-ons/user/month = 250K tryons
# Cost: $2,500 - $12,500/month
```

#### Claude API (Outfit Recommendations)

```python
# app/services/recommendation_service.py
from anthropic import Anthropic

class RecommendationService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    async def get_outfit_recommendation(
        self,
        user_id: str,
        wardrobe_items: list[dict],
        body_shape: str,
        occasion: str,
        query: str
    ) -> str:
        """
        Ask Claude to recommend outfits based on user's wardrobe.
        """
        wardrobe_text = "\n".join([
            f"- {item['category']}: {item['color']} {item['brand']}"
            for item in wardrobe_items
        ])

        prompt = f"""
        User body shape: {body_shape}
        Occasion: {occasion}
        Available items:
        {wardrobe_text}

        User request: {query}

        Suggest 3 outfit combinations from the available items.
        For each outfit:
        1. List items (by color/brand)
        2. Why it works for {occasion}
        3. Styling tips
        """

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

# Pricing: $3/$15 per 1M input/output tokens (Sonnet)
# Estimate: 50K users * 2 recommendations/month = 100K calls
# ~200 tokens per call = 20M tokens
# Cost: $60-300/month
```

#### Stripe / Mercado Pago (Subscriptions)

```python
# app/services/subscription_service.py
import stripe
from mercadopago import configurations, client

class SubscriptionService:
    def __init__(self, stripe_key: str, mp_token: str):
        stripe.api_key = stripe_key
        self.stripe = stripe

        configurations.access_token = mp_token
        self.mp_client = client.Client()

    async def create_stripe_subscription(
        self,
        user_id: str,
        email: str,
        plan_id: str  # 'premium_monthly' or 'premium_annual'
    ) -> str:
        """Create Stripe checkout session for subscription."""
        prices = {
            'premium_monthly': 'price_1Q...',  # From Stripe Dashboard
            'premium_annual': 'price_2Q...',
        }

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': prices[plan_id],
                    'quantity': 1,
                }
            ],
            mode='subscription',
            success_url='https://app.example.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://app.example.com/pricing',
            customer_email=email,
            metadata={'user_id': user_id},
        )

        return checkout_session.url

    async def handle_stripe_webhook(self, event: dict) -> None:
        """Handle Stripe subscription events (payment, cancellation)."""
        if event['type'] == 'customer.subscription.created':
            # Mark user as premium
            pass
        elif event['type'] == 'customer.subscription.deleted':
            # Mark user as free tier
            pass

# Stripe pricing: 2.9% + $0.30 per transaction
# Mercado Pago: 2.9% + varying fees (Latin America focused)
```

#### Supabase Realtime (Live Updates)

```python
# Backend doesn't initiate realtime, but Flutter app subscribes:

# Flutter example:
final channel = supabase.channel('user_${userId}_events');
channel.onPostgresChanges(
  event: PostgresChangeEvent.all,
  schema: 'public',
  table: 'wardrobe_items',
  filter: PostgresChangeFilter(
    type: PostgresChangeFilterType.eq,
    column: 'user_id',
    value: supabase.auth.currentUser!.id,
  ),
  callback: (payload) {
    // Update UI when items change (new item added, favorite toggled)
    emit(WardrobeUpdated(items: updatedItems));
  },
).subscribe();
```

---

## 2. DESGLOSE DE TRABAJO POR COMPONENTE

### 2.1 Core Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **JWT Auth System** | Login, register, refresh tokens, password reset | Medium | 16 | Pydantic, passlib, PyJWT | Unit + integration tests for all flows |
| **OAuth Integration** | Google + Apple sign-in | Hard | 20 | google-auth-oauthlib, Firebase Auth | Mock OAuth providers, integration tests |
| **Supabase Setup** | Database schema, RLS policies, migrations | Medium | 12 | Supabase CLI | SQL verification, policy testing |
| **API Client (Dio)** | HTTP client with interceptors, auth headers | Easy | 8 | Dio, retrofit | Mock API tests |
| **Image Upload** | File validation, resize, compression | Easy | 10 | Pillow/image_rs, Supabase Storage | Unit tests for resize logic |
| **Rate Limiting** | 100 req/min per user, 10K req/sec total | Medium | 8 | slowapi | Load tests, spike tests |

**Subtotal: 74 horas**

### 2.2 Body Analysis Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Body Photo Upload** | Camera + gallery picker, preview | Easy | 8 | image_picker, cached_network_image | Widget tests |
| **Google Vision API Integration** | Detect pose, colors, body landmarks | Hard | 24 | google-cloud-vision, numpy | Integration tests with real API |
| **Body Shape Classification** | Map landmarks to shape (pear, apple, etc.) | Medium | 12 | scipy (for geometric calculations) | Unit tests with sample landmarks |
| **Color Palette Extraction** | Extract dominant colors from body photo | Medium | 10 | PIL, scikit-image | Unit tests with test images |
| **Measurement Input Form** | Manual height, weight, measurements | Easy | 6 | Pydantic validators | Widget tests |
| **Analysis History UI** | Display past analyses, trend tracking | Easy | 8 | flutter_bloc, Supabase Realtime | Widget tests |

**Subtotal: 68 horas**

### 2.3 Wardrobe Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Clothing Upload + Auto-Categorize** | Image + Google Vision API for category, color, pattern | Hard | 28 | google-cloud-vision, FastAPI storage | Integration tests, image test set |
| **Wardrobe Grid UI** | Display all items with filters (category, color, size) | Medium | 14 | flutter_bloc, cached_network_image | Widget tests, lazy loading tests |
| **Item Detail Page** | Edit metadata (color, brand, size, price) | Easy | 8 | Pydantic schemas | Widget tests |
| **Search + Filter Logic** | Full-text search on item names, brands | Medium | 12 | PostgreSQL full-text search (GIN index) | Unit + integration tests |
| **Favorites System** | Mark items as favorite, filter to favorites | Easy | 6 | Supabase RLS policies | Unit tests |
| **Archive/Delete Items** | Soft delete, recovery option | Easy | 6 | Supabase transactions | Unit tests |

**Subtotal: 74 horas**

### 2.4 Virtual Try-On Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Try-On Request Endpoint** | Orchestrate user body photo + item image → Replicate API | Hard | 20 | replicate-python SDK | Integration tests with mock Replicate |
| **Replicate API Integration** | Handle model inference, polling for results, error retry | Hard | 16 | replicate, async queue | Integration tests, timeout handling |
| **Try-On Result UI** | Display before/after, save/share result | Medium | 10 | flutter_cached_network_image, share_plus | Widget tests |
| **Try-On History** | List all past try-ons, delete old results | Easy | 8 | Supabase pagination | Unit + integration tests |
| **Queue System** | Handle high concurrency of try-on requests (queue them) | Hard | 24 | Celery or n8n | Load tests, queue tests |

**Subtotal: 78 horas**

### 2.5 Recommendations Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Claude API Integration** | Prompt engineering for recommendations, streaming | Hard | 20 | anthropic SDK, prompt templates | Integration tests, prompt validation |
| **Chat-like UI** | Real-time chat interface in Flutter | Medium | 12 | flutter_bloc, auto_scroll_text | Widget tests |
| **Recommendation Caching** | Cache recommendations to reduce API costs | Medium | 8 | Redis pattern, Supabase | Unit tests |
| **Suggestion Item Linking** | Link recommendations back to wardrobe items | Easy | 8 | Dart matching logic | Unit tests |

**Subtotal: 48 horas**

### 2.6 Subscription + Payment Components

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Stripe Subscription Setup** | Create checkout session, manage plans | Hard | 20 | stripe, Pydantic | Integration tests with Stripe test API |
| **Mercado Pago Integration** | Alternative payment for Latin America | Hard | 18 | mercadopago SDK | Integration tests |
| **Webhook Handlers** | Process subscription events (created, renewed, cancelled) | Medium | 12 | FastAPI background tasks | Webhook simulation tests |
| **Feature Gating** | Restrict features to premium users | Easy | 6 | Pydantic decorators | Unit tests |
| **Subscription UI** | Display plans, prices, upgrade button | Easy | 8 | flutter_stripe, Dart models | Widget tests |

**Subtotal: 64 horas**

### 2.7 Analytics + Monitoring

| Componente | Descripción | Dificultad | Horas | Dependencias | Testing |
|------------|-------------|-----------|-------|--------------|---------|
| **Event Tracking** | Log wardrobe uploads, try-ons, recommendations | Easy | 8 | Supabase analytics table | Unit tests |
| **DAU/MAU Metrics** | Daily/monthly active users | Easy | 6 | SQL aggregations | Integration tests |
| **Funnel Analysis** | Signup → body analysis → wardrobe → tryon → paid | Medium | 10 | Supbase views or dbt | SQL tests |
| **Error Logging** | Sentry or Datadog for production errors | Medium | 10 | sentry-sdk, structured logging | Integration tests |

**Subtotal: 34 horas**

### 2.8 QA + Testing

| Componente | Descripción | Dificultad | Horas |
|------------|-------------|-----------|-------|
| **Unit Tests** | 80%+ coverage for services, repositories, usecases | Medium | 40 |
| **Integration Tests** | APIs with real Supabase, external APIs (mocked) | Hard | 40 |
| **E2E Tests** | Full user flows (signup → upload → tryon → pay) | Hard | 30 |
| **Load Testing** | 50K concurrent users, 1K users/sec signup spike | Hard | 20 |
| **Security Testing** | OWASP Top 10 audit, RLS verification, JWT validation | Hard | 20 |

**Subtotal: 150 horas**

---

## 3. TIMELINE REALISTA POR SPRINT (14 semanas)

### Sprint 0: Week 1 — Architecture + Setup (Foundation)
**Goal:** Production-ready infrastructure, no features yet.

**Tasks:**
- Supabase project setup + database schema migration
- FastAPI + Uvicorn + Docker Dockerfile
- Flutter project init + folder structure + DI setup
- GitHub Actions CI/CD (auto-test on push)
- Stripe + Mercado Pago sandbox accounts
- Google Cloud Vision credentials
- Sentry project for error tracking
- Deployment to Railway (backend) + Firebase Hosting (web marketing)

**Deliverables:**
- `POST /api/v1/health` returns `{"status": "ok"}`
- Flutter app builds without errors
- Database migrations tracked in version control
- CI/CD pipeline runs unit tests on every PR

**Hours: 60 (Sasha 40, Brook 20 for Flutter setup)**

---

### Sprint 1: Week 2-3 — Auth + User Management

**Tasks:**
- Implement JWT auth (login, register, refresh, logout)
- Password hashing + validation
- Email verification (optional for MVP)
- Google OAuth flow
- User profile management (CRUD)
- User preferences (body shape, budget, colors)
- RLS policies for all user-related tables
- Flutter auth screens (login, register, onboarding)
- Secure token storage (Hive local database)

**Deliverables:**
- `POST /api/v1/auth/register` + `POST /api/v1/auth/login`
- JWT tokens issued + refresh working
- Flutter login/register flows complete
- Tests: 100% coverage for auth service

**Hours: 80 (Sasha 50, Brook 30 for Flutter UI)**

---

### Sprint 2: Week 4-5 — Body Analysis Feature

**Tasks:**
- Google Vision API integration for pose detection
- Body shape classification algorithm
- Color palette extraction
- Body measurements input form
- API endpoint for body photo upload
- Flutter camera UI + image picker
- Body analysis result page (display shape, colors, tips)
- Store analysis results in Supabase
- Analysis history endpoint + UI

**Deliverables:**
- `POST /api/v1/analysis/upload` processes image + returns analysis
- Flutter app can capture body photo → see results
- Body shape classification 90%+ accurate on test set
- Tests: Integration tests with real Google Vision API

**Hours: 90 (Sasha 55, Brook 35 for Flutter UI)**

---

### Sprint 3: Week 6-7 — Wardrobe Management

**Tasks:**
- Clothing item model + CRUD endpoints
- Google Vision integration for auto-categorization
- Image upload to Supabase Storage
- Wardrobe grid UI with pagination
- Filter by category, color, season
- Search (full-text search on Postgres)
- Item detail page + edit form
- Favorites system
- RLS policies for wardrobe_items

**Deliverables:**
- `POST /api/v1/wardrobe/upload` + auto-categorization working
- `GET /api/v1/wardrobe?category=shirt&color=blue` returns filtered items
- Flutter wardrobe grid displays all items with lazy loading
- Upload + categorization takes <5 seconds per item
- Tests: Integration tests, image processing tests

**Hours: 100 (Sasha 50, Brook 50 for Flutter grid + upload UI)**

---

### Sprint 4: Week 8 — Outfit Builder

**Tasks:**
- Outfit model + CRUD
- Outfit builder UI (drag-drop items)
- Body model preview (simple 2D render)
- Save outfit
- Rating system
- Outfit history + delete

**Deliverables:**
- Users can create, view, edit outfits
- Flutter UI is smooth + responsive
- Tests: Widget tests for outfit builder

**Hours: 50 (Sasha 15, Brook 35 for Flutter UI)**

---

### Sprint 5: Week 9-10 — Virtual Try-On

**Tasks:**
- Replicate API integration
- Try-on request queuing (handle concurrency)
- Poll for Replicate job completion
- Store try-on results
- Try-on result UI (before/after)
- Error handling + retry logic
- Load testing (ensure 1K concurrent requests don't break)

**Deliverables:**
- `POST /api/v1/tryons` triggers Replicate inference
- Try-on results display in <60 seconds
- Queue system handles 1K concurrent requests
- Tests: Integration tests with mock Replicate, load tests

**Hours: 110 (Sasha 80, Brook 30 for Flutter result UI)**

---

### Sprint 6: Week 11 — Recommendations (Claude API)

**Tasks:**
- Claude API integration + prompt engineering
- Recommendation caching (to reduce costs)
- Chat UI in Flutter
- Link recommendations to wardrobe items
- Stream responses in real-time

**Deliverables:**
- `POST /api/v1/recommendations` returns AI outfit suggestions
- Chat interface is responsive + real-time
- Caching reduces Claude API calls by 70%
- Tests: Integration tests, prompt validation

**Hours: 60 (Sasha 40, Brook 20 for Flutter chat UI)**

---

### Sprint 7: Week 12 — Subscriptions + Payment

**Tasks:**
- Stripe subscription setup + pricing page
- Mercado Pago integration
- Webhook handlers for payment events
- Feature gating (restrict premium features)
- Subscription management UI (upgrade, cancel)
- Plan comparison UI

**Deliverables:**
- Stripe checkout working in sandbox
- Mercado Pago checkout working
- Premium features gated correctly
- Tests: Integration tests with Stripe test API

**Hours: 80 (Sasha 50, Brook 30 for Flutter subscription UI)**

---

### Sprint 8: Week 13 — Polishing + Performance + Analytics

**Tasks:**
- Analytics event tracking
- DAU/MAU dashboards (Supbase + Metabase)
- Error logging (Sentry)
- Performance optimization (image caching, lazy loading)
- Accessibility improvements (Flutter a11y)
- Localization (Spanish, English)
- App store preparation (screenshots, description)

**Deliverables:**
- Analytics dashboard shows key metrics
- Sentry errors are tracked + alerted
- App loads <3 seconds on 4G
- Tests: 80%+ code coverage

**Hours: 70 (Sasha 30, Brook 40)**

---

### Sprint 9: Week 14 — Launch Preparation + Soft Launch

**Tasks:**
- Final bug fixes + edge cases
- Load testing at 50K users
- Security audit (OWASP)
- Soft launch (100 beta users)
- Monitor errors, performance
- Prepare App Store + Google Play submissions

**Deliverables:**
- Zero critical bugs
- Load tests pass with 50K users
- App deployed to production
- Beta feedback collected + addressed

**Hours: 60 (Sasha 20, Brook 30, Erik 10 for visual polish)**

---

## 4. INFRAESTRUCTURA + COSTOS

### 4.1 Hosting + Database

| Servicio | Plan | Costo/mes | Detalle |
|----------|------|-----------|---------|
| **Supabase** | Pro | $25 + usage | 100K MAU, 8GB DB, 100GB storage base |
| **Supabase MAU Overage** | $3.25 per 1K | $162.50 at 50K users | 50K - 100K = $325/mo |
| **Railway (Backend)** | Pro | $20 + usage | 512MB RAM, 1CPU base |
| **Firebase Hosting** | Pay-as-you-go | $1-5 | Marketing website only |
| **Cloudflare CDN** | Free + Paid | $0-20 | Image caching + DDoS protection |

**Monthly Infrastructure Cost (50K users):**
- Supabase: $25 + $325 (overages) = **$350**
- Railway: $20 + $50 (egress) = **$70**
- Firebase: **$5**
- Cloudflare: **$10**
- **Total: $435/month at 50K users**

**Scaling to 500K users:**
- Supabase: $25 + $1,625 (overages) = **$1,650**
- Database compute upgrade (2-core): **+$110**
- Railway upgrade (2GB RAM): **$100 + $150 egress = $250**
- **Total: $2,010/month at 500K users**

### 4.2 API Costs (per month, 50K users)

| API | Usage | Price/Unit | Monthly Cost |
|-----|-------|-----------|--------------|
| **Google Vision** | 200K requests (4/item) | $1.50 per 1K | **$300** |
| **Replicate Try-On** | 250K tryons (5/user) | $0.02 per | **$5,000** |
| **Claude API** | 100K recommendations | $3 per 1M tokens | **$90** |
| **Stripe** | 10% of users upgrade | 2.9% + $0.30 | **$225** (at $4.99 avg) |
| **Sentry** | Error tracking | Free tier | **$0** |

**Total API Costs (50K users): $5,615/month**

**Cost Breakdown by User:**
- Per-user monthly revenue (10% premium × $6.50 avg): **$0.65**
- Per-user monthly cost (infra + APIs): **$0.11 + $0.11 = $0.22**
- **Gross margin per premium user: $0.43 (66%)**

### 4.3 Revenue Model (Freemium)

| Tier | Price | Features | Conversion Target |
|------|-------|----------|-------------------|
| **Free** | $0 | 1 body analysis, 5 wardrobe items, 1 tryon/month | 90% of users |
| **Premium Monthly** | $4.99 | Unlimited items, 50 tryons/month, AI recommendations | 8% |
| **Premium Annual** | $49.99 | Same as monthly, 17% discount | 2% |

**Revenue at 50K users:**
- 50K × 10% × $5.80 avg (mix of monthly/annual) = **$29,000/month**
- Less API costs ($5,615) = **$23,385 gross profit**
- Less team salary (1 senior eng) ≈ $-15,000 = **$8,385 net** (tight, but viable for MVP phase)

**Break-even: ~15K users at 10% conversion**

### 4.4 Scaling Strategy (How to Grow to 50K Without Breaking Infra)

**Phase 1 (Days 1-7): 1K → 5K users**
- Vertical scaling (upgrade Supabase to higher compute)
- Replicate try-on queue with timeout (prevent hanging requests)
- Image caching + CDN for Supabase Storage

**Phase 2 (Week 2-4): 5K → 25K users**
- Add Supabase read replicas for heavy queries
- Implement database connection pooling (Supavisor)
- Cache recommendations (Redis pattern in Supabase)
- Rate limit API to 100 req/min per user

**Phase 3 (Month 2): 25K → 50K users**
- Consider moving to PostgreSQL + AWS RDS for lower per-user cost
- Implement image resizing + compression service (Cloudinary or self-hosted)
- Queue try-on requests → process asynchronously (Celery + Redis)

**Cost per 1K users:**
- Infrastructure: $8.70 (DB overages dominate)
- APIs: $112 (Replicate is 90% of cost)
- **Total: $120.70/1K users**

---

## 5. RIESGOS TÉCNICOS + PLANES DE MITIGACIÓN

### 5.1 Riesgos Críticos

| Riesgo | Probabilidad | Impacto | Mitigación | Timebox |
|--------|--------------|--------|-----------|---------|
| **Replicate API Errors** | High | Critical | Queue all requests, exponential backoff retry, fallback to static try-on template | Week 9 (Sprint 5) |
| **Supabase Performance Degradation** | Medium | Critical | Implement RLS indices, read replicas, connection pooling. Test at 50K MAU load. | Week 5 (Sprint 3) |
| **Google Vision API Rate Limits** | Medium | High | Batch requests, implement circuit breaker, cache results. Test with 100K requests/day. | Week 4 (Sprint 2) |
| **JWT Token Expiration Edge Cases** | High | Medium | Implement refresh token rotation, handle 401s in client gracefully. Test all scenarios. | Week 2 (Sprint 1) |
| **Image Upload Handling (Corrupted Files)** | Medium | Medium | Validate MIME types, file size limits, resize before storing. Quarantine bad uploads. | Week 6 (Sprint 3) |
| **Claude API Prompt Injection** | Low | High | Sanitize user input, use system prompts only, test with adversarial inputs. | Week 11 (Sprint 6) |
| **Stripe Webhook Failures** | Medium | High | Implement webhook signing, idempotency keys, retry logic. Monitor Stripe logs. | Week 12 (Sprint 7) |
| **Concurrent Try-On Requests (Bottleneck)** | High | High | Implement async queue (Celery/n8n), max 10 concurrent per user. Load test with 1K spike. | Week 10 (Sprint 5) |

### 5.2 Risk Response Plan

**If Replicate API becomes too expensive:**
- Use cheaper model (latency trade-off)
- Implement client-side filtering (only allow try-on for similar body types)
- Batch try-ons (not real-time, process in background)

**If Supabase can't handle 50K users:**
- Migrate to AWS RDS + Postgres (more predictable pricing)
- Implement read replicas for high-traffic queries
- Archive old analytics/tryons to S3

**If JWT refresh token rotation causes issues:**
- Extend access token lifetime (1 hour → 8 hours)
- Implement sliding window (auto-refresh on 75% expiry)
- Accept 24-hour refresh tokens for mobile

**If user acquisition is slower than 50K:**
- Reduce first week target to 10K
- Extend timeline by 2 weeks
- Focus on organic growth + influencer seeding

---

## 6. REQUISITOS.txt (Backend)

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
pydantic-settings>=2.3.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
supabase>=2.5.0
httpx>=0.27.0
python-multipart>=0.0.9
structlog>=24.0.0
slowapi>=0.1.9
google-cloud-vision>=3.6.0
anthropic>=0.34.0
replicate>=0.33.0
stripe>=11.1.0
mercadopago>=2.27.0
Pillow>=10.4.0
python-dotenv>=1.0.0

# Testing
pytest>=8.2.0
anyio[trio]>=4.4.0
pytest-anyio>=0.0.0
pytest-cov>=5.0.0
httpx>=0.27.0
```

---

## 7. PUBSPEC.yaml (Flutter)

```yaml
name: asesor_imagen_ai
description: AI-powered fashion advisor with virtual try-on.
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.4.0 <4.0.0'
  flutter: ^3.24.0

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.0
  equatable: ^2.0.0

  # Navigation
  go_router: ^14.0.0

  # Network
  dio: ^5.4.0
  supabase_flutter: ^2.5.0

  # DI
  get_it: ^7.6.0
  injectable: ^2.3.0

  # Functional
  dartz: ^0.10.1

  # Storage
  shared_preferences: ^2.2.0
  hive: ^2.2.0

  # UI
  flutter_screenutil: ^5.9.0
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0
  image_picker: ^1.0.0
  google_sign_in: ^6.2.0
  sign_in_with_apple: ^6.1.0
  flutter_stripe: ^12.0.0
  share_plus: ^7.2.0
  camera: ^0.10.0

  # Utils
  intl: ^0.19.0
  logger: ^2.4.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
  flutter_lints: ^3.0.0
  integration_test:
    sdk: flutter
```

---

## 8. Checklist de Arquitectura

- [ ] Database schema reviewed + indexed
- [ ] RLS policies tested (users can only see own data)
- [ ] API endpoints follow REST conventions
- [ ] JWT token lifecycle (expiry, refresh) documented
- [ ] All external APIs have error handling + retry logic
- [ ] Image processing (resize, compress) implemented
- [ ] Rate limiting configured per user + global
- [ ] Supabase Storage buckets created (avatars, wardrobe, tryons)
- [ ] Stripe + Mercado Pago webhook listeners implemented
- [ ] Sentry error tracking integrated
- [ ] GitHub Actions CI/CD pipeline running
- [ ] Load test script ready (k6, Locust)
- [ ] Security audit checklist (OWASP Top 10)
- [ ] Monitoring dashboards (Supabase, Sentry, custom)

---

## RESUMEN EJECUTIVO

**MVP de Asesor de Imagen AI en 14 semanas:**

- **Backend:** FastAPI (70 endpoints) + Supabase PostgreSQL + Realtime
- **Mobile:** Flutter (8 screens, Riverpod state management)
- **AI Integration:** Google Vision (body analysis) + Replicate (try-on) + Claude (recommendations)
- **Monetization:** Freemium ($4.99-8.99/mo)
- **Infrastructure:** Railway (backend) + Supabase (DB + auth + storage) + Firebase (marketing)
- **Team:** 1 senior backend (Sasha) + 1 senior frontend (Brook) + 1 designer (Erik)
- **Total Sprint Hours:** ~900 hours
- **Cost at 50K users:** $435/mo infra + $5,615/mo APIs = **$6,050/mo**
- **Revenue at 50K users:** **$29,000/mo** (10% × 50K × $5.80 avg)
- **Gross margin:** **$22,950/mo** (79%)
- **Riesgos principales:** Replicate API cost/availability, Supabase scaling, concurrent try-on bottleneck

**Milestone crítico:** 50K users en semana 1 requiere:
- Perfect infrastructure (no 503 errors)
- Aggressive marketing (influencers, TikTok, Instagram)
- Referral loop (incentivize sign-ups)
- Zero downtime deployment

Este documento es la **especificación técnica definitiva** para que Sasha construya sin ambigüedades.

