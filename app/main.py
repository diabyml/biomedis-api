from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Determine environment
environment = os.getenv("ENVIRONMENT", "development")
is_production = environment == "production"

app = FastAPI(
    title="Biomedis API",
    description="E-commerce platform for laboratory equipment and reagents",
    version="1.0.0",
    docs_url="/docs" if not is_production else None,  # Hide docs in production
    redoc_url="/redoc" if not is_production else None,  # Hide redoc in production
)

# Configure CORS based on environment
if is_production:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update with your actual domain
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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Import and include routers
from app.routers import frontend, admin, auth

app.include_router(frontend.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Lab Equipment Company API is running!", "environment": environment}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "environment": environment,
        "database": "connected"  # We'll enhance this later
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