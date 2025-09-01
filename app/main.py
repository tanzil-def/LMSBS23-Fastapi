from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

# Routers import
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router, dashboard_router  # ✅ import dashboard_router here
from app.routers.books import router as books_router
from app.routers.categories import router as categories_router
from app.routers.borrow import router as borrow_router
from app.routers.bookings import router as bookings_router
from app.routers.reviews import router as reviews_router
from app.routers.donations import router as donations_router
from app.routers.settings import router as settings_router
from app.routers.notifications import router as notification_router

# ✅ Create tables in DB
Base.metadata.create_all(bind=engine)

# ✅ FastAPI instance
app = FastAPI(title="📚 LMSBS-Fastapi")

# ✅ Include routers in proper order
app.include_router(auth_router, prefix="/api/auth")                        # Authentication
app.include_router(users_router, prefix="/api/users")                      # Admin: User Management
app.include_router(dashboard_router, prefix="/api/users/user-dashboard")   # User Dashboard
app.include_router(books_router, prefix="/api/books")                      # Books
app.include_router(categories_router, prefix="/api/categories")            # Categories
app.include_router(bookings_router, prefix="/api/bookings")                # Bookings
app.include_router(borrow_router, prefix="/api/borrow")                    # Borrow
app.include_router(reviews_router, prefix="/api/reviews")                  # Reviews
app.include_router(donations_router, prefix="/api/donations")              # Donations
app.include_router(settings_router, prefix="/api/admin-settings")          # Admin Settings
app.include_router(notification_router, prefix="/api/notifications")      # Notifications

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "📚 LMSBS-Fastapi Backend is running!"}
