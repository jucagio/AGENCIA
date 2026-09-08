from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.routes import (
    health,
    auth,
    body_analysis,
    recommendations,
    wardrobe,
    outfits,
    try_ons
)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API para análisis de imagen corporal y recomendaciones de vestuario con IA"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.API_TITLE} in {settings.ENVIRONMENT} mode...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    print(f"Shutting down {settings.API_TITLE}...")

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(body_analysis.router)
app.include_router(recommendations.router)
app.include_router(wardrobe.router)
app.include_router(outfits.router)
app.include_router(try_ons.router)

@app.get("/")
async def root():
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

