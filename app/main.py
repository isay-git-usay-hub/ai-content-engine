from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings
import uvicorn

app = FastAPI(
    title="AI Content Strategy Engine",
    description="Automated trending content analysis and strategy generation",
    version="1.0.0"
)  # ← Fixed: Added missing closing bracket

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # ← Fixed: Added missing closing bracket

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Content Strategy Engine API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-08-18T22:49:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # Changed from just "main:app"
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )  # ← Fixed: Added missing closing bracket
