# SETUP — Supabase Storage Bucket `/try-ons/`

**Owner:** Jarvis (CEO)  
**Task:** Create storage bucket for T2 Replicate Worker (signed URLs)  
**Time:** 5 minutes  
**Status:** ⏳ TODO

---

## 🎯 WHAT & WHY

**Replicate Worker (Sprint 0.5, T2) generates virtual try-on images.**

These images need to be:
1. **Stored** in persistent storage (not temporary)
2. **Served** with signed URLs (24h expiry, secure)
3. **Retrieved** by frontend at S04 Virtual Try-On screen

**Supabase Storage bucket `/try-ons/` is the storage layer.**

---

## 📋 STEPS

### Step 1: Login to Supabase Dashboard
```
https://app.supabase.com/projects
```

Select your project: `asesor-imagen-ai` (or equivalent)

---

### Step 2: Navigate to Storage

Left sidebar → **Storage** → **Buckets**

---

### Step 3: Create Bucket

Click **Create a new bucket**

```
Bucket name: try-ons
Visibility: Private (🔒 — requires signed URL)
File size limit: 100 MB (sufficient for high-res images)
```

Click **Create bucket**

---

### Step 4: Verify Bucket Created

Should see in Buckets list:
```
Name       | Type      | Created
-----------|-----------|----------
try-ons    | Private   | [today]
```

---

### Step 5: (OPTIONAL) Set Policies

If Replicate worker is a service account, verify RLS allows upload:

Go to bucket → **Policies** tab

Should have default policies allowing authenticated uploads. If not, add:

```sql
-- Allow authenticated users to upload
CREATE POLICY "allow-auth-upload" ON storage.objects
FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'try-ons');

-- Allow frontend to download via signed URL
CREATE POLICY "allow-signed-download" ON storage.objects
FOR SELECT
USING (bucket_id = 'try-ons');
```

(Usually pre-configured in Supabase, no action needed.)

---

### Step 6: Test (Optional)

In Supabase dashboard, manually upload a test image:
```
Bucket: try-ons
File: test.jpg
Path: user_1/test.jpg
```

Then generate signed URL:
```
Right-click → Copy URL → Check it works (24h expiry)
```

---

## 🔐 SECURITY NOTES

- ✅ **Private bucket:** Only accessible via signed URLs
- ✅ **24h expiry:** URLs become invalid after 1 day (prevents leaking)
- ✅ **Path structure:** `/user_id/{random_id}.jpg` (prevents enumeration)

---

## 📝 BACKEND INTEGRATION

Replicate worker will use:

```python
# app/workers/replicate_worker.py
from supabase import create_client

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,  # Has admin powers
)

# After Replicate generates image:
image_data = ...  # bytes

# Upload to Supabase
response = supabase.storage.from_("try-ons").upload(
    path=f"{user_id}/{job_id}.jpg",
    file=image_data,
    file_options={"content-type": "image/jpeg"},
)

# Generate signed URL (24h)
signed_url = supabase.storage.from_("try-ons").create_signed_url(
    path=f"{user_id}/{job_id}.jpg",
    expires_in=86400,  # 24 hours in seconds
)

# Store in DB
db.update_try_on(
    id=job_id,
    image_url=signed_url,
    status="completed",
)
```

---

## ✅ SUCCESS CRITERIA

- [ ] Bucket `try-ons` exists in Supabase Storage
- [ ] Visibility is **Private**
- [ ] Can upload test file via dashboard
- [ ] Can generate signed URL for test file
- [ ] Signed URL expires after 24h

---

## 🚀 TIMING

**Create this bucket TODAY (2026-05-18)** before Antigravity starts Sprint 0.5.

If bucket doesn't exist when T2 Replicate worker tries to upload, Sprint 0.5 will fail.

5-minute task. Do it now.

