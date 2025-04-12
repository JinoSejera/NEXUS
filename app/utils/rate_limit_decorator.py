import functools
from fastapi import Request
from slowapi import Limiter


def rate_limited(limit: str):
    """
    Decorator to apply rate limiting using app.state.limiter with a custom limit string.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract Request object from args or kwargs
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise RuntimeError("Request object not found for rate limiting")

            limiter: Limiter = request.app.state.limiter
            decorated_func = limiter.limit(limit)(func)
            return await decorated_func(*args, **kwargs)
        return wrapper
    return decorator
