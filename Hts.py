import streamlit as st
import pandas as pd

# --------- User Credentials ---------
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "pass456"
}

# --------- Login Page ---------
def login():
    # Set background to white
    st.markdown("""
        <style>
            body {
                background-color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Show logo
    st.image("ucmb-logo1.jpg", width=150)


    st.title("UEC West Nile Surge Dashboard Login")

    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("✅ Login successful. Loading dashboard...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# --------- Load Excel Data ---------
@st.cache_data
def load_data():
    df = pd.read_excel(
        "West Nile New Surge Tracking Dashboard.xlsx",
        sheet_name="HTS"
    )
    return df

# --------- Dashboard ---------
def dashboard():
    st.title("📈 HTS Performance Dashboard")

    # Logout button
    if st.button("🔓 Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.rerun()

    df = load_data()

    # Format % columns
    percent_columns = [col for col in df.columns if "%" in str(col)]

    for col in percent_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (df[col].fillna(0) * 100).round(0).astype(int).astype(str) + "%"

    st.write("### Full HTS Data")
    st.dataframe(df, use_container_width=True)

# --------- Main App ---------
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""

    if st.session_state.get("authenticated", False):
        dashboard()
    else:
        login()

if __name__ == "__main__":
    main()
