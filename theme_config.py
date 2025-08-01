# Theme Configuration for Vendor Evaluation Tool
# Modify these colors to customize the appearance

# Color Schemes
COLOR_SCHEMES = {
    "default": {
        "primary": "#3498db",      # Blue
        "secondary": "#2c3e50",    # Dark Blue
        "accent": "#e74c3c",       # Red
        "success": "#27ae60",      # Green
        "warning": "#f39c12",      # Orange
        "error": "#e74c3c",        # Red
        "background": "#f8f9fa",   # Light Gray
        "sidebar_bg": "#2c3e50",   # Dark Blue
        "sidebar_text": "#ecf0f1", # Light Gray
        "text_primary": "#2c3e50", # Dark Blue
        "text_secondary": "#7f8c8d" # Gray
    },
    "corporate": {
        "primary": "#1f4e79",      # Corporate Blue
        "secondary": "#2c3e50",    # Dark Blue
        "accent": "#e67e22",       # Orange
        "success": "#27ae60",      # Green
        "warning": "#f39c12",      # Orange
        "error": "#e74c3c",        # Red
        "background": "#ffffff",    # White
        "sidebar_bg": "#1f4e79",   # Corporate Blue
        "sidebar_text": "#ffffff",  # White
        "text_primary": "#2c3e50", # Dark Blue
        "text_secondary": "#7f8c8d" # Gray
    },
    "modern": {
        "primary": "#6366f1",      # Indigo
        "secondary": "#374151",    # Gray
        "accent": "#f59e0b",       # Amber
        "success": "#10b981",      # Emerald
        "warning": "#f59e0b",      # Amber
        "error": "#ef4444",        # Red
        "background": "#f9fafb",   # Light Gray
        "sidebar_bg": "#374151",   # Gray
        "sidebar_text": "#f9fafb", # Light Gray
        "text_primary": "#111827", # Dark Gray
        "text_secondary": "#6b7280" # Gray
    },
    "dark": {
        "primary": "#3b82f6",      # Blue
        "secondary": "#1f2937",    # Dark Gray
        "accent": "#f59e0b",       # Amber
        "success": "#10b981",      # Emerald
        "warning": "#f59e0b",      # Amber
        "error": "#ef4444",        # Red
        "background": "#111827",   # Dark Gray
        "sidebar_bg": "#1f2937",   # Dark Gray
        "sidebar_text": "#f9fafb", # Light Gray
        "text_primary": "#f9fafb", # Light Gray
        "text_secondary": "#9ca3af" # Gray
    },
    "pantone_red": {
        "primary": "#E32636",      # Pantone Red
        "secondary": "#B91C1C",    # Darker Red
        "accent": "#DC2626",       # Red Accent
        "success": "#059669",      # Green
        "warning": "#D97706",      # Orange
        "error": "#DC2626",        # Red
        "background": "#FFFFFF",   # White
        "sidebar_bg": "#E32636",   # Pantone Red
        "sidebar_text": "#FFFFFF", # White
        "text_primary": "#000000", # Black
        "text_secondary": "#374151" # Dark Gray
    }
}

def get_custom_css(theme_name="default"):
    """Generate custom CSS based on the selected theme."""
    colors = COLOR_SCHEMES.get(theme_name, COLOR_SCHEMES["default"])
    
    return f"""
    <style>
    /* Main background color */
    .main {{
        background-color: {colors['background']};
    }}
    
    /* Sidebar styling - Multiple selectors for compatibility */
    .css-1d391kg,
    .css-1lcbmhc,
    .css-1dp5vir,
    .css-1r6slb0,
    .css-1wivap2,
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {{
        background-color: {colors['sidebar_bg']} !important;
    }}
    
    /* Sidebar title color */
    .css-1d391kg .css-1v0mbdj,
    .css-1lcbmhc .css-1v0mbdj,
    .css-1dp5vir .css-1v0mbdj,
    .css-1r6slb0 .css-1v0mbdj,
    .css-1wivap2 .css-1v0mbdj,
    [data-testid="stSidebar"] .css-1v0mbdj,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p {{
        color: {colors['sidebar_text']} !important;
    }}
    
    /* Sidebar radio buttons */
    .css-1d391kg .stRadio > label,
    .css-1lcbmhc .stRadio > label,
    .css-1dp5vir .stRadio > label,
    .css-1r6slb0 .stRadio > label,
    .css-1wivap2 .stRadio > label,
    [data-testid="stSidebar"] .stRadio > label {{
        color: {colors['sidebar_text']} !important;
        background-color: {colors['secondary']} !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 4px 0 !important;
    }}
    
    /* Sidebar radio buttons when selected */
    .css-1d391kg .stRadio > label[data-baseweb="radio"],
    .css-1lcbmhc .stRadio > label[data-baseweb="radio"],
    .css-1dp5vir .stRadio > label[data-baseweb="radio"],
    .css-1r6slb0 .stRadio > label[data-baseweb="radio"],
    .css-1wivap2 .stRadio > label[data-baseweb="radio"],
    [data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] {{
        background-color: {colors['primary']} !important;
        color: white !important;
    }}
    
    /* Main title styling */
    .css-10trblm {{
        color: {colors['text_primary']} !important;
        font-weight: bold !important;
    }}
    
    /* Headers styling */
    h1, h2, h3 {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Success message styling */
    .stSuccess {{
        background-color: #d4edda !important;
        border-color: #c3e6cb !important;
        color: #155724 !important;
    }}
    
    /* Error message styling */
    .stError {{
        background-color: #f8d7da !important;
        border-color: #f5c6cb !important;
        color: #721c24 !important;
    }}
    
    /* Info message styling */
    .stInfo {{
        background-color: #d1ecf1 !important;
        border-color: #bee5eb !important;
        color: #0c5460 !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {colors['primary']} !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
    }}
    
    .stButton > button:hover {{
        background-color: {colors['secondary']} !important;
    }}
    
    /* File uploader styling */
    .stFileUploader {{
        border: 2px dashed {colors['primary']} !important;
        border-radius: 8px !important;
        background-color: {colors['background']} !important;
    }}
    
    /* Dataframe styling */
    .dataframe {{
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
    }}
    
    /* Download button styling */
    .stDownloadButton > button {{
        background-color: {colors['success']} !important;
        color: white !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {colors['secondary']} !important;
    }}
    
    /* Text color */
    .stMarkdown {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Link color */
    a {{
        color: {colors['primary']} !important;
    }}
    
    a:hover {{
        color: {colors['secondary']} !important;
    }}
    </style>
    """

def get_available_themes():
    """Return list of available theme names."""
    return list(COLOR_SCHEMES.keys())

def apply_theme(st, theme_name="default"):
    """Apply the selected theme to the Streamlit app."""
    css = get_custom_css(theme_name)
    st.markdown(css, unsafe_allow_html=True) 