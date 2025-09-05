from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.db.base import Base
from app.db.session import engine

# Routers
from app.routers.users import router as users_router, dashboard_router
from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.categories import router as categories_router
from app.routers.bookings import router as bookings_router
from app.routers.borrow import router as borrow_router
from app.routers.reviews import router as reviews_router
from app.routers.donations import router as donations_router
from app.routers.settings import router as settings_router
from app.routers.notifications import router as notification_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="📚 LMSBS-Fastapi")

app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(books_router, prefix="/api/book")
app.include_router(categories_router, prefix="/api/categories")
app.include_router(bookings_router, prefix="/api/bookings")
app.include_router(borrow_router, prefix="/api/borrow")  # Clean integration, no duplicate
app.include_router(reviews_router, prefix="/api/reviews")
app.include_router(donations_router, prefix="/api/donations")
app.include_router(settings_router, prefix="/api/admin-settings")
app.include_router(notification_router, prefix="/api/notifications")

@app.get("/")
def root():
    return {"message": "📚 LMSBS-Fastapi Backend is running!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="📚 LMSBS-Fastapi",
        version="1.0.0",
        description="LMS API with JWT Bearer Auth",
        routes=app.routes,
    )
    # Add JWT Security globally
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Paste JWT token here with **Bearer** prefix"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
