from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

# Routers import
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router, dashboard_router
from app.routers.books import router as books_router
from app.routers.categories import router as categories_router
from app.routers.borrow import router as borrow_router
from app.routers.bookings import router as bookings_router
from app.routers.reviews import router as reviews_router
from app.routers.donations import router as donations_router
from app.routers.settings import router as settings_router
from app.routers.notifications import router as notification_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="📚 LMSBS-Fastapi")

# Routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router, prefix="/api/users")
app.include_router(dashboard_router, prefix="/api/users/user-dashboard")
app.include_router(books_router, prefix="/api/books")
app.include_router(categories_router, prefix="/api/categories")
app.include_router(bookings_router, prefix="/api/bookings")
app.include_router(borrow_router, prefix="/api/borrow")
app.include_router(reviews_router, prefix="/api/reviews")
app.include_router(donations_router, prefix="/api/donations")
app.include_router(settings_router, prefix="/api/admin-settings")
app.include_router(notification_router, prefix="/api/notifications")

@app.get("/")
def root():
    return {"message": "📚 LMSBS-Fastapi Backend is running!"}
