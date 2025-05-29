"""
JWT token service for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from pydantic import BaseModel

from src.core.config import settings
from src.core.exceptions import AuthenticationError


class TokenData(BaseModel):
    """Token data model."""
    username: Optional[str] = None
    user_id: Optional[str] = None
    scopes: list[str] = []


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class JWTService:
    """Service for JWT token operations."""
    
    def __init__(self):
        """Initialize JWT service with settings."""
        self.secret_key = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM
        self.expire_minutes = settings.JWT_EXPIRE_MINUTES
    
    def create_access_token(
        self, 
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Custom expiration time
            
        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token data
            
        Raises:
            AuthenticationError: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            scopes: list = payload.get("scopes", [])
            
            if username is None:
                raise AuthenticationError("Invalid token: missing username")
            
            return TokenData(username=username, user_id=user_id, scopes=scopes)
            
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
    
    def create_token_response(
        self, 
        user_id: str, 
        username: str, 
        scopes: Optional[list] = None
    ) -> Token:
        """
        Create a complete token response.
        
        Args:
            user_id: User ID
            username: Username
            scopes: Optional scopes list
            
        Returns:
            Token response object
        """
        if scopes is None:
            scopes = []
        
        access_token_expires = timedelta(minutes=self.expire_minutes)
        access_token = self.create_access_token(
            data={
                "sub": username,
                "user_id": user_id,
                "scopes": scopes
            },
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            expires_in=self.expire_minutes * 60  # Convert to seconds
        )


# Global instance
jwt_service = JWTService()