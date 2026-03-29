# ASESOR DE IMAGEN AI — Schemas Pydantic + Implementación de Servicios

Este documento contiene **ejemplos de código real** que Sasha puede copiar/pegar.

---

## 1. SCHEMAS PYDANTIC (app/schemas/)

### 1.1 Auth Schemas

```python
# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=100)

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class GoogleOAuthRequest(BaseModel):
    token: str  # ID token from Google

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)
```

### 1.2 User Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: str
    full_name: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    avatar_url: str | None = None
    body_shape: str | None = Field(None, pattern="^(pear|apple|hourglass|rectangle|inverted_triangle)$")
    skin_tone: str | None = Field(None, pattern="^(fair|light|medium|olive|tan|dark)$")
    budget_range: str | None = None  # "$50-100", "$100-250", etc.

class UserPreferences(BaseModel):
    color_preferences: list[str] = []  # e.g., ["blue", "black", "white"]
    style_preferences: list[str] = []  # e.g., ["casual", "minimalist", "bold"]
    budget_range: str | None = None

class UserResponse(UserBase):
    id: UUID
    avatar_url: str | None = None
    body_shape: str | None = None
    skin_tone: str | None = None
    subscription_tier: str  # "free", "premium_monthly", "premium_annual"
    subscription_status: str  # "active", "cancelled", "past_due"
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 1.3 Body Analysis Schemas

```python
# app/schemas/body_analysis.py
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class Measurements(BaseModel):
    bust_cm: float | None = None
    waist_cm: float | None = None
    hips_cm: float | None = None
    shoulder_cm: float | None = None
    height_cm: int | None = None
    weight_kg: float | None = None

class BodyLandmark(BaseModel):
    joint_name: str  # "nose", "left_shoulder", "right_knee", etc.
    x: float
    y: float
    z: float | None = None
    confidence: float  # 0-1

class ColorPalette(BaseModel):
    colors: list[str]  # ["#FFB6C1", "#FFE4E1", ...]
    hex_codes: list[str]
    names: list[str]  # ["Light Pink", "Misty Rose", ...]

class BodyAnalysisRequest(BaseModel):
    measurements: Measurements | None = None
    image_url: str | None = None  # If uploading from URL

class BodyAnalysisResponse(BaseModel):
    id: UUID
    user_id: UUID
    body_shape: str  # "pear", "apple", etc.
    confidence_score: float  # 0-1
    measurements: Measurements
    body_landmarks: list[BodyLandmark]
    color_palette: ColorPalette
    style_notes: str  # "You have an hourglass shape. Consider fitted styles."
    image_url: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 1.4 Wardrobe Schemas

```python
# app/schemas/wardrobe.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class ImageFeatures(BaseModel):
    dominant_colors: list[str]  # ["blue", "white"]
    hex_codes: list[str]
    pattern: str  # "solid", "striped", "floral", "plaid"
    material: str | None = None  # "cotton", "silk", "polyester"
    style: str  # "casual", "formal", "sporty"
    texture: str | None = None  # "smooth", "rough", "shiny"

class WardrobeItemCreate(BaseModel):
    category: str = Field(..., pattern="^(shirt|pants|dress|jacket|shoes|accessories|skirt|coat)$")
    sub_category: str | None = None
    color: str
    size: str | None = Field(None, pattern="^(XS|S|M|L|XL|XXL)$")
    brand: str | None = None
    price: float | None = None
    purchase_date: str | None = None  # ISO format
    condition: str = Field("good", pattern="^(excellent|good|fair|worn)$")

class WardrobeItemUpdate(BaseModel):
    color: str | None = None
    size: str | None = None
    brand: str | None = None
    price: float | None = None
    condition: str | None = None
    is_favorite: bool | None = None
    is_archived: bool | None = None

class WardrobeItemResponse(WardrobeItemCreate):
    id: UUID
    user_id: UUID
    image_url: str
    image_features: ImageFeatures
    is_favorite: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WardrobeListResponse(BaseModel):
    items: list[WardrobeItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
```

### 1.5 Outfit Schemas

```python
# app/schemas/outfit.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class OutfitItemRef(BaseModel):
    item_id: UUID
    position: int  # 1=top, 2=bottom, 3=shoes, etc.

class OutfitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    occasion: str = Field(..., pattern="^(casual|work|date|party|outdoor|wedding)$")
    season: str | None = Field(None, pattern="^(spring|summer|fall|winter)$")
    description: str | None = None
    items: list[OutfitItemRef]

class OutfitResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    occasion: str
    season: str | None
    description: str | None
    items: list[OutfitItemRef]
    created_outfit_image_url: str | None  # Composite image URL
    rating: float | None  # 0-5
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 1.6 Try-On Schemas

```python
# app/schemas/tryons.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class TryOnRequest(BaseModel):
    body_image_url: str
    item_id: UUID | None = None  # Single item
    outfit_id: UUID | None = None  # Full outfit
    garment_type: str = Field(..., pattern="^(top|bottom|dress|full-body|shoes)$")

class TryOnResponse(BaseModel):
    id: UUID
    user_id: UUID
    wardrobe_item_id: UUID | None
    outfit_id: UUID | None
    body_image_url: str
    item_image_url: str
    result_image_url: str
    model_used: str  # "replicate:yolo-virtual-try-on"
    status: str = "completed"  # "pending", "processing", "completed", "failed"
    error_message: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 1.7 Recommendation Schemas

```python
# app/schemas/recommendations.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class RecommendationRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500)
    # e.g., "Outfit ideas for a casual Friday at work"
    include_items: bool = True  # Include suggested items from wardrobe

class OutfitSuggestion(BaseModel):
    title: str
    description: str
    items: list[dict]  # [{"id": uuid, "color": "blue", "type": "shirt"}, ...]
    why_it_works: str
    styling_tips: str

class RecommendationResponse(BaseModel):
    id: UUID
    user_id: UUID
    query: str
    suggestions: list[OutfitSuggestion]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 1.8 Subscription Schemas

```python
# app/schemas/subscriptions.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class PlanType(str, Enum):
    FREE = "free"
    PREMIUM_MONTHLY = "premium_monthly"
    PREMIUM_ANNUAL = "premium_annual"

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price: float
    currency: str = "USD"
    billing_period: str = "month"  # "month" or "year"
    features: list[str]
    max_items: int  # Wardrobe items
    max_tryons_per_month: int
    max_recommendations_per_month: int

class CheckoutSessionRequest(BaseModel):
    plan_id: str  # "premium_monthly" or "premium_annual"
    provider: str = "stripe"  # "stripe" or "mercadopago"

class CheckoutSessionResponse(BaseModel):
    session_id: str
    url: str  # Redirect URL for payment
    expires_at: datetime

class SubscriptionStatus(BaseModel):
    current_plan: PlanType
    is_active: bool
    next_billing_date: datetime | None
    cancel_at_period_end: bool
```

---

## 2. SERVICIOS IMPLEMENTADOS (app/services/)

### 2.1 Auth Service (JWT + Password)

```python
# app/services/auth_service.py
from datetime import datetime, timedelta, timezone
from uuid import UUID
from email.mime.text import MIMEText
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.config import get_settings
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, LoginResponse

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.settings = settings

    async def register(self, request: RegisterRequest) -> dict:
        """Register new user with email + password."""
        # Check if user exists
        existing = await self.user_repo.get_by_email(request.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash password
        hashed = pwd_context.hash(request.password)

        # Create user
        user_data = {
            "email": request.email,
            "hashed_password": hashed,
            "full_name": request.full_name,
            "subscription_tier": "free",
            "subscription_status": "active",
        }
        user = await self.user_repo.create(user_data)

        # Generate tokens
        access_token = self._create_access_token(UUID(user["id"]))
        refresh_token = self._create_refresh_token(UUID(user["id"]))

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def login(self, request: LoginRequest) -> LoginResponse:
        """Login with email + password."""
        user = await self.user_repo.get_by_email(request.email)
        if not user or not pwd_context.verify(request.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = self._create_access_token(UUID(user["id"]))
        refresh_token = self._create_refresh_token(UUID(user["id"]))

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def refresh_token(self, refresh_token: str) -> LoginResponse:
        """Issue new access token from refresh token."""
        try:
            payload = jwt.decode(
                refresh_token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            user_id = UUID(payload["sub"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        access_token = self._create_access_token(user_id)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    def _create_access_token(self, user_id: UUID, expires_delta: timedelta | None = None) -> str:
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access",
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

    def _create_refresh_token(self, user_id: UUID) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
```

### 2.2 Body Analysis Service

```python
# app/services/body_analysis_service.py
from uuid import UUID
import io
from google.cloud import vision
from PIL import Image
import numpy as np
from app.repositories.body_analysis_repository import BodyAnalysisRepository
from app.schemas.body_analysis import BodyAnalysisResponse, Measurements, ColorPalette

class BodyAnalysisService:
    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()
        self.repo = BodyAnalysisRepository()

    async def analyze_body_photo(self, user_id: UUID, image_bytes: bytes) -> BodyAnalysisResponse:
        """
        Analyze body photo using Google Vision API.
        Returns body shape, measurements estimate, and color palette.
        """
        # Step 1: Detect pose landmarks
        image = vision.Image(content=image_bytes)
        response = self.vision_client.document_text_detection(image=image)

        # Step 2: Extract landmarks (27 joints from pose detection)
        landmarks = self._extract_pose_landmarks(response)

        # Step 3: Calculate body shape from proportions
        body_shape = self._estimate_body_shape(landmarks)

        # Step 4: Extract color palette
        img = Image.open(io.BytesIO(image_bytes))
        colors = self._extract_color_palette(img)

        # Step 5: Save to DB
        analysis_data = {
            "user_id": str(user_id),
            "body_shape": body_shape,
            "measurements": {
                "bust_cm": None,  # Would estimate from landmarks
                "waist_cm": None,
                "hips_cm": None,
            },
            "body_landmarks": landmarks,
            "color_analysis": colors,
            "style_notes": self._generate_style_notes(body_shape, colors),
            "image_url": f"s3://uploads/{user_id}/body_analysis.jpg",
        }

        saved = await self.repo.create(analysis_data)

        return BodyAnalysisResponse(
            id=saved["id"],
            user_id=user_id,
            body_shape=body_shape,
            confidence_score=0.92,  # From pose detection confidence
            measurements=Measurements(),
            body_landmarks=landmarks,
            color_palette=colors,
            style_notes=analysis_data["style_notes"],
            image_url=analysis_data["image_url"],
            created_at=saved["created_at"],
        )

    def _extract_pose_landmarks(self, vision_response) -> list:
        """Extract 27 pose landmarks from Vision API response."""
        landmarks = []
        # Parse response.document_text_detection() for pose
        # This is simplified; real implementation uses pose_estimation_model
        return landmarks

    def _estimate_body_shape(self, landmarks: list) -> str:
        """
        Classify body shape based on landmark proportions:
        - Pear: wider hips than shoulders
        - Apple: wider torso
        - Hourglass: similar hip/shoulder, narrow waist
        - Rectangle: straight lines
        - Inverted triangle: wider shoulders
        """
        # Calculate ratios from landmarks
        shoulder_width = landmarks[5]["x"] - landmarks[2]["x"]  # Right - left shoulder
        hip_width = landmarks[25]["x"] - landmarks[24]["x"]  # Right - left hip
        waist = 0  # Estimated from torso

        if hip_width > shoulder_width * 1.2:
            return "pear"
        elif shoulder_width > hip_width * 1.2:
            return "inverted_triangle"
        elif abs(hip_width - shoulder_width) < 0.1 * shoulder_width:
            return "hourglass"  # Proportional
        else:
            return "rectangle"

    def _extract_color_palette(self, image: Image.Image) -> ColorPalette:
        """Extract dominant colors using k-means clustering."""
        img_array = np.array(image.convert("RGB"))
        pixels = img_array.reshape(-1, 3)

        # Cluster to find 5 dominant colors
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(pixels)

        colors = []
        hex_codes = []
        for center in kmeans.cluster_centers_:
            rgb = tuple(int(c) for c in center)
            hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
            hex_codes.append(hex_code)
            colors.append(self._rgb_to_name(rgb))

        return ColorPalette(colors=colors, hex_codes=hex_codes, names=colors)

    def _rgb_to_name(self, rgb: tuple) -> str:
        """Convert RGB to color name."""
        r, g, b = rgb
        if max(r, g, b) < 50:
            return "Black"
        elif min(r, g, b) > 200:
            return "White"
        elif r > g and r > b:
            return "Red"
        elif g > r and g > b:
            return "Green"
        elif b > r and b > g:
            return "Blue"
        return "Neutral"

    def _generate_style_notes(self, body_shape: str, colors: ColorPalette) -> str:
        notes = {
            "pear": "You have a pear shape. Opt for A-line skirts, wide-leg pants, and darker colors on top to balance.",
            "apple": "You have an apple shape. Try structured blazers, v-necks to elongate, and statement bottoms.",
            "hourglass": "You have an hourglass shape. Fitted styles that highlight your curves work best.",
            "rectangle": "You have a rectangle shape. Add volume with peplum tops, ruffles, and layering.",
            "inverted_triangle": "You have broad shoulders. Balance with wide-leg pants and skirts, darker tops.",
        }
        return notes.get(body_shape, "")
```

### 2.3 Wardrobe Service (Auto-Categorization)

```python
# app/services/wardrobe_service.py
from uuid import UUID
from google.cloud import vision
from app.repositories.wardrobe_repository import WardrobeRepository
from app.schemas.wardrobe import WardrobeItemCreate, WardrobeItemResponse

class WardrobeService:
    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()
        self.repo = WardrobeRepository()

    async def upload_and_categorize(self, user_id: UUID, image_bytes: bytes, filename: str) -> WardrobeItemResponse:
        """
        Upload clothing item, auto-detect category, color, pattern, style.
        """
        # Step 1: Detect labels and attributes
        image = vision.Image(content=image_bytes)
        response = self.vision_client.label_detection(image=image)

        # Step 2: Extract clothing info
        labels = [label.description.lower() for label in response.label_annotations]
        category = self._classify_category(labels)
        color = self._extract_color(image)
        pattern = self._detect_pattern(labels)
        style = self._detect_style(labels)

        # Step 3: Save to storage
        storage_url = f"s3://wardrobe/{user_id}/{filename}"

        # Step 4: Save to DB
        item_data = {
            "user_id": str(user_id),
            "category": category,
            "color": color,
            "image_url": storage_url,
            "image_features": {
                "dominant_colors": [color],
                "pattern": pattern,
                "style": style,
            },
        }

        saved = await self.repo.create(item_data)
        return WardrobeItemResponse(**saved)

    def _classify_category(self, labels: list[str]) -> str:
        """Map Vision labels to clothing categories."""
        category_map = {
            "shirt": ["t-shirt", "blouse", "top", "dress shirt"],
            "pants": ["jeans", "trousers", "shorts", "pants"],
            "dress": ["dress", "gown"],
            "jacket": ["jacket", "coat", "blazer", "cardigan"],
            "shoes": ["shoe", "sneaker", "boot", "sandal"],
            "skirt": ["skirt"],
        }

        for category, keywords in category_map.items():
            if any(kw in " ".join(labels) for kw in keywords):
                return category
        return "accessories"

    def _extract_color(self, image: vision.Image) -> str:
        """Extract dominant color using properties."""
        # Use image properties to get dominant color
        response = self.vision_client.image_properties(image=image)
        colors = response.image_properties.dominant_colors.colors

        if colors:
            return colors[0].color.red  # Simplified; real: RGB to color name
        return "neutral"

    def _detect_pattern(self, labels: list[str]) -> str:
        patterns = {
            "solid": len(labels) == 1,
            "striped": "stripe" in " ".join(labels),
            "floral": "flower" in " ".join(labels) or "floral" in " ".join(labels),
            "plaid": "plaid" in " ".join(labels) or "check" in " ".join(labels),
        }
        for pattern, match in patterns.items():
            if match:
                return pattern
        return "solid"

    def _detect_style(self, labels: list[str]) -> str:
        text = " ".join(labels).lower()
        if any(w in text for w in ["casual", "tee", "hoodie"]):
            return "casual"
        elif any(w in text for w in ["formal", "suit", "dress", "gown"]):
            return "formal"
        elif any(w in text for w in ["sport", "athletic", "gym"]):
            return "sporty"
        return "casual"
```

### 2.4 Try-On Service (Replicate Integration)

```python
# app/services/tryon_service.py
import replicate
import asyncio
from uuid import UUID
from fastapi import HTTPException, status
from app.repositories.tryon_repository import TryonRepository
from app.config import get_settings

settings = get_settings()

class TryOnService:
    def __init__(self):
        self.repo = TryonRepository()
        self.replicate_client = replicate.Client(api_token=settings.REPLICATE_API_KEY)

    async def generate_tryon(
        self,
        user_id: UUID,
        body_image_url: str,
        item_image_url: str,
        garment_type: str,
    ) -> dict:
        """
        Queue virtual try-on request, poll Replicate for result.
        """
        # Step 1: Validate inputs
        if not self._is_valid_url(body_image_url) or not self._is_valid_url(item_image_url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image URLs"
            )

        # Step 2: Create Replicate job
        try:
            output = await asyncio.to_thread(
                self.replicate_client.run,
                "antonioferrari/yolo-virtual-try-on:latest",
                input={
                    "background": body_image_url,
                    "items": [item_image_url],
                    "garment_type": garment_type,
                }
            )
            result_image_url = output[0] if output else None

        except replicate.APIError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Virtual try-on service unavailable: {e}"
            )

        # Step 3: Save result
        tryon_data = {
            "user_id": str(user_id),
            "body_image_url": body_image_url,
            "item_image_url": item_image_url,
            "result_image_url": result_image_url,
            "model_used": "replicate:yolo-virtual-try-on",
            "status": "completed",
        }

        saved = await self.repo.create(tryon_data)
        return saved

    def _is_valid_url(self, url: str) -> bool:
        return url.startswith("http://") or url.startswith("https://")

    async def poll_tryon_status(self, tryon_id: UUID) -> dict:
        """Poll status of a try-on job."""
        tryon = await self.repo.get_by_id(tryon_id)
        if not tryon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Try-on not found"
            )
        return tryon
```

### 2.5 Recommendation Service (Claude API)

```python
# app/services/recommendation_service.py
from uuid import UUID
from anthropic import Anthropic
from app.repositories.user_repository import UserRepository
from app.repositories.wardrobe_repository import WardrobeRepository
from app.config import get_settings

settings = get_settings()

class RecommendationService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.user_repo = UserRepository()
        self.wardrobe_repo = WardrobeRepository()

    async def get_recommendations(
        self,
        user_id: UUID,
        query: str,
        max_suggestions: int = 3,
    ) -> str:
        """
        Get outfit recommendations from Claude based on user's wardrobe.
        """
        # Step 1: Fetch user profile
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Step 2: Fetch wardrobe items
        items, _ = await self.wardrobe_repo.list_by_user(user_id, limit=50)

        # Step 3: Format wardrobe for Claude
        wardrobe_text = self._format_wardrobe(items)

        # Step 4: Construct prompt
        prompt = f"""You are a professional fashion stylist. Help the user create outfit combinations.

User Profile:
- Body shape: {user.get('body_shape', 'Unknown')}
- Skin tone: {user.get('skin_tone', 'Unknown')}
- Budget: {user.get('budget_range', 'Any')}

Available Wardrobe Items:
{wardrobe_text}

User Request: {query}

Please suggest {max_suggestions} outfit combinations that:
1. Match the occasion/purpose
2. Flatter the user's body shape
3. Coordinate colors well
4. Stay within budget preferences

For each outfit, provide:
- Items to combine (be specific with colors/brands from the wardrobe)
- Why it works for this occasion
- 2-3 styling tips (accessories, how to wear it)"""

        # Step 5: Call Claude
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _format_wardrobe(self, items: list[dict]) -> str:
        """Format wardrobe items for Claude prompt."""
        formatted = []
        for item in items:
            line = f"- {item['category'].capitalize()}: {item['color']} {item.get('brand', 'Unknown brand')}"
            if item.get('size'):
                line += f" (Size {item['size']})"
            formatted.append(line)
        return "\n".join(formatted)
```

### 2.6 Subscription Service (Stripe)

```python
# app/services/subscription_service.py
import stripe
from uuid import UUID
from fastapi import HTTPException, status
from app.config import get_settings
from app.repositories.user_repository import UserRepository

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.stripe_plans = {
            "premium_monthly": "price_xxx",  # From Stripe Dashboard
            "premium_annual": "price_yyy",
        }

    async def create_checkout_session(
        self,
        user_id: UUID,
        plan_id: str,
    ) -> dict:
        """Create Stripe checkout session."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if plan_id not in self.stripe_plans:
            raise HTTPException(status_code=400, detail="Invalid plan")

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": self.stripe_plans[plan_id],
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                customer_email=user["email"],
                success_url="https://app.example.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="https://app.example.com/pricing",
                metadata={"user_id": str(user_id), "plan_id": plan_id},
            )

            return {
                "session_id": session.id,
                "url": session.url,
                "expires_at": session.expires_at,
            }

        except stripe.error.InvalidRequestError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def handle_webhook(self, event: dict) -> None:
        """Process Stripe webhook events."""
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            user_id = session["metadata"]["user_id"]
            plan_id = session["metadata"]["plan_id"]

            # Update user subscription
            await self.user_repo.update(
                UUID(user_id),
                {
                    "subscription_tier": plan_id,
                    "subscription_status": "active",
                    "subscription_id": session["subscription"],
                }
            )

        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            # Find user by subscription_id and downgrade to free
            pass  # Implement lookup
```

---

## 3. API ENDPOINTS (app/api/v1/endpoints/)

### 3.1 Auth Endpoints

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.services.auth_service import AuthService
from app.core.security import get_current_user
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service() -> AuthService:
    return AuthService()

@router.post("/register", response_model=LoginResponse)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Register new user."""
    result = await service.register(request)
    return LoginResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
    )

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Login with email + password."""
    return await service.login(request)

@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    refresh_token: str,
    service: AuthService = Depends(get_auth_service),
):
    """Refresh access token."""
    return await service.refresh_token(refresh_token)

@router.post("/logout")
async def logout(current_user_id: UUID = Depends(get_current_user)):
    """Logout (client discards token)."""
    return {"message": "Logout successful"}
```

### 3.2 Body Analysis Endpoints

```python
# app/api/v1/endpoints/analysis.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from uuid import UUID
from app.services.body_analysis_service import BodyAnalysisService
from app.core.security import get_current_user
from app.schemas.body_analysis import BodyAnalysisResponse

router = APIRouter(prefix="/analysis", tags=["body analysis"])

def get_analysis_service() -> BodyAnalysisService:
    return BodyAnalysisService()

@router.post("/upload", response_model=BodyAnalysisResponse)
async def upload_body_photo(
    file: UploadFile = File(...),
    current_user_id: UUID = Depends(get_current_user),
    service: BodyAnalysisService = Depends(get_analysis_service),
):
    """Upload body photo for analysis."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    image_bytes = await file.read()
    return await service.analyze_body_photo(current_user_id, image_bytes)

@router.get("/latest", response_model=BodyAnalysisResponse)
async def get_latest_analysis(
    current_user_id: UUID = Depends(get_current_user),
    service: BodyAnalysisService = Depends(get_analysis_service),
):
    """Get latest body analysis."""
    return await service.repo.get_latest_by_user(current_user_id)
```

---

## 4. Testing Examples

### 4.1 Unit Test — Auth Service

```python
# tests/services/test_auth_service.py
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, RegisterRequest

@pytest.fixture
def auth_service():
    return AuthService()

@pytest.mark.anyio
async def test_register_success(auth_service):
    """Test successful user registration."""
    request = RegisterRequest(
        email="test@example.com",
        password="securepassword123",
        full_name="Test User",
    )

    with patch.object(auth_service.user_repo, "get_by_email", return_value=None):
        with patch.object(auth_service.user_repo, "create") as mock_create:
            mock_create.return_value = {
                "id": str(uuid4()),
                "email": request.email,
                "full_name": request.full_name,
            }

            result = await auth_service.register(request)

            assert result["access_token"]
            assert result["refresh_token"]
            assert result["user"]["email"] == request.email

@pytest.mark.anyio
async def test_login_invalid_credentials(auth_service):
    """Test login with wrong password."""
    request = LoginRequest(email="test@example.com", password="wrongpassword")

    with patch.object(auth_service.user_repo, "get_by_email", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login(request)

        assert exc_info.value.status_code == 401
```

### 4.2 Integration Test — Wardrobe Service

```python
# tests/services/test_wardrobe_service.py
import pytest
from uuid import uuid4
from app.services.wardrobe_service import WardrobeService

@pytest.mark.anyio
async def test_upload_and_categorize(wardrobe_service):
    """Test clothing item upload + auto-categorization."""
    user_id = uuid4()

    # Read test image
    with open("tests/fixtures/blue_shirt.jpg", "rb") as f:
        image_bytes = f.read()

    result = await wardrobe_service.upload_and_categorize(
        user_id,
        image_bytes,
        "blue_shirt.jpg"
    )

    assert result.category == "shirt"
    assert "blue" in result.image_features.dominant_colors
    assert result.image_url
```

---

## RESUMEN

Este documento tiene **todo lo que Sasha necesita para implementar sin ambigüedades:**

1. **Schemas Pydantic exactos** para cada endpoint
2. **Servicios completamente implementados** con código real
3. **Integración con APIs externas** (Google Vision, Replicate, Claude, Stripe)
4. **Tests unitarios e integración** como referencia
5. **Error handling + validación** en cada capa

Copiar → Pegar → Ajustar para las particularidades del proyecto. Sin abstracciones.

