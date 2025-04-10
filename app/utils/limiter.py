from slowapi import Limiter
from ..services.get_client_ip import get_client_ip

limiter = Limiter(key_func=get_client_ip)
