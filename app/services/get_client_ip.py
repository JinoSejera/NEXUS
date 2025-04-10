from fastapi import Request

def get_client_ip(request: Request):
    """Extract client IP from X-Client-IP (if sent), X-Forwarded-For or fallback to client.host."""
    x_client_ip = request.headers.get("X-Client-IP")
    if x_client_ip:
        return x_client_ip.strip()
    
    forward_for = request.headers.get("X-Forwarded-For")
    if forward_for:
        return forward_for.split(',')[0] # Extract the first IP in the list
    return request.client.host # Fallback to the client's IP address