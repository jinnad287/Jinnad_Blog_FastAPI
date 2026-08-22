from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import time

from app.database.base import Base
from app.database.session import engine
from app.core.logger import logger
from app.core.exceptions import AppException, ErrorResponse
from app.api import user_routes, blog_routes


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    start_time = time.time()
    yield
    end_time = time.time()
    logger.info(f"Application shutdown. Total uptime: {end_time - start_time:.2f} seconds")


app = FastAPI(
    title="Blog App",
    description="A sample FastAPI application with structured logging and error handling",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(blog_routes.router, prefix="/blogs", tags=["blogs"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response  = await call_next(request)
    duration = time.time() - start_time
    logger.info("f{request.method} {request.url} - {response.status_code} - {duration:.2f} seconds")
    return response


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.error_type} - {exc.message} - Details: {exc.details}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            error_type=exc.error_type,
            message=exc.message,
            details=exc.details
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status_code=500,
            error_type="InternalServerError",
            message="An unexpected error occured."
        ).model_dump()
    )

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy",
            "time": datetime.utcnow().isoformat()
            }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
