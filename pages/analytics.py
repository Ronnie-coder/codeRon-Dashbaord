# pages/analytics.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_utils import get_db_session, PageVisit

def display_analytics():
    st.title("Website Analytics")
    
    # Add JS tracker snippet for demonstration
    with st.expander("JavaScript Tracker for Your Website"):
        st.code("""
<!-- CodRon Analytics Tracker -->
<script>
  (function() {
    var d = document;
    var s = d.createElement('script');
    s.src = 'https://your-analytics-api.com/tracker.js';
    s.async = true;
    d.head.appendChild(s);
    
    window.codronTracker = window.codronTracker || function() {
      (window.codronTracker.q = window.codronTracker.q || []).push(arguments);
    };
    
    window.codronTracker('pageview');
  })();
</script>
        """, language="html")
    
    # Fetch analytics data from the database
    with get_db_session() as session:
        results = session.query(PageVisit).all()
        if not results:
            st.warning("No analytics data available. Would you like to generate sample data for demonstration?")
            if st.button("Generate Sample Data"):
                # Import and run sample data generator
                from utils.sample_data import generate_sample_analytics_data
                generate_sample_analytics_data()
                st.success("Sample data generated successfully! Please refresh the page.")
                st.rerun()
            return
        
        # Convert to DataFrame for easier manipulation
        data = [{
            "URL": r.url,
            "Path": r.path,
            "Referrer": r.referrer if r.referrer else "Direct",
            "Device": r.device,
            "Location": r.location,
            "Timestamp": r.timestamp
        } for r in results]
        
        df = pd.DataFrame(data)
    
    # Display key metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visits = len(df)
        st.metric("Total Visits", f"{total_visits:,}")
    
    with col2:
        unique_visitors = df["URL"].nunique()
        st.metric("Unique URLs", f"{unique_visitors:,}")
    
    with col3:
        popular_page = df["Path"].value_counts().idxmax()
        st.metric("Most Popular Page", popular_page)
    
    with col4:
        top_referrer = df["Referrer"].value_counts().idxmax()
        st.metric("Top Referrer", top_referrer)
    
    # Visits over time chart
    st.subheader("Visits Over Time")
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    visits_per_day = df.groupby("Date").size().reset_index(name="Visits")
    visits_per_day["Date"] = pd.to_datetime(visits_per_day["Date"])
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=visits_per_day, x="Date", y="Visits", ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Display additional charts in tabs
    tab1, tab2, tab3 = st.tabs(["Traffic Sources", "Device Breakdown", "Popular Pages"])
    
    with tab1:
        st.subheader("Traffic Sources")
        referrer_counts = df["Referrer"].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        referrer_counts.plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            ax=ax,
            label=""
        )
        plt.axis('equal')
        plt.title("Traffic Sources")
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Device Breakdown")
        device_counts = df["Device"].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=device_counts.index, y=device_counts.values, ax=ax)
        plt.title("Visits by Device Type")
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Popular Pages")
        page_counts = df["Path"].value_counts().reset_index()
        page_counts.columns = ["Page", "Visit Count"]
        
        # Sort by visit count in descending order
        page_counts = page_counts.sort_values("Visit Count", ascending=False)
        
        # Display as a bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Visit Count", y="Page", data=page_counts.head(10), ax=ax)
        plt.title("Top 10 Pages by Visit Count")
        plt.tight_layout()
        st.pyplot(fig)
        
        # Also display as a table
        st.dataframe(page_counts)
    
    # Raw data view
    with st.expander("View Raw Data"):
        st.dataframe(df)

def integrate():
    display_analytics()

if __name__ == "__main__":
    display_analytics()