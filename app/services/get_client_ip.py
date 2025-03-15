from fastapi import Request

def get_client_ip(request: Request):
    """Extracts the real client IP even when behind a reverse proxy like Azure."""
    forward_for = request.headers.get("X-Forwarded-For")
    if forward_for:
        return forward_for.split(',')[0] # Extract the first IP in the list
    return request.client.host # Fallback to the client's IP address