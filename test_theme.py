#!/usr/bin/env python3
"""
Test script to verify the Pantone red theme is working correctly.
"""

import streamlit as st
from theme_config import apply_theme, get_available_themes

def test_pantone_red_theme():
    """Test the Pantone red theme application."""
    
    st.set_page_config(
        page_title="Theme Test",
        page_icon="🎨",
        layout="wide"
    )
    
    # Apply Pantone red theme
    apply_theme(st, "pantone_red")
    
    st.title("🎨 Pantone Red Theme Test")
    st.markdown("Testing the Pantone red navigation with white background.")
    
    # Sidebar test
    st.sidebar.title("Navigation Test")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Theme Verification")
    
    # Test radio buttons
    test_option = st.sidebar.radio(
        "Test Navigation:",
        ["Option 1", "Option 2", "Option 3"]
    )
    
    # Test selectbox
    test_select = st.sidebar.selectbox(
        "Test Dropdown:",
        ["Choice A", "Choice B", "Choice C"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"Selected: {test_option}")
    st.sidebar.write(f"Dropdown: {test_select}")
    
    # Main content test
    st.header("Color Verification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expected Colors")
        st.markdown("""
        ✅ **Navigation Bar**: Pantone Red (#E32636)
        ✅ **Background**: White (#FFFFFF)
        ✅ **Text on White**: Black (#000000)
        ✅ **Text on Red**: White (#FFFFFF)
        """)
    
    with col2:
        st.subheader("Test Elements")
        st.info("Info message test")
        st.success("Success message test")
        st.warning("Warning message test")
        st.error("Error message test")
    
    # Button test
    st.header("Button Test")
    if st.button("Test Button (Should be Pantone Red)"):
        st.success("Button clicked! Color should be Pantone red.")
    
    # File upload test
    st.header("File Upload Test")
    uploaded_file = st.file_uploader("Test File Upload", type=['txt'])
    if uploaded_file is not None:
        st.success("File uploaded! Border should be Pantone red.")
    
    # Dataframe test
    st.header("Dataframe Test")
    import pandas as pd
    test_df = pd.DataFrame({
        'Test Column 1': ['A', 'B', 'C'],
        'Test Column 2': [1, 2, 3],
        'Test Column 3': [True, False, True]
    })
    st.dataframe(test_df)
    
    # Download button test
    st.header("Download Button Test")
    st.download_button(
        label="Download Test File",
        data="This is a test file content.",
        file_name="test.txt",
        mime="text/plain"
    )
    
    # Theme selector test
    st.header("Theme Selector Test")
    available_themes = get_available_themes()
    selected_theme = st.selectbox(
        "Available Themes:",
        available_themes,
        index=available_themes.index("pantone_red") if "pantone_red" in available_themes else 0
    )
    
    st.write(f"Current theme: {selected_theme}")
    
    # Color code display
    st.header("Color Codes")
    st.markdown("""
    | Element | Color | Hex Code |
    |---------|-------|----------|
    | Navigation Bar | Pantone Red | #E32636 |
    | Background | White | #FFFFFF |
    | Text on White | Black | #000000 |
    | Text on Red | White | #FFFFFF |
    | Buttons | Pantone Red | #E32636 |
    """)

if __name__ == "__main__":
    test_pantone_red_theme() 