from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from backend.app.database import create_user, get_user
from backend.app.security import create_access_token
import logging

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
logger = logging.getLogger(__name__)

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    body_type: str = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Register a new user"""
    try:
        response = await create_user(request.email, request.password, request.body_type)

        if response.user:
            access_token = create_access_token(data={"sub": response.user.id})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": response.user.id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    try:
        # In production, verify password with hash
        user = await get_user(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = create_access_token(data={"sub": user.get("id")})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.get("id")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
