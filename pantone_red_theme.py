# Pantone Red Theme - Manual CSS Application
# This shows how to apply Pantone red navigation with white background

import streamlit as st

def apply_pantone_red_theme():
    """Apply Pantone red navigation with white background."""
    
    st.markdown("""
    <style>
    /* Main background - White */
    .main {
        background-color: #FFFFFF !important;
    }
    
    /* Sidebar background - Pantone Red */
    .css-1d391kg {
        background-color: #E32636 !important;
    }
    
    /* Sidebar title and text - White */
    .css-1d391kg .css-1v0mbdj {
        color: #FFFFFF !important;
    }
    
    /* Sidebar radio buttons - White text on darker red */
    .css-1d391kg .stRadio > label {
        color: #FFFFFF !important;
        background-color: #B91C1C !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 4px 0 !important;
    }
    
    /* Sidebar radio buttons when selected - White text on Pantone red */
    .css-1d391kg .stRadio > label[data-baseweb="radio"] {
        background-color: #E32636 !important;
        color: #FFFFFF !important;
    }
    
    /* Main title and headers - Black text on white background */
    .css-10trblm {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* All headers - Black text */
    h1, h2, h3 {
        color: #000000 !important;
    }
    
    /* Regular text - Black on white */
    .stMarkdown {
        color: #000000 !important;
    }
    
    /* Buttons - Pantone red background, white text */
    .stButton > button {
        background-color: #E32636 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background-color: #B91C1C !important;
    }
    
    /* File uploader - Pantone red border */
    .stFileUploader {
        border: 2px dashed #E32636 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }
    
    /* Dataframe - Clean borders */
    .dataframe {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    /* Download button - Green for success */
    .stDownloadButton > button {
        background-color: #059669 !important;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #047857 !important;
    }
    
    /* Success message - Green background */
    .stSuccess {
        background-color: #D1FAE5 !important;
        border-color: #A7F3D0 !important;
        color: #065F46 !important;
    }
    
    /* Error message - Red background */
    .stError {
        background-color: #FEE2E2 !important;
        border-color: #FECACA !important;
        color: #991B1B !important;
    }
    
    /* Info message - Blue background */
    .stInfo {
        background-color: #DBEAFE !important;
        border-color: #BFDBFE !important;
        color: #1E40AF !important;
    }
    
    /* Links - Pantone red */
    a {
        color: #E32636 !important;
    }
    
    a:hover {
        color: #B91C1C !important;
    }
    
    /* Sidebar selectbox - White text on red */
    .css-1d391kg .stSelectbox > div > div {
        color: #FFFFFF !important;
    }
    
    /* Sidebar selectbox options - Black text on white */
    .css-1d391kg .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Pantone Red Theme Example",
        page_icon="🎨",
        layout="wide"
    )
    
    # Apply the Pantone red theme
    apply_pantone_red_theme()
    
    st.title("🎨 Pantone Red Theme Example")
    st.markdown("This demonstrates the Pantone red navigation bar with white background.")
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Theme Features")
    st.sidebar.write("• Pantone Red (#E32636) sidebar")
    st.sidebar.write("• White background")
    st.sidebar.write("• Black text for readability")
    st.sidebar.write("• White text on red elements")
    
    # Main content
    st.header("Color Scheme")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Colors Used")
        st.markdown("""
        - **Pantone Red**: #E32636 (Navigation bar)
        - **White**: #FFFFFF (Background)
        - **Black**: #000000 (Text on white)
        - **White**: #FFFFFF (Text on red)
        """)
    
    with col2:
        st.subheader("Accessibility")
        st.markdown("""
        - High contrast for readability
        - Black text on white background
        - White text on red background
        - Consistent color scheme
        """)
    
    # Example elements
    st.header("Example Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("This is an info message")
        st.success("This is a success message")
        if st.button("Sample Button"):
            st.write("Button clicked!")
    
    with col2:
        st.warning("This is a warning")
        st.error("This is an error message")
        st.download_button(
            label="Download Example",
            data="Sample data",
            file_name="example.txt",
            mime="text/plain"
        )
    
    # File upload example
    st.header("File Upload Example")
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf'])
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
    
    # Dataframe example
    st.header("Dataframe Example")
    import pandas as pd
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': ['A', 'B', 'C', 'D'],
        'Column 3': [True, False, True, False]
    })
    st.dataframe(df)

if __name__ == "__main__":
    main() 