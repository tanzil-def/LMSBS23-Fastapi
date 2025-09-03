from sqlalchemy.exc import IntegrityError
from app.db.database import SessionLocal
from app.crud.user import create_user, get_user_by_username
from app.schemas.user import RegisterRequest
from app.models.user_role import UserRole
from passlib.context import CryptContext

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def main():
    db = SessionLocal()
    try:
        username = "admin"
        email = "admin@gmail.com"

        # Check if admin already exists
        existing = get_user_by_username(db, username)
        if existing:
            print(f"Admin user '{username}' already exists. Skipping creation.")
            return

        # Create admin user object
        admin_user = RegisterRequest(
            username=username,
            name="Admin User",
            email=email,
            password="admin123",  # plaintext, will hash next
            role="ADMIN"
        )

        # Hash password
        admin_user.password = pwd_context.hash(admin_user.password)

        # Create user in database
        create_user(db, admin_user, role=UserRole.ADMIN)
        print(f"Admin '{username}' created successfully!")

    except IntegrityError as e:
        db.rollback()
        print(f"Database Integrity Error: {e.orig}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
