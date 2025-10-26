from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL
import secrets
import string

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def generate_referral_code():
    """Generate unique referral code"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))
