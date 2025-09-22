from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Routers
from app.routers.users import router as users_router, dashboard_router
from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.categories import router as categories_router
from app.routers.bookings import router as bookings_router
from app.routers.borrow import router as borrow_router
from app.routers.reviews import router as reviews_router
from app.routers.donations import router as donation_router
from app.routers.featured import router as featured_router
from app.routers.settings import router as settings_router
from app.routers.notifications import router as notification_router

# Create all tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title="📚 LMSBS-Fastapi")

# ===== CORS Middleware =====
origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5174",  # Vite dev server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Include Routers =====
app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(books_router, prefix="/api/book")
app.include_router(categories_router, prefix="/api/categories")
app.include_router(bookings_router, prefix="/api/bookings")
app.include_router(borrow_router, prefix="/api/borrow")
app.include_router(reviews_router, prefix="/api/reviews")
app.include_router(donation_router, prefix="/api/donations")
app.include_router(featured_router)
app.include_router(settings_router, prefix="/api/admin-settings")
app.include_router(notification_router, prefix="/api/notifications")

# Root endpoint
@app.get("/")
def root():
    return {"message": "📚 LMSBS-Fastapi Backend is running!"}

# ===== Custom OpenAPI with JWT security =====
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="📚 LMSBS-Fastapi",
        version="1.0.0",
        description="LMS API with JWT Bearer Auth",
        routes=app.routes,
    )

    # Ensure 'components' exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Add JWT security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Paste JWT token here with **Bearer** prefix"
        }
    }

    # Apply security to all endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign custom OpenAPI function
app.openapi = custom_openapi
