# Example: How to Customize Colors Manually
# This shows different ways to change the interface colors

import streamlit as st

def apply_custom_colors():
    """Example of manually applying custom colors."""
    
    # Method 1: Simple color changes
    st.markdown("""
    <style>
    /* Change sidebar background to purple */
    .css-1d391kg {
        background-color: #6a4c93 !important;
    }
    
    /* Change sidebar text to white */
    .css-1d391kg .css-1v0mbdj {
        color: white !important;
    }
    
    /* Change main background to light purple */
    .main {
        background-color: #f8f5ff !important;
    }
    
    /* Change button color to purple */
    .stButton > button {
        background-color: #6a4c93 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_gradient_theme():
    """Example of applying a gradient theme."""
    
    st.markdown("""
    <style>
    /* Gradient background for sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Gradient background for main area */
    .main {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    }
    
    /* Glass effect for cards */
    .stMarkdown {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_dark_theme():
    """Example of applying a dark theme."""
    
    st.markdown("""
    <style>
    /* Dark sidebar */
    .css-1d391kg {
        background-color: #1a1a1a !important;
    }
    
    /* Dark main background */
    .main {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* Dark text */
    .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Dark headers */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Dark buttons */
    .stButton > button {
        background-color: #4a4a4a !important;
        color: white !important;
        border: 1px solid #666 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Example usage in main app
def main():
    st.set_page_config(
        page_title="Custom Theme Example",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 Custom Theme Examples")
    
    # Theme selector
    theme_option = st.sidebar.selectbox(
        "Choose Theme Style:",
        ["Default", "Purple Theme", "Gradient Theme", "Dark Theme"]
    )
    
    if theme_option == "Purple Theme":
        apply_custom_colors()
    elif theme_option == "Gradient Theme":
        apply_gradient_theme()
    elif theme_option == "Dark Theme":
        apply_dark_theme()
    
    st.header("Theme Customization Examples")
    
    st.markdown("""
    ### How to Customize Colors:
    
    1. **Change Sidebar Colors:**
       ```css
       .css-1d391kg {
           background-color: #your-color !important;
       }
       ```
    
    2. **Change Button Colors:**
       ```css
       .stButton > button {
           background-color: #your-color !important;
       }
       ```
    
    3. **Change Text Colors:**
       ```css
       .stMarkdown {
           color: #your-color !important;
       }
       ```
    
    4. **Change Background:**
       ```css
       .main {
           background-color: #your-color !important;
       }
       ```
    """)
    
    # Example content
    st.subheader("Sample Content")
    st.write("This is sample content to show how the theme looks.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("This is an info box")
        st.success("This is a success message")
    
    with col2:
        st.warning("This is a warning")
        st.error("This is an error message")
    
    if st.button("Sample Button"):
        st.write("Button clicked!")

if __name__ == "__main__":
    main() 