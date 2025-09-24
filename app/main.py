from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Determine environment
environment = os.getenv("ENVIRONMENT", "development")
is_production = environment == "production"

# Get the base directory path
BASE_DIR = Path(__file__).parent.parent

app = FastAPI(
    title="Lab Equipment Company",
    description="E-commerce platform for laboratory equipment and reagents",
    version="1.0.0",
    docs_url="/docs" if not is_production else None,
    redoc_url="/redoc" if not is_production else None,
)

# Configure CORS based on environment
if is_production:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://your-domain.onrender.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Create static and templates directories if they don't exist
static_dir = BASE_DIR / "app" / "static"
templates_dir = BASE_DIR / "app" / "templates"

# Create directories if they don't exist
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

# Create subdirectories
(static_dir / "css").mkdir(exist_ok=True)
(static_dir / "images").mkdir(exist_ok=True)

print(f"Static directory: {static_dir}")
print(f"Templates directory: {templates_dir}")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    print("✅ Static files mounted successfully")
except Exception as e:
    print(f"❌ Error mounting static files: {e}")

# Configure templates
try:
    templates = Jinja2Templates(directory=str(templates_dir))
    print("✅ Templates configured successfully")
except Exception as e:
    print(f"❌ Error configuring templates: {e}")

# Import routers inside functions to avoid circular imports
@app.on_event("startup")
async def startup_event():
    """Import routers after app is created to avoid circular imports"""
    from app.routers import frontend, admin, auth
    
    app.include_router(frontend.router)
    app.include_router(admin.router)
    app.include_router(auth.router)
    print("✅ Routers loaded successfully")

# @app.get("/")
# async def root():
#     return {"message": "Lab Equipment Company API is running!", "environment": environment}

@app.get("/health")
async def health_check():
    static_exists = static_dir.exists()
    templates_exists = templates_dir.exists()
    
    return {
        "status": "healthy", 
        "environment": environment,
        "static_files": "available" if static_exists else "missing",
        "templates": "available" if templates_exists else "missing"
    }

# Production-specific middleware
if is_production:
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

# This allows running with python app/main.py directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True if os.getenv("DEBUG") == "True" else False
    )