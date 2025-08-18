from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api.routes import router
from app.config import settings

app = FastAPI(title="AI Content Strategy Engine")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve React build
frontend_dir = Path(__file__).parent.parent / "frontend" / "build"

# Only mount static files if they exist
if (frontend_dir / "static").exists():
    app.mount("/static", StaticFiles(directory=frontend_dir / "static"), name="static")

# Serve React app
if (frontend_dir / "index.html").exists():
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """Catch-all: send React index.html for any non-API route"""
        return FileResponse(frontend_dir / "index.html")
    
    @app.get("/")
    async def serve_index():
        """Serve React index.html"""
        return FileResponse(frontend_dir / "index.html")
