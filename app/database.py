import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle special characters in password for Render PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    # Parse and reconstruct URL to handle special characters
    parsed_url = urllib.parse.urlparse(DATABASE_URL)
    # Re-encode the password (ensure it's not None)
    password = urllib.parse.quote_plus(parsed_url.password or "")
    # Only include port if it exists
    port_part = f":{parsed_url.port}" if parsed_url.port else ""
    DATABASE_URL = f"postgresql://{parsed_url.username}:{password}@{parsed_url.hostname}{port_part}{parsed_url.path}"

# Create SQLAlchemy engine
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, 
        # PostgreSQL-specific settings for production
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,  # Recycle connections after 5 minutes
    )
else:
    engine = None

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
from sqlalchemy import text
def test_database_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False