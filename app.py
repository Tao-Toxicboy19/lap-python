import streamlit as st
from pymongo import MongoClient
import plotly.graph_objects as go

st.set_page_config(page_title="Home Dashboard", layout="centered")

url = "mongodb://root:example@localhost:27017/examdb?authSource=admin"

try:
    client = MongoClient(url)
    db = client["examdb"]
    client.admin.command('ping')

except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")

# Check if the user is logged in, and set the appropriate page icon
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Function to verify login credentials
def login(username, password):
    users_collection = db["examauth"]
    user = users_collection.find_one(
        {"username": username,
         "password": password
         })
    if user:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        return True
    return False

# Function to display the login page
def login_page():
    st.title("Login Page")

    # Create a form for user login
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        # Check credentials
        if submit:
            if login(username, password):
                st.success(f"Welcome, {username}! 🎉 Redirecting to the main page...")
                st.rerun()  # Reload the page to show main page after login
            else:
                st.error("Invalid username or password. Please try again.")

# Home dashboard with temperature and humidity tabs
def home_dashboard():
    st.title("🏠 Home Dashboard")

    # Create two tabs for Temperature and Humidity
    col1, col2= st.columns(2)

    with col1:
        st.subheader("Temperature")
        # Create a gauge for Temperature
        gauge_temp = go.Figure(go.Indicator(
            mode="gauge+number",
            value=14,  # Replace with actual temperature value
            gauge={
                'axis': {'range': [0, 70]},
                'bar': {'color': "#e1704c"},
                'steps': [
                    {'range': [0, 20], 'color': "#e2e6bd"},
                    {'range': [20, 50], 'color': "#e8c33c"}
                ]
            },
            title={'text': "Temperature"}
        ))
        st.plotly_chart(gauge_temp)

    with col2:
        st.subheader("Humidity")
        # Create a gauge for Humidity
        gauge_humidity = go.Figure(go.Indicator(
            mode="gauge+number",
            value=14,  # Replace with actual humidity value
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#e1704c"},
                'steps': [
                    {'range': [0, 20], 'color': "#e2e6bd"},
                    {'range': [20, 50], 'color': "#e8c33c"}
                ]
            },
            title={'text': "Humidity"}
        ))
        st.plotly_chart(gauge_humidity)

    if st.button("Log out"):
        st.session_state["logged_in"] = False

# Main application logic: Show login page if not logged in, else show main page
if st.session_state["logged_in"]:
    home_dashboard()  # Show main page if logged in
else:
    login_page()  # Show login page if not logged in