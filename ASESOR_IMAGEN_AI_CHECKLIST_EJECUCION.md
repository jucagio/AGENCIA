# ASESOR DE IMAGEN AI — Checklist de Ejecución por Sprint

**Proyecto de 14 semanas | MVP Freemium | 50K usuarios target semana 1**

Usar este documento para tracking diario. Marcar items con ✅ cuando estén completados.

---

## SPRINT 0: Week 1 — Architecture + Foundation

**Goal:** Production-ready infrastructure. 0 features.
**Horas:** 60
**Equipo:** Sasha (40h backend), Brook (20h frontend setup), Erik (environment)

### Infrastructure Setup

- [ ] Supabase project created + organization setup
- [ ] Database schema migrated (SQL migrations in version control)
- [ ] Auth tables + RLS policies configured
- [ ] Storage buckets created (avatars/, wardrobe/, tryons/)
- [ ] Connection pooling enabled (Supavisor)
- [ ] Backups configured (daily)
- [ ] Monitoring dashboard accessible (Supabase dashboard)

### Backend Setup

- [ ] FastAPI project scaffold created
- [ ] `requirements.txt` with all dependencies
- [ ] `config.py` with Pydantic BaseSettings (env vars)
- [ ] `main.py` with lifespan, middleware, exception handlers
- [ ] CORS configured for development
- [ ] `GET /health` endpoint returns `{"status": "ok"}`
- [ ] Docker container builds + runs locally
- [ ] Dockerfile optimized for production (slim base, multi-stage)

### Deployment

- [ ] Railway project created + connected to GitHub
- [ ] Auto-deploy on git push configured
- [ ] Environment variables secured (Railway secrets)
- [ ] Datadog/Sentry project created + integrated
- [ ] Error tracking + logging working
- [ ] Database backups tested

### Frontend Setup

- [ ] Flutter project created (`flutter create`)
- [ ] Folder structure set up (clean architecture)
- [ ] `.env` file template created (SUPABASE_URL, SUPABASE_KEY)
- [ ] `pubspec.yaml` with all dependencies
- [ ] Code generation setup (build_runner, injectable)
- [ ] App runs on Android emulator + iOS simulator
- [ ] Navigation structure (go_router) configured

### CI/CD Pipeline

- [ ] GitHub Actions workflow created
- [ ] Unit tests run on every push
- [ ] Code coverage report generated (>80% target)
- [ ] Linting rules configured (flutter analyze, dart fix)
- [ ] Build matrix for multiple platforms (web, Android, iOS)
- [ ] Deployments automated on merge to main

### Documentation

- [ ] Architecture diagram documented
- [ ] API spec (OpenAPI/Swagger) generated
- [ ] Development setup guide written
- [ ] Environment variables documented
- [ ] Database migration process documented

### Testing

- [ ] Test fixtures/test data created
- [ ] Supabase test mode enabled (for tests)
- [ ] Mock external APIs set up
- [ ] Database reset script created (`make reset-db`)

---

## SPRINT 1: Week 2-3 — Auth + User Management

**Goal:** Users can sign up, log in, manage profiles.
**Horas:** 80
**Equipo:** Sasha (50h), Brook (30h)

### Backend Auth

- [ ] JWT token generation working (access + refresh)
- [ ] Password hashing with bcrypt (passlib)
- [ ] `POST /api/v1/auth/register` implemented + tested
  - [ ] Email validation
  - [ ] Password strength validation (min 8 chars)
  - [ ] User creation in Supabase
  - [ ] Returns tokens
  - [ ] Tested: Happy path + duplicate email + weak password
- [ ] `POST /api/v1/auth/login` implemented + tested
  - [ ] Email + password validation
  - [ ] JWT issued
  - [ ] Tested: Valid creds + invalid creds + no user
- [ ] `POST /api/v1/auth/refresh` implemented
  - [ ] Refresh token → new access token
  - [ ] Old tokens invalidated (optional, depends on design)
- [ ] `GET /api/v1/auth/verify` implemented
  - [ ] Returns current user if token valid
- [ ] `POST /api/v1/auth/logout` endpoint
  - [ ] Client-side token discard (no server-side revocation for MVP)

### OAuth Integration (Google)

- [ ] Google OAuth credentials obtained
- [ ] `POST /api/v1/auth/login/google` endpoint
  - [ ] Accepts ID token from frontend
  - [ ] Verifies token with Google
  - [ ] Creates/updates user in Supabase
  - [ ] Returns access + refresh tokens
- [ ] Tested with Google OAuth test account

### User Profile Management

- [ ] User schema created (email, name, avatar, preferences)
- [ ] `GET /api/v1/users/me` endpoint
  - [ ] Returns current user profile
  - [ ] RLS policies verified
- [ ] `PATCH /api/v1/users/me` endpoint
  - [ ] Update full_name, avatar_url
  - [ ] Validation on all fields
  - [ ] Tested: Valid update + invalid data
- [ ] `DELETE /api/v1/users/me` endpoint
  - [ ] Soft delete user account
  - [ ] Cascade delete related data (optional for MVP)

### User Preferences

- [ ] User preferences table created
- [ ] `GET /api/v1/users/me/preferences` endpoint
- [ ] `PATCH /api/v1/users/me/preferences` endpoint
  - [ ] body_shape, skin_tone, color_preferences, budget_range
  - [ ] All validated

### RLS Policies

- [ ] `users` table RLS enabled
  - [ ] Users see only own profile
  - [ ] Users update only own profile
- [ ] `user_preferences` table RLS enabled
- [ ] Test RLS policies with multiple users

### Flutter Auth Screens

- [ ] Login screen UI
  - [ ] Email + password fields
  - [ ] Login button
  - [ ] Navigate to register screen
  - [ ] Loading state during request
  - [ ] Error handling + display
- [ ] Register screen UI
  - [ ] Email, password, full name fields
  - [ ] Form validation (real-time)
  - [ ] Register button
  - [ ] Error handling
- [ ] Onboarding screen
  - [ ] Body shape selection (radio buttons)
  - [ ] Skin tone selection
  - [ ] Budget range selection
  - [ ] Skip option
- [ ] Auth state management (BLoC)
  - [ ] AuthBloc with login/register/logout events
  - [ ] AuthState with initial/loading/authenticated/failure
  - [ ] Persistence of tokens (Hive local storage)

### Flutter Navigation

- [ ] Auth guard (redirect to login if not authenticated)
- [ ] Route guards tested
- [ ] Deep linking configured (for future)

### Testing

- [ ] Unit tests for AuthService (90%+ coverage)
  - [ ] test_register_success
  - [ ] test_register_duplicate_email
  - [ ] test_login_success
  - [ ] test_login_invalid_credentials
  - [ ] test_refresh_token
- [ ] Integration tests for endpoints
  - [ ] Test real Supabase (on staging DB)
- [ ] Flutter widget tests for auth screens
  - [ ] test_login_screen_renders
  - [ ] test_email_validation_error
  - [ ] test_login_button_disabled_empty_fields

---

## SPRINT 2: Week 4-5 — Body Analysis Feature

**Goal:** Users can upload body photo, get analysis (shape, colors).
**Horas:** 90
**Equipo:** Sasha (55h), Brook (35h)

### Backend — Google Vision Integration

- [ ] Google Cloud Vision API credentials obtained
- [ ] `app/services/body_analysis_service.py` created
- [ ] Pose detection implemented
  - [ ] Extract 27 landmarks from body photo
  - [ ] Confidence scores validated
- [ ] Body shape classification
  - [ ] Algorithm implemented (pear, apple, hourglass, rectangle, inverted_triangle)
  - [ ] Test with sample images (accuracy 90%+)
- [ ] Color palette extraction
  - [ ] KMeans clustering for 5 dominant colors
  - [ ] RGB → color names
- [ ] Database models created
  - [ ] body_analysis table
  - [ ] RLS policies

### Backend Endpoints

- [ ] `POST /api/v1/analysis/upload`
  - [ ] File upload + validation (max 5MB, image/* MIME type)
  - [ ] Call Google Vision
  - [ ] Save results to DB
  - [ ] Return BodyAnalysisResponse
  - [ ] Tested: Valid image + invalid file + oversized file
- [ ] `GET /api/v1/analysis/latest`
  - [ ] Return user's latest analysis
  - [ ] RLS verified
- [ ] `GET /api/v1/analysis/history`
  - [ ] Paginated list of past analyses
  - [ ] Order by created_at DESC
- [ ] `DELETE /api/v1/analysis/{id}`
  - [ ] Soft delete analysis record

### Image Processing

- [ ] Pillow integration for image resizing
- [ ] Image compression (reduce file size before Vision API)
- [ ] EXIF data removal (privacy)

### Flutter — Camera + Photo Picker

- [ ] Camera permission handling (iOS + Android)
- [ ] Camera screen UI
  - [ ] Live camera feed
  - [ ] Capture button
  - [ ] Switch front/back camera
  - [ ] Gallery picker fallback
- [ ] Image preview screen
  - [ ] Display captured photo
  - [ ] Crop tool (optional)
  - [ ] Confirm button
- [ ] Loading state during analysis

### Flutter — Analysis Result Screen

- [ ] Display body shape (with icon/illustration)
- [ ] Display color palette (color swatches)
- [ ] Display style notes (text)
- [ ] Display measurements (if available)
- [ ] Share result option
- [ ] Save to history

### Flutter — BLoC for Body Analysis

- [ ] BodyAnalysisBloc created
- [ ] Events: UploadPhoto, FetchHistory
- [ ] States: Initial, Loading, AnalysisComplete, Error
- [ ] Error handling + retry logic

### Testing

- [ ] Unit tests for BodyAnalysisService (90%+ coverage)
  - [ ] test_analyze_body_photo_success
  - [ ] test_extract_pose_landmarks
  - [ ] test_classify_body_shape (pear, apple, etc.)
  - [ ] test_extract_color_palette
- [ ] Integration tests with real Google Vision API
  - [ ] Test with 10 different body photos
  - [ ] Verify accuracy + performance
- [ ] Flutter widget tests
  - [ ] test_camera_screen_renders
  - [ ] test_analysis_result_displays_shape
  - [ ] test_color_palette_swatches_rendered

### Performance

- [ ] Image upload completes in <5 seconds
- [ ] Analysis results display in <2 seconds
- [ ] No memory leaks in camera widget

---

## SPRINT 3: Week 6-7 — Wardrobe Management

**Goal:** Users upload clothing items, auto-categorized, filterable.
**Horas:** 100
**Equipo:** Sasha (50h), Brook (50h)

### Backend — Wardrobe Service

- [ ] WardrobeItem model + database table created
- [ ] `app/services/wardrobe_service.py` created
- [ ] Auto-categorization with Vision API
  - [ ] Classify into: shirt, pants, dress, jacket, shoes, skirt, coat, accessories
  - [ ] 90%+ accuracy on test set
- [ ] Color extraction
- [ ] Pattern detection (solid, striped, floral, plaid)
- [ ] Style classification (casual, formal, sporty)
- [ ] RLS policies for wardrobe_items

### Backend Endpoints

- [ ] `POST /api/v1/wardrobe/upload`
  - [ ] File upload + validation
  - [ ] Call Vision API
  - [ ] Auto-categorize
  - [ ] Save to Supabase Storage
  - [ ] Store metadata in DB
  - [ ] Return WardrobeItemResponse
  - [ ] Tested: Valid image + invalid types + duplicates
- [ ] `GET /api/v1/wardrobe` (paginated list)
  - [ ] Pagination (page, page_size)
  - [ ] Default 20 items per page, max 100
  - [ ] Order by created_at DESC
- [ ] `GET /api/v1/wardrobe/{item_id}`
  - [ ] Return item details
- [ ] `PATCH /api/v1/wardrobe/{item_id}`
  - [ ] Update color, size, brand, price, condition
  - [ ] Validation on all fields
- [ ] `DELETE /api/v1/wardrobe/{item_id}`
  - [ ] Soft delete (is_archived = true)
- [ ] `GET /api/v1/wardrobe?category=shirt` (filter)
  - [ ] Filter by category
  - [ ] Filter by color
  - [ ] Filter by season
  - [ ] Combine filters
  - [ ] Tested: All filter combinations
- [ ] `GET /api/v1/wardrobe/search?q=blue%20shirt` (search)
  - [ ] Full-text search on item names, brands
  - [ ] PostgreSQL GIN index for performance
  - [ ] Tested: Search speed <200ms for 10K items
- [ ] `POST /api/v1/wardrobe/{item_id}/favorite`
  - [ ] Toggle favorite flag

### Storage Service

- [ ] Supabase Storage integration
  - [ ] Create signed URLs for uploads
  - [ ] Bucket policies configured
  - [ ] File path structure: `wardrobe/{user_id}/{item_id}.jpg`
- [ ] Image resizing before storage
  - [ ] Max width 1024px
  - [ ] Max height 1024px
  - [ ] JPEG quality 85%
- [ ] Tested: Upload + download works

### Flutter — Wardrobe Grid

- [ ] Wardrobe screen UI
  - [ ] Grid view (2 columns)
  - [ ] Lazy loading (infinite scroll)
  - [ ] Each item shows: thumbnail, category, color
  - [ ] Tap item to open detail
- [ ] Filter bar
  - [ ] Category dropdown (shirt, pants, etc.)
  - [ ] Color filter (tappable color swatches)
  - [ ] Season filter (Spring, Summer, Fall, Winter)
  - [ ] Apply filters button
- [ ] Search bar
  - [ ] Text input with debounce
  - [ ] Search results in real-time
- [ ] Add item button
  - [ ] Navigation to upload screen

### Flutter — Upload Item Screen

- [ ] Camera + gallery picker
- [ ] Image preview
- [ ] Manual category override (in case Vision API fails)
- [ ] Manual color input
- [ ] Size, brand, price fields
- [ ] Upload button with loading state
- [ ] Success/error messages

### Flutter — Item Detail Screen

- [ ] Display item image + metadata
- [ ] Edit button → edit form
- [ ] Delete button (confirmation)
- [ ] Favorite toggle
- [ ] Share button (generate share link)
- [ ] Back button

### Flutter — BLoC for Wardrobe

- [ ] WardrobeBloc created
- [ ] Events: FetchItems, UploadItem, UpdateItem, DeleteItem, FilterByCategory, Search
- [ ] States: Initial, Loading, ItemsLoaded, Error
- [ ] Caching of items (don't refetch on every load)

### Performance

- [ ] Wardrobe grid loads instantly (from cache)
- [ ] Upload completes in <10 seconds
- [ ] Filter/search completes in <500ms
- [ ] No jank when scrolling grid (60 FPS)

### Testing

- [ ] Unit tests for WardrobeService
  - [ ] test_upload_and_categorize
  - [ ] test_classify_category (all types)
  - [ ] test_extract_color
  - [ ] test_detect_pattern
- [ ] Integration tests
  - [ ] test_upload_with_real_vision_api
  - [ ] test_filter_by_category
  - [ ] test_search_functionality
- [ ] Flutter widget tests
  - [ ] test_wardrobe_grid_renders
  - [ ] test_filter_bar_works
  - [ ] test_search_debounces
  - [ ] test_lazy_loading_pagination

---

## SPRINT 4: Week 8 — Outfit Builder

**Goal:** Users create outfits by combining items.
**Horas:** 50
**Equipo:** Sasha (15h), Brook (35h)

### Backend

- [ ] Outfit model + database table
- [ ] `POST /api/v1/outfits` (create outfit)
  - [ ] Accept list of item IDs
  - [ ] Validate all items belong to user
  - [ ] Save outfit
- [ ] `GET /api/v1/outfits` (list)
  - [ ] Paginated
- [ ] `GET /api/v1/outfits/{outfit_id}` (detail)
- [ ] `PATCH /api/v1/outfits/{outfit_id}` (update)
- [ ] `DELETE /api/v1/outfits/{outfit_id}`
- [ ] `POST /api/v1/outfits/{outfit_id}/rate` (rate outfit 0-5)

### Flutter — Outfit Builder Screen

- [ ] Drag-and-drop interface (or button-based selection)
  - [ ] Available items in sidebar
  - [ ] Drag to "Add to Outfit"
  - [ ] Visual feedback
- [ ] Outfit preview
  - [ ] Simple 2D layout (top, middle, bottom)
  - [ ] Item images positioned
  - [ ] Remove item button on each item
- [ ] Save outfit
  - [ ] Modal for name + occasion + season
  - [ ] Confirm button
- [ ] Outfit list screen
  - [ ] Grid of saved outfits
  - [ ] Tap to view detail
  - [ ] Delete outfit (confirmation)
- [ ] Outfit detail screen
  - [ ] Large preview
  - [ ] List of items
  - [ ] Rating (stars)
  - [ ] Edit / Delete buttons

### Flutter — BLoCs

- [ ] OutfitBloc created
- [ ] Events: FetchOutfits, CreateOutfit, UpdateOutfit, DeleteOutfit, RateOutfit
- [ ] States: Initial, Loading, OutfitsLoaded, Error

### Testing

- [ ] Unit tests for Outfit endpoints
- [ ] Widget tests for outfit builder
  - [ ] test_drag_and_drop_items
  - [ ] test_outfit_preview_renders
  - [ ] test_save_outfit

---

## SPRINT 5: Week 9-10 — Virtual Try-On

**Goal:** Replicate API integration, queue system, try-on results.
**Horas:** 110
**Equipo:** Sasha (80h), Brook (30h)

### Backend — Replicate Integration

- [ ] Replicate API credentials obtained
- [ ] `app/services/tryon_service.py` created
- [ ] Try-on request queuing system
  - [ ] Max 10 concurrent per user
  - [ ] FIFO queue per user
  - [ ] Retry logic (exponential backoff, max 3 retries)
- [ ] Replicate job polling
  - [ ] Poll every 2 seconds
  - [ ] Timeout after 5 minutes
  - [ ] Error handling
- [ ] Result storage
  - [ ] Download result image
  - [ ] Store in Supabase Storage
  - [ ] Save metadata to DB

### Backend Endpoints

- [ ] `POST /api/v1/tryons` (create try-on)
  - [ ] Accept body_image_url, item_id or outfit_id
  - [ ] Queue request
  - [ ] Return immediately with job ID
  - [ ] Return status + estimated time
  - [ ] Tested: Valid request + invalid IDs + invalid images
- [ ] `GET /api/v1/tryons/{tryon_id}` (get result)
  - [ ] Return pending/completed/failed status
  - [ ] If completed, return result_image_url
  - [ ] If failed, return error message
- [ ] `GET /api/v1/tryons` (list past try-ons)
  - [ ] Paginated
  - [ ] Order by created_at DESC
- [ ] `DELETE /api/v1/tryons/{tryon_id}` (delete try-on)

### Queue System

- [ ] Background task runner (Celery or n8n)
  - [ ] Process try-on queue every 5 seconds
  - [ ] Call Replicate API
  - [ ] Update status in DB
  - [ ] Error handling + logging
- [ ] Database tracking
  - [ ] tryons table with status (pending, processing, completed, failed)
  - [ ] timestamps (created_at, completed_at)

### Load Testing

- [ ] Load test script (k6 or Locust)
  - [ ] Simulate 1K concurrent users
  - [ ] Each user requests 5 try-ons
  - [ ] Measure response time + P95 + P99
  - [ ] Verify queue doesn't drop requests
  - [ ] Verify infra doesn't break

### Flutter — Try-On Screen

- [ ] Item selection UI
  - [ ] Show current body photo
  - [ ] Select item from wardrobe (grid picker)
  - [ ] OR select outfit
- [ ] Try-on request
  - [ ] Show loading state with estimated time
  - [ ] Poll for completion (every 1 second)
  - [ ] Cancel button
- [ ] Result display
  - [ ] Before/after swiper (swipe to compare)
  - [ ] Full-screen view
  - [ ] Share button
  - [ ] Save to favorites
  - [ ] Try another button

### Flutter — Try-On History Screen

- [ ] Grid of past try-ons
- [ ] Tap to view result again
- [ ] Delete try-on (confirmation)
- [ ] Filter by item / outfit

### Flutter — BLoCs

- [ ] TryonBloc created
- [ ] Events: CreateTryon, FetchResult, FetchHistory, DeleteTryon
- [ ] States: Initial, Loading, Processing, Completed, Error
- [ ] Polling logic (automatic every 1 second if processing)

### Cost Optimization

- [ ] Monitor Replicate costs
  - [ ] Set budget alerts
  - [ ] Track cost per user
- [ ] Implement caching (don't re-run same try-on)
  - [ ] Cache key: hash(body_image + item_image)
  - [ ] TTL: 30 days

### Testing

- [ ] Unit tests for TryOnService
  - [ ] test_queue_try_on_request
  - [ ] test_poll_completion
  - [ ] test_retry_on_failure
  - [ ] test_timeout_after_5_min
- [ ] Integration tests with mock Replicate
  - [ ] test_full_workflow (request → pending → completed)
- [ ] Load tests
  - [ ] test_1k_concurrent_requests
  - [ ] Verify no dropped requests
  - [ ] Verify P95 response < 100ms

---

## SPRINT 6: Week 11 — Recommendations (Claude API)

**Goal:** Claude-powered outfit suggestions.
**Horas:** 60
**Equipo:** Sasha (40h), Brook (20h)

### Backend

- [ ] `app/services/recommendation_service.py` created
- [ ] Prompt engineering
  - [ ] Include wardrobe items
  - [ ] Include body shape + skin tone
  - [ ] Include occasion/query
  - [ ] Request N outfit suggestions
- [ ] Caching strategy
  - [ ] Hash(query) → cached response
  - [ ] TTL: 7 days
  - [ ] Store in Supabase or Redis
- [ ] `POST /api/v1/recommendations` endpoint
  - [ ] Accept query string
  - [ ] Return list of outfit suggestions (with item IDs)
  - [ ] Tested: Different queries + edge cases
- [ ] `GET /api/v1/recommendations/history` endpoint
  - [ ] Paginated list of past recommendations

### Prompt Engineering

- [ ] Test with sample wardrobe + queries
- [ ] Verify Claude returns structured format
- [ ] Test accuracy + relevance
- [ ] Test with diverse body shapes + skin tones
- [ ] Cost optimization (minimize tokens)
  - [ ] Pre-summarize wardrobe
  - [ ] Use cached responses
  - [ ] Target: <300 tokens per request

### Flutter — Recommendations Screen

- [ ] Chat-like interface
  - [ ] User input field at bottom
  - [ ] Message bubbles (user on right, AI on left)
  - [ ] Typing indicator while Claude responds
- [ ] Suggestion cards
  - [ ] Each suggestion shows:
    - Outfit name/title
    - List of items (with thumbnails)
    - Why it works (description)
    - Styling tips
  - [ ] Tap to view full outfit
  - [ ] Add to outfits button
- [ ] Request input examples
  - [ ] Suggestions: "Work meeting", "Date night", "Casual Friday"
  - [ ] Freeform text allowed

### Flutter — BLoCs

- [ ] RecommendationBloc created
- [ ] Events: RequestRecommendation, FetchHistory
- [ ] States: Initial, Loading, Completed, Error
- [ ] Streaming (optional: show Claude response as it comes)

### Testing

- [ ] Unit tests for RecommendationService
  - [ ] test_get_recommendations
  - [ ] test_caching_works
  - [ ] test_prompt_includes_wardrobe_items
- [ ] Integration tests with real Claude API
  - [ ] Test with 5 different queries
  - [ ] Verify token usage < 500 per call
- [ ] Flutter widget tests
  - [ ] test_chat_interface_renders
  - [ ] test_suggestion_cards_displayed
  - [ ] test_input_field_captures_query

---

## SPRINT 7: Week 12 — Subscriptions + Payment

**Goal:** Freemium model working (Stripe + Mercado Pago).
**Horas:** 80
**Equipo:** Sasha (50h), Brook (30h)

### Backend — Stripe Integration

- [ ] Stripe account created + API keys obtained
- [ ] Product + price IDs created in Stripe
  - [ ] "Premium Monthly" → $4.99/month
  - [ ] "Premium Annual" → $49.99/year
- [ ] `app/services/subscription_service.py` created
- [ ] `POST /api/v1/subscriptions/checkout` endpoint
  - [ ] Create Stripe checkout session
  - [ ] Return session URL
  - [ ] Tested: Valid plan + invalid plan
- [ ] Webhook receiver
  - [ ] Listen to `checkout.session.completed`
  - [ ] Listen to `customer.subscription.created`
  - [ ] Listen to `customer.subscription.deleted`
  - [ ] Listen to `invoice.payment_failed`
  - [ ] Update user subscription status in DB
- [ ] `GET /api/v1/subscriptions/status` endpoint
  - [ ] Return current subscription tier + next billing date
- [ ] `POST /api/v1/subscriptions/cancel` endpoint
  - [ ] Cancel subscription at end of current period

### Backend — Mercado Pago Integration

- [ ] Mercado Pago credentials obtained
- [ ] `POST /api/v1/subscriptions/checkout-mp` endpoint
  - [ ] Create Mercado Pago preference
  - [ ] Return redirect URL
- [ ] Webhook receiver for Mercado Pago
- [ ] Tested with Mercado Pago sandbox

### Feature Gating

- [ ] Implement premium features gate
  - [ ] Max 5 wardrobe items free, unlimited premium
  - [ ] Max 1 try-on/month free, 50/month premium
  - [ ] Max 2 recommendations/month free, unlimited premium
- [ ] Check subscription tier in endpoints
  - [ ] Return 402 Payment Required if limit exceeded
  - [ ] Return friendly error message

### Flutter — Subscription Screen

- [ ] Plans display
  - [ ] Free: $0
  - [ ] Premium Monthly: $4.99
  - [ ] Premium Annual: $49.99 (save 17%)
  - [ ] Feature comparison (table)
- [ ] Upgrade button
  - [ ] Opens Stripe checkout (web view)
  - [ ] Returns to app after success/cancel
- [ ] Manage subscription
  - [ ] Show current plan
  - [ ] Show next billing date
  - [ ] Cancel subscription button (confirmation)

### Flutter — Payment Integration

- [ ] Flutter Stripe plugin integrated
- [ ] WebView for checkout
- [ ] Deep linking (app://checkout?success=true)
- [ ] Handle payment success/failure
- [ ] Error messages

### Testing

- [ ] Unit tests for SubscriptionService
  - [ ] test_create_checkout_session
  - [ ] test_update_subscription_on_webhook
  - [ ] test_feature_gating_free_tier
  - [ ] test_feature_gating_premium_tier
- [ ] Integration tests with Stripe test API
  - [ ] test_full_checkout_flow
  - [ ] test_webhook_received_and_processed
- [ ] Flutter widget tests
  - [ ] test_subscription_screen_renders
  - [ ] test_plan_comparison_displayed
  - [ ] test_upgrade_button_opens_checkout

---

## SPRINT 8: Week 13 — Polish + Performance + Analytics

**Goal:** Production-ready quality, monitoring, analytics.
**Horas:** 70
**Equipo:** Sasha (30h), Brook (40h)

### Analytics

- [ ] Analytics event schema created
  - [ ] user_id, event_type, metadata, created_at
- [ ] Event tracking in services
  - [ ] wardrobe_upload, body_analysis_completed, tryon_generated, recommendation_viewed, subscription_created
- [ ] DAU/MAU dashboards
  - [ ] SQL views for daily active users
  - [ ] SQL views for monthly active users
  - [ ] Supbase dashboard or Metabase
- [ ] Funnel analysis
  - [ ] Signup → body analysis → wardrobe → try-on → upgrade
- [ ] Dashboard accessible to Juan Camilo
  - [ ] Real-time metrics
  - [ ] Charts + KPIs

### Performance Optimization

- [ ] Image caching
  - [ ] Cloudflare CDN for Supabase Storage
  - [ ] Browser cache headers (1 year for static images)
- [ ] Database query optimization
  - [ ] Indexes verified on all filter columns
  - [ ] Query execution time <100ms
  - [ ] No N+1 queries
- [ ] API response time optimization
  - [ ] Pagination applied everywhere
  - [ ] Lazy loading in mobile
  - [ ] P95 response < 200ms
- [ ] Mobile app performance
  - [ ] App startup time <3 seconds
  - [ ] Screen transitions smooth (60 FPS)
  - [ ] No memory leaks
- [ ] Load testing at scale
  - [ ] Simulate 50K users accessing app simultaneously
  - [ ] Verify infrastructure holds up
  - [ ] Identify bottlenecks

### Error Logging + Monitoring

- [ ] Sentry integration complete
  - [ ] Backend errors logged
  - [ ] Frontend errors logged
  - [ ] Mobile app errors logged
- [ ] Error alerts configured
  - [ ] Critical errors → Slack notification
  - [ ] Pattern detection (X errors in 5 min)
- [ ] Custom metrics logged
  - [ ] API latency
  - [ ] Database query time
  - [ ] External API success rates
- [ ] Dashboards created
  - [ ] Sentry error dashboard
  - [ ] Infrastructure dashboard (Railway, Supabase)
  - [ ] Business metrics dashboard

### Accessibility

- [ ] Flutter a11y audit
  - [ ] Semantics labels on all buttons/inputs
  - [ ] Color contrast ratios verified (WCAG AA minimum)
  - [ ] Text scaling works
  - [ ] Screen reader compatible
- [ ] Backend a11y (if applicable)
  - [ ] API responses include alt text fields

### Localization (i18n)

- [ ] Flutter localization setup (intl package)
- [ ] English + Spanish strings extracted
  - [ ] Generate .arb files
  - [ ] Strings translated
- [ ] Dynamic language switching
  - [ ] Settings screen language option
  - [ ] Persist selection

### App Store Preparation

- [ ] Android:
  - [ ] Privacy policy (URL)
  - [ ] Terms of service (URL)
  - [ ] App description + screenshots (5 images)
  - [ ] Minimum Android version: 7.0
- [ ] iOS:
  - [ ] Privacy policy (URL)
  - [ ] Terms of service (URL)
  - [ ] App description + screenshots (5 images)
  - [ ] Minimum iOS version: 12.0
  - [ ] TestFlight beta setup

### QA

- [ ] Feature complete checklist
  - [ ] All endpoints implemented + tested
  - [ ] All screens built + usable
  - [ ] No hardcoded values
  - [ ] Error messages user-friendly
- [ ] Regression testing
  - [ ] Full user flow tested end-to-end
  - [ ] Edge cases handled
- [ ] Security audit
  - [ ] OWASP Top 10 checklist
  - [ ] SQL injection: all queries parameterized ✅
  - [ ] XSS: input validation ✅
  - [ ] CSRF: CORS configured ✅
  - [ ] Authentication: JWT validated ✅
  - [ ] Authorization: RLS policies verified ✅
  - [ ] Sensitive data: passwords hashed ✅
  - [ ] Rate limiting: implemented ✅

### Testing

- [ ] Code coverage >80% across backend
- [ ] Unit tests for all services
- [ ] Integration tests for critical paths
- [ ] E2E tests for full user flow
- [ ] Load tests pass

---

## SPRINT 9: Week 14 — Launch Preparation + Soft Launch

**Goal:** Production deployment, beta launch, monitoring.
**Horas:** 60
**Equipo:** Sasha (20h), Brook (30h), Erik (10h)

### Final Bug Fixes

- [ ] Review all GitHub issues + fix remaining bugs
- [ ] Manual testing on real devices (iPhone + Android)
- [ ] Cross-browser testing (web version)
- [ ] Network testing (slow 4G, offline scenarios)

### Production Deployment

- [ ] Database backups tested + working
- [ ] Staging environment mirrors production
- [ ] All environment variables set correctly
- [ ] SSL/HTTPS working
- [ ] Email templates tested
- [ ] Payment providers in production mode (not sandbox)

### Load Testing

- [ ] Load test at 50K concurrent users
  - [ ] Expected to handle successfully
  - [ ] Monitor CPU, memory, database connections
  - [ ] Identify any remaining bottlenecks
- [ ] Spike testing (10x traffic surge)
  - [ ] Ensure app recovers gracefully
  - [ ] No data loss

### Monitoring Setup

- [ ] Alerting rules configured
  - [ ] 5xx error rate > 1% → alert
  - [ ] API latency P95 > 500ms → alert
  - [ ] Database connections > 80% → alert
  - [ ] Storage usage > 80% → alert
- [ ] On-call rotation (if team available)
- [ ] Incident response plan documented

### Soft Launch (Beta)

- [ ] Select 100-200 beta users
  - [ ] Friends, family, influencers
  - [ ] Diverse geographies + devices
- [ ] Beta release (TestFlight + Google Play beta)
- [ ] Feedback collection
  - [ ] In-app feedback form
  - [ ] GitHub issues from beta users
  - [ ] Slack channel for feedback
- [ ] Monitor analytics closely
  - [ ] DAU/MAU
  - [ ] Conversion funnels
  - [ ] Error rates
  - [ ] Feature usage

### Bug Fixes from Beta

- [ ] Prioritize critical bugs (app crash, data loss)
- [ ] Deploy hotfixes to beta
- [ ] Gather feedback + iterate
- [ ] Target: 0 crashes after 2 weeks beta

### Marketing Materials

- [ ] Landing page finalized
- [ ] Social media accounts set up (Instagram, TikTok, Twitter)
- [ ] Influencer outreach (fashion, style creators)
- [ ] Press release drafted
- [ ] Launch video recorded (30 seconds)

### Public Launch Readiness

- [ ] App Store submission (iOS)
  - [ ] Pass App Store review (expect 1-2 days)
- [ ] Google Play submission (Android)
  - [ ] Auto-approved usually (1-2 hours)
- [ ] Website goes live
- [ ] Social media posts scheduled
- [ ] Email campaign drafted (welcome series)

### Post-Launch Monitoring

- [ ] First week: Team on standby for critical issues
- [ ] Daily metrics review
- [ ] Respond to user feedback quickly
- [ ] Plan improvements based on usage patterns

---

## ONGOING TASKS (Throughout All Sprints)

- [ ] Daily standup (15 min)
- [ ] GitHub issues tracked + prioritized
- [ ] Code reviews (PR process)
- [ ] Dependency updates (monthly)
- [ ] Security patches (as-needed)
- [ ] Database backups (daily)
- [ ] Monitoring dashboards checked (daily)

---

## GO/NO-GO DECISION POINTS

**After Sprint 0:**
- Go: Infrastructure stable, 0 downtime, deployments automated
- No-go: Infrastructure issues, manual deployments, flaky tests

**After Sprint 1:**
- Go: Auth working, users can sign up + log in
- No-go: Auth bugs, token issues, RLS not working

**After Sprint 3:**
- Go: Wardrobe feature complete, auto-categorization working
- No-go: Vision API fails frequently, search performance poor

**After Sprint 5:**
- Go: Virtual try-on working, queue system stable, cost acceptable
- No-go: Replicate too expensive, queue drops requests, images bad quality

**After Sprint 7:**
- Go: Payments working (both providers), feature gating working
- No-go: Payment integration broken, webhook failures

**After Sprint 9:**
- Go: 0 critical bugs, load tests pass, launch approved
- No-go: Unresolved crashes, data loss, security issues

---

## CONTINGENCY PLANS

**If Behind Schedule:**
- Cut features: recommendations, annual plan, Mercado Pago
- Extend timeline by 2-4 weeks
- Focus on core: auth, wardrobe, try-on, payment

**If Infrastructure Fails:**
- Migrate to AWS RDS (faster than Supabase at scale)
- Use Cloudinary for image processing
- Scale horizontally (multiple API instances)

**If Replicate Costs Too High:**
- Use cheaper model
- Batch try-ons (process overnight)
- Implement quota (5 free tryons/month, upgrade for more)

**If User Growth Slower Than Expected:**
- Reduce initial target from 50K to 10K
- Focus on organic growth + word-of-mouth
- Partner with fashion influencers
- Extend timeline by 4-8 weeks

---

## SUCCESS METRICS

**Day 1:**
- 50K signups (target)
- 0 critical errors
- 99.9% uptime

**Week 1:**
- 30K DAU (60% retention)
- 10% conversion to premium ($29K revenue)
- <200ms API response time

**Month 1:**
- 100K+ registered users
- 40K DAU
- 10-15% premium conversion
- <1% error rate

