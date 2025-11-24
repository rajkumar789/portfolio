import time
from functools import wraps
from django.http import JsonResponse
from django.core.cache import cache

def rate_limit(limit=5, period=60):
    """
    Simple rate limiting decorator.
    limit: Number of requests allowed.
    period: Time period in seconds.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get IP address
            ip = request.META.get('REMOTE_ADDR')
            if not ip:
                ip = 'unknown'
            
            # Create a unique cache key based on IP and view name
            key = f"rate_limit_{view_func.__name__}_{ip}"
            
            # Get current request count
            request_count = cache.get(key, 0)
            
            if request_count >= limit:
                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'}, 
                    status=429
                )
            
            # Increment count and set expiry if it's a new key
            if request_count == 0:
                cache.set(key, 1, period)
            else:
                cache.incr(key)
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
