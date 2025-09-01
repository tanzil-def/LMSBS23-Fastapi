from app.db.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.models.user_role import UserRole

def main():
    db = SessionLocal()
    try:
        admin_user = UserCreate(
            username="admin",
            name="Admin User",
            email="admin@gmail.com",
            password="admin123",
            role=UserRole.ADMIN
        )
        create_user(db, admin_user)
        print("Admin created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
