"""
Authentication service for user management.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User
from src.core.exceptions import AuthenticationError, NotFoundError
from .password_service import password_service
from .jwt_service import jwt_service, Token


class AuthService:
    """Service for user authentication operations."""
    
    def __init__(self, db: AsyncSession):
        """Initialize auth service with database session."""
        self.db = db
    
    async def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticate a user with username and password.
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            Authenticated user object
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # Try to find user by username or email
        stmt = select(User).where(
            (User.username == username) | (User.email == username)
        )
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        if not password_service.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid username or password")
        
        return user
    
    async def create_user(
        self, 
        email: str, 
        password: str, 
        full_name: str,
        username: Optional[str] = None
    ) -> User:
        """
        Create a new user account.
        
        Args:
            email: User email
            password: Plain text password
            full_name: User's full name
            username: Optional username
            
        Returns:
            Created user object
            
        Raises:
            AuthenticationError: If user already exists
        """
        # Check if user already exists
        stmt = select(User).where(
            (User.email == email) | 
            (User.username == username if username else False)
        )
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            if existing_user.email == email:
                raise AuthenticationError("Email already registered")
            if existing_user.username == username:
                raise AuthenticationError("Username already taken")
        
        # Hash password
        hashed_password = password_service.hash_password(password)
        
        # Create new user
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_verified=False
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_id(self, user_id: str) -> User:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            NotFoundError: If user not found
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError("User", user_id)
        
        return user
    
    async def login(self, username: str, password: str) -> Token:
        """
        Login user and return JWT token.
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            JWT token response
        """
        user = await self.authenticate_user(username, password)
        
        # Create token with user info
        return jwt_service.create_token_response(
            user_id=user.id,
            username=user.username or user.email,
            scopes=["user"]  # Basic user scope
        )
    
    async def register(
        self, 
        email: str, 
        password: str, 
        full_name: str,
        username: Optional[str] = None
    ) -> Token:
        """
        Register new user and return JWT token.
        
        Args:
            email: User email
            password: Plain text password
            full_name: User's full name
            username: Optional username
            
        Returns:
            JWT token response
        """
        user = await self.create_user(email, password, full_name, username)
        
        # Create token for new user
        return jwt_service.create_token_response(
            user_id=user.id,
            username=user.username or user.email,
            scopes=["user"]
        )
