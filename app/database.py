import os
from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle special characters in password for Render PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    try:
        # Parse and reconstruct URL to handle special characters
        parsed_url = urllib.parse.urlparse(DATABASE_URL)
        if parsed_url.password:
            password = urllib.parse.quote(parsed_url.password)
            # Reconstruct the URL
            DATABASE_URL = f"postgresql://{parsed_url.username}:{password}@{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}"
    except Exception as e:
        print(f"Warning: Could not parse DATABASE_URL: {e}")

# Create SQLAlchemy engine with appropriate settings
engine_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL settings for production
    engine_args.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    })

try:
    if DATABASE_URL:
        engine = create_engine(DATABASE_URL, **engine_args)
        print(f"✅ Database engine created for: {DATABASE_URL.split('@')[-1]}")
    else:
        raise ValueError("DATABASE_URL is None")
except Exception as e:
    print(f"❌ Error creating database engine: {e}")
    # Fallback for development
    engine = create_engine("sqlite:///./fallback.db", connect_args={"check_same_thread": False})

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
from sqlalchemy.sql.expression import text
def test_database_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False