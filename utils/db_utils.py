import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL

# Define the SQLAlchemy base class
Base = declarative_base()

# Define PageVisit model as an example
class PageVisit(Base):
    __tablename__ = "page_visits"
    
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    referrer = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    device = Column(String(100), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

# Create the engine, bind it to the sessionmaker
def get_db_session():
    """Get a database session"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

# Initialize the database if this file is run directly
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")