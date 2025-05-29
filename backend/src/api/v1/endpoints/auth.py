"""
Authentication endpoints.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import AuthenticationError, MetaMysticException
from src.services.auth import AuthService
from src.services.auth.jwt_service import jwt_service, Token, TokenData
from src.models.user import User

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class RegisterRequest(BaseModel):
    """Registration request schema."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    full_name: str = Field(..., description="User full name")
    username: Optional[str] = Field(None, description="Optional username")


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: str
    username: Optional[str]
    full_name: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Extract token from "Bearer <token>" format
        if token.startswith("Bearer "):
            token = token[7:]

        # Verify token
        token_data = jwt_service.verify_token(token)

        # Get user from database
        auth_service = AuthService(db)
        user = await auth_service.get_user_by_id(token_data.user_id)

        return user

    except (AuthenticationError, MetaMysticException) as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    User login endpoint.

    Authenticates user credentials and returns JWT access token.
    """
    try:
        auth_service = AuthService(db)
        token = await auth_service.login(request.username, request.password)
        return token

    except AuthenticationError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/register", response_model=Token)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    User registration endpoint.

    Creates new user account and returns JWT access token.
    """
    try:
        auth_service = AuthService(db)
        token = await auth_service.register(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            username=request.username
        )
        return token

    except AuthenticationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    User logout endpoint.

    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token. In a production system, you might want to
    implement a token blacklist.
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information.

    Returns user profile information for the authenticated user.
    """
    return UserResponse.from_orm(current_user)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token endpoint.

    This endpoint is compatible with OAuth2 password flow for tools
    that expect the standard /token endpoint.
    """
    try:
        auth_service = AuthService(db)
        token = await auth_service.login(form_data.username, form_data.password)
        return token

    except AuthenticationError as e:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
