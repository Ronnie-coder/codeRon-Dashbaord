# utils/sample_data.py
import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_utils import get_db_session, PageVisit

def generate_sample_analytics_data():
    """Generate sample website analytics data for demo purposes."""
    with get_db_session() as session:
        # Check if we already have data
        if session.query(PageVisit).count() > 0:
            print("Analytics data already exists.")
            return
        
        # Sample websites and pages
        websites = [
            "example.com",
            "mywebsite.io",
            "codronblog.com"
        ]
        
        pages = [
            "/",
            "/about",
            "/blog",
            "/contact",
            "/products",
            "/services"
        ]
        
        referrers = [
            "https://google.com",
            "https://facebook.com",
            "https://twitter.com",
            "https://linkedin.com",
            "direct",
            None
        ]
        
        devices = [
            "Desktop",
            "Mobile",
            "Tablet"
        ]
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
        ]
        
        # Generate 100 sample visits
        sample_visits = []
        for _ in range(100):
            # Random dates in the last 30 days
            random_days = random.randint(0, 30)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            visit_time = datetime.now() - timedelta(
                days=random_days,
                hours=random_hours,
                minutes=random_minutes
            )
            
            website = random.choice(websites)
            page = random.choice(pages)
            
            visit = PageVisit(
                url=f"https://{website}",
                path=page,
                referrer=random.choice(referrers),
                ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                location=random.choice(["United States", "Canada", "UK", "Germany", "India", "Australia"]),
                device=random.choice(devices),
                user_agent=random.choice(user_agents),
                timestamp=visit_time
            )
            
            sample_visits.append(visit)
        
        # Add to database
        session.add_all(sample_visits)
        session.commit()
        print(f"Added {len(sample_visits)} sample page visits.")

if __name__ == "__main__":
    generate_sample_analytics_data()
    print("Sample data generated successfully.")