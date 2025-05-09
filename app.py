# app.py
import streamlit as st
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import APP_NAME, load_user_settings
from utils.auth_utils import init_auth, login_page, logout

# Configure the page
st.set_page_config(
    page_title=APP_NAME,
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and authentication
init_auth()

# Check if user is authenticated
if not st.session_state.authenticated:
    login_page()
else:
    # Load user settings
    settings = load_user_settings()
    
    # Sidebar with navigation
    with st.sidebar:
        st.title("Navigation")
        
        # Create navigation menu
        selected_page = st.radio(
            "Select a section:",
            [
                "Dashboard Home",
                "Website Analytics",
                "SEO & Uptime Checker",
                "Invoice & Project Tracker",
                "Learning Goals + Pomodoro",
                "Data Analysis",
                "AI Assistant",
                "Reports",
                "Settings"
            ]
        )
        
        # Add username display
        st.write(f"Logged in as: {st.session_state.username}")
        
        # Logout button
        if st.button("Logout"):
            logout()
            st.rerun()
    
    # Main content based on selected page
    if selected_page == "Dashboard Home":
        st.title(f"Welcome to {APP_NAME}")
        st.write("Your personal development dashboard")
        
        # Create a dashboard overview with columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Active Projects", value="5")
        
        with col2:
            st.metric(label="Pending Invoices", value="3", delta="$1,250")
        
        with col3:
            st.metric(label="Website Uptime", value="99.8%", delta="0.2%")
            
        # Recent activity
        st.subheader("Recent Activity")
        st.info("This section will display your recent activities across all modules.")
        
        # Quick overview of all modules
        st.subheader("Quick Overview")
        
        module_cols = st.columns(3)
        
        with module_cols[0]:
            st.write("### Analytics")
            st.info("124 visits today")
            
        with module_cols[1]:
            st.write("### Projects")
            st.info("2 projects due this week")
            
        with module_cols[2]:
            st.write("### Learning")
            st.info("3 pomodoro sessions completed today")
    
    elif selected_page == "Website Analytics":
        from pages.analytics import integrate as integrate_analytics
        integrate_analytics()
    
    elif selected_page == "SEO & Uptime Checker":
        st.title("SEO & Uptime Checker")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for SEO & Uptime feature
        st.subheader("Check Website SEO")
        url = st.text_input("Enter a website URL to check:", "https://example.com")
        if st.button("Analyze SEO"):
            st.success(f"SEO analysis for {url} will be implemented in the next version!")
    
    elif selected_page == "Invoice & Project Tracker":
        st.title("Invoice & Project Tracker")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for project management
        st.subheader("Projects & Invoices")
        st.write("Track your client projects and invoices here.")
    
    elif selected_page == "Learning Goals + Pomodoro":
        st.title("Learning Goals + Pomodoro")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for learning tracker
        st.subheader("Learning Goals")
        st.write("Track your learning progress and use the Pomodoro timer.")
    
    elif selected_page == "Data Analysis":
        st.title("Data Analysis")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for data analysis
        st.subheader("Upload & Analyze Data")
        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file is not None:
            st.success("File uploaded successfully! Analysis features coming soon.")
    
    elif selected_page == "AI Assistant":
        st.title("AI Assistant")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for AI assistant
        st.subheader("CodRon Bot")
        user_input = st.text_input("Ask me anything:")
        if user_input:
            st.write(f"AI response to: '{user_input}' will be implemented in the next version!")
    
    elif selected_page == "Reports":
        st.title("Reports")
        st.info("This module is under development. Check back soon!")
        
        # Placeholder for reports
        st.subheader("Generate Reports")
        report_type = st.selectbox("Select report type:", ["Daily Summary", "Weekly Summary", "Monthly Summary"])
        if st.button("Generate Report"):
            st.success(f"{report_type} will be implemented in the next version!")
    
    elif selected_page == "Settings":
        st.title("Settings")
        
        # Theme selection
        theme = st.selectbox(
            "Select theme:",
            ["Dark", "Light"],
            index=0 if settings["theme"] == "dark" else 1
        )
        
        # Module toggles
        st.subheader("Enable/Disable Modules")
        for module, enabled in settings["enabled_modules"].items():
            settings["enabled_modules"][module] = st.toggle(
                f"Enable {module.replace('_', ' ').title()}", 
                value=enabled
            )
        
        # OpenAI API key for AI assistant
        st.subheader("API Keys")
        api_key = st.text_input(
            "OpenAI API Key", 
            value=settings["openai_api_key"],
            type="password"
        )
        
        # Save button
        if st.button("Save Settings"):
            settings["theme"] = "dark" if theme == "Dark" else "light"
            settings["openai_api_key"] = api_key
            from config import save_user_settings
            save_user_settings(settings)
            st.success("Settings saved successfully!")