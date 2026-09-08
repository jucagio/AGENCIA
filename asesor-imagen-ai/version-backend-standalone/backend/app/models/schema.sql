-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  body_type VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Body Analysis table
CREATE TABLE IF NOT EXISTS body_analysis (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  analysis_json JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Wardrobe table
CREATE TABLE IF NOT EXISTS wardrobe (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Clothes table
CREATE TABLE IF NOT EXISTS clothes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  wardrobe_id UUID NOT NULL REFERENCES wardrobe(id) ON DELETE CASCADE,
  image_url VARCHAR(500),
  category VARCHAR(100),
  color VARCHAR(50),
  size VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Outfits table
CREATE TABLE IF NOT EXISTS outfits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  clothes_ids_json JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Try-ons table
CREATE TABLE IF NOT EXISTS try_ons (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  outfit_id UUID REFERENCES outfits(id) ON DELETE SET NULL,
  generated_image_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'active',
  payment_method VARCHAR(100),
  amount DECIMAL(10, 2),
  next_billing TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE body_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE wardrobe ENABLE ROW LEVEL SECURITY;
ALTER TABLE clothes ENABLE ROW LEVEL SECURITY;
ALTER TABLE outfits ENABLE ROW LEVEL SECURITY;
ALTER TABLE try_ons ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Users can only see their own data
CREATE POLICY "users_own_data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "users_update_own" ON users FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "body_analysis_own" ON body_analysis FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "body_analysis_insert" ON body_analysis FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "wardrobe_own" ON wardrobe FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "wardrobe_insert" ON wardrobe FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "clothes_own" ON clothes FOR SELECT USING (
  wardrobe_id IN (SELECT id FROM wardrobe WHERE user_id = auth.uid())
);
CREATE POLICY "clothes_insert" ON clothes FOR INSERT WITH CHECK (
  wardrobe_id IN (SELECT id FROM wardrobe WHERE user_id = auth.uid())
);

CREATE POLICY "outfits_own" ON outfits FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "outfits_insert" ON outfits FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "try_ons_own" ON try_ons FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "try_ons_insert" ON try_ons FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "subscriptions_own" ON subscriptions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "subscriptions_insert" ON subscriptions FOR INSERT WITH CHECK (auth.uid() = user_id);
