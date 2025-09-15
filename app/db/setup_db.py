from app.db.session import engine
from app.db.base import Base

# Import all models BEFORE create_all
from app.models.user import User
from app.models.booking import Booking
from app.models.borrow import Borrow
from app.models.review import Review
from app.models.donations import DonationRequest
from app.models.book import Book
from app.models.category import Category  # if you have

Base.metadata.create_all(bind=engine)
print("✅ All tables created safely")
