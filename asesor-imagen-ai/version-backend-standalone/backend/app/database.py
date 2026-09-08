import os
from supabase import create_client, Client

class SupabaseDB:
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env.local")
            
            cls._instance = create_client(url, key)
        
        return cls._instance

# Helper functions
async def create_user(email: str, password: str, body_type: str = None):
    db = SupabaseDB.get_client()
    response = db.auth.sign_up({"email": email, "password": password})
    
    if response.user:
        db.table("users").insert({
            "id": response.user.id,
            "email": email,
            "password": password,  # In production, store hashed
            "body_type": body_type
        }).execute()
    
    return response

async def get_user(user_id: str):
    db = SupabaseDB.get_client()
    response = db.table("users").select("*").eq("id", user_id).single().execute()
    return response.data

async def get_body_analysis(user_id: str):
    db = SupabaseDB.get_client()
    response = db.table("body_analysis").select("*").eq("user_id", user_id).execute()
    return response.data

async def create_analysis(user_id: str, analysis_json: dict):
    db = SupabaseDB.get_client()
    response = db.table("body_analysis").insert({
        "user_id": user_id,
        "analysis_json": analysis_json
    }).execute()
    return response.data

