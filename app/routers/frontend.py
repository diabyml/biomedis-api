from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")

# Import database dependency inside the route functions to avoid circular imports
@router.get("/")
async def homepage(request: Request):
    # Lazy import to avoid circular dependencies
    from app.database import get_db
    from sqlalchemy.orm.session import Session
    
    # We'll add database functionality later
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/products")
async def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})