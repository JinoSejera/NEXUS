from fastapi import Request


def get_client_ip(request: Request):
    x_client_ip = request.headers.get("X-Client-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    fallback = request.client.host

    ip = x_client_ip or (x_forwarded_for.split(",")[0] if x_forwarded_for else fallback)
    
    return ip