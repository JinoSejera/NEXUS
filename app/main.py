from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints.capstone_title_generator_rrls import router as capstone_title_generator_router
from .services.get_client_ip import get_client_ip
import logging
import time
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Rate Limiting
app.state.limiter = Limiter(key_func=get_client_ip)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_request(request:Request, call_next):
    client_ip = get_client_ip(request)
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}\nFrom IP: {client_ip}")
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Error occured: {str(e)}")
        response = JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "detail": str(e)}
        )
    
    process_time = time.time() - start_time
    logger.info(f"Request completed in {process_time:.2f}s with status {response.status_code}")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request:Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal servcer error", "detail": str(exc)}
    )

app.include_router(capstone_title_generator_router)
