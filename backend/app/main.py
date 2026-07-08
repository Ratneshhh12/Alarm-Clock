from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import auth, users

app = FastAPI(
    title="Intelligent Cognitive Alarm Platform API",
    description="Milestone 1: Project Setup and JWT Authentication",
    version="1.0.0"
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "The request payload validation failed.",
            "details": exc.errors()
        }
    )

# Custom exception handler for HTTPExceptions to ensure uniform error format
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "Error occurred",
            "message": str(exc.detail)
        }
    )

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict access in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication and User Management Routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    """Service status and landing message."""
    return {
        "message": "Welcome to the Intelligent Cognitive Alarm Platform API",
        "milestone": "Milestone 1 (Base Project & Auth)",
        "status": "Operational"
    }

