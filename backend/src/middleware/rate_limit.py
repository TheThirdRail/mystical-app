"""
Rate limiting middleware using Redis.
"""

import time
from typing import Dict, Optional
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis

from src.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis for storage.
    
    Implements a sliding window rate limiter with different limits
    for different endpoint types.
    """
    
    def __init__(self, app, redis_url: str = None):
        """Initialize rate limiter with Redis connection."""
        super().__init__(app)
        self.redis_url = redis_url or settings.REDIS_URL
        self.redis_client: Optional[redis.Redis] = None
        
        # Rate limits per endpoint type (requests per minute)
        self.rate_limits = {
            "/api/v1/auth/": 10,  # Auth endpoints
            "/api/v1/readings/": 5,  # Reading endpoints
            "/api/v1/admin/": 20,  # Admin endpoints
            "default": 60  # Default for other endpoints
        }
    
    async def get_redis_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if self.redis_client is None:
            self.redis_client = redis.from_url(self.redis_url)
        return self.redis_client
    
    def get_client_identifier(self, request: Request) -> str:
        """Get client identifier for rate limiting."""
        # Try to get user ID from auth header if available
        auth_header = request.headers.get("authorization")
        if auth_header:
            # In a real implementation, you'd decode the JWT here
            # For now, use the token as identifier
            return f"user:{auth_header}"
        
        # Fall back to IP address
        client_ip = request.client.host
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip:{client_ip}"
    
    def get_rate_limit(self, path: str) -> int:
        """Get rate limit for a specific path."""
        for prefix, limit in self.rate_limits.items():
            if path.startswith(prefix):
                return limit
        return self.rate_limits["default"]
    
    async def check_rate_limit(
        self, 
        client_id: str, 
        path: str, 
        limit: int
    ) -> tuple[bool, Dict[str, int]]:
        """
        Check if request is within rate limit.
        
        Returns:
            Tuple of (is_allowed, headers_dict)
        """
        try:
            redis_client = await self.get_redis_client()
            current_time = int(time.time())
            window_start = current_time - 60  # 1 minute window
            
            # Redis key for this client and endpoint
            key = f"rate_limit:{client_id}:{path}"
            
            # Remove old entries outside the window
            await redis_client.zremrangebyscore(key, 0, window_start)
            
            # Count current requests in window
            current_requests = await redis_client.zcard(key)
            
            # Check if limit exceeded
            if current_requests >= limit:
                # Get time until window resets
                oldest_request = await redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_request:
                    reset_time = int(oldest_request[0][1]) + 60
                    retry_after = max(1, reset_time - current_time)
                else:
                    retry_after = 60
                
                headers = {
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                    "Retry-After": str(retry_after)
                }
                return False, headers
            
            # Add current request to window
            await redis_client.zadd(key, {str(current_time): current_time})
            await redis_client.expire(key, 60)  # Expire key after window
            
            # Calculate remaining requests
            remaining = limit - current_requests - 1
            reset_time = current_time + 60
            
            headers = {
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset_time)
            }
            
            return True, headers
            
        except Exception as e:
            # If Redis is down, allow the request but log the error
            print(f"Rate limiting error: {e}")
            return True, {}
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc"]:
            return await call_next(request)
        
        client_id = self.get_client_identifier(request)
        path = request.url.path
        limit = self.get_rate_limit(path)
        
        # Check rate limit
        is_allowed, headers = await self.check_rate_limit(client_id, path, limit)
        
        if not is_allowed:
            # Return rate limit exceeded response
            response = Response(
                content='{"detail": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json"
            )
            for key, value in headers.items():
                response.headers[key] = value
            return response
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value
        
        return response
