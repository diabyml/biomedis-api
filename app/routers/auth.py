from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login():
    # Will be implemented later
    return {"message": "Login endpoint"}

@router.post("/register")
async def register():
    # Will be implemented later
    return {"message": "Register endpoint"}