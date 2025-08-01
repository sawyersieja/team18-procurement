# 🎨 Website Interface Color Customization Guide

This guide shows you how to customize the colors and styling of your Vendor Evaluation Tool website interface.

## 🚀 **Quick Start - Using the Built-in Theme System**

The easiest way to customize colors is using the theme system I've added:

### 1. **Choose from Pre-built Themes**

- **Default**: Blue and gray theme
- **Corporate**: Professional blue theme
- **Modern**: Indigo and gray theme
- **Dark**: Dark mode theme

### 2. **How to Change Themes**

1. Run the application: `streamlit run main.py`
2. Look at the sidebar under "🎨 Theme"
3. Select your preferred theme from the dropdown
4. The interface will update immediately!

## 🎨 **Method 1: Using the Theme Configuration File**

### **Easy Theme Customization**

Edit `theme_config.py` to change colors:

```python
# In theme_config.py, modify the COLOR_SCHEMES
COLOR_SCHEMES = {
    "my_custom_theme": {
        "primary": "#ff6b6b",      # Change this to your preferred color
        "secondary": "#4ecdc4",    # Secondary color
        "background": "#f7f7f7",   # Background color
        "sidebar_bg": "#2c3e50",   # Sidebar background
        "sidebar_text": "#ecf0f1", # Sidebar text color
        # ... add more colors
    }
}
```

### **Adding Your Own Theme**

1. Open `theme_config.py`
2. Add a new theme to `COLOR_SCHEMES`
3. Use hex color codes (like `#ff6b6b`)
4. Restart the application

## 🎨 **Method 2: Manual CSS Customization**

### **Quick Color Changes**

Add this to your `main.py` after `st.set_page_config()`:

```python
st.markdown("""
<style>
/* Change sidebar to purple */
.css-1d391kg {
    background-color: #6a4c93 !important;
}

/* Change buttons to green */
.stButton > button {
    background-color: #28a745 !important;
}

/* Change main background */
.main {
    background-color: #f8f9fa !important;
}
</style>
""", unsafe_allow_html=True)
```

### **Common CSS Selectors to Customize**

| Element            | CSS Selector                | What it changes      |
| ------------------ | --------------------------- | -------------------- |
| Sidebar background | `.css-1d391kg`              | Sidebar color        |
| Sidebar text       | `.css-1d391kg .css-1v0mbdj` | Sidebar text color   |
| Main background    | `.main`                     | Main page background |
| Buttons            | `.stButton > button`        | Button colors        |
| Headers            | `h1, h2, h3`                | Title colors         |
| Text               | `.stMarkdown`               | Regular text color   |
| File uploader      | `.stFileUploader`           | Upload area styling  |
| Dataframes         | `.dataframe`                | Table styling        |

## 🎨 **Method 3: Advanced Customization**

### **Gradient Backgrounds**

```python
st.markdown("""
<style>
.css-1d391kg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}
</style>
""", unsafe_allow_html=True)
```

### **Glass Effect**

```python
st.markdown("""
<style>
.stMarkdown {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)
```

### **Custom Fonts**

```python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
* {
    font-family: 'Roboto', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)
```

## 🎨 **Method 4: Using Streamlit's Built-in Options**

### **Page Configuration Options**

```python
st.set_page_config(
    page_title="Your App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': '# Your App\nBuilt with Streamlit'
    }
)
```

## 🎨 **Color Palette Examples**

### **Professional Blue Theme**

```python
colors = {
    "primary": "#1f4e79",      # Corporate blue
    "secondary": "#2c3e50",    # Dark blue
    "background": "#ffffff",    # White
    "sidebar_bg": "#1f4e79",   # Corporate blue
    "sidebar_text": "#ffffff",  # White
}
```

### **Modern Purple Theme**

```python
colors = {
    "primary": "#6a4c93",      # Purple
    "secondary": "#4a4a4a",    # Dark gray
    "background": "#f8f5ff",   # Light purple
    "sidebar_bg": "#6a4c93",   # Purple
    "sidebar_text": "#ffffff",  # White
}
```

### **Warm Orange Theme**

```python
colors = {
    "primary": "#ff6b6b",      # Coral red
    "secondary": "#4ecdc4",    # Turquoise
    "background": "#fff5f5",   # Light pink
    "sidebar_bg": "#ff6b6b",   # Coral red
    "sidebar_text": "#ffffff",  # White
}
```

## 🎨 **Testing Your Changes**

### **Run the Example**

```bash
streamlit run custom_theme_example.py
```

This will show you different theme examples and how to apply them.

### **Test Your Main App**

```bash
streamlit run main.py
```

## 🎨 **Tips for Good Design**

### **Color Contrast**

- Ensure text is readable against backgrounds
- Use tools like [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### **Accessibility**

- Don't rely solely on color to convey information
- Use sufficient contrast ratios
- Consider colorblind users

### **Consistency**

- Use a consistent color palette throughout
- Limit to 3-4 main colors
- Use variations of the same color for different elements

## 🎨 **Troubleshooting**

### **CSS Not Working?**

1. Make sure you're using `!important` for CSS rules
2. Check that the CSS selector is correct
3. Clear your browser cache
4. Restart the Streamlit app

### **Colors Not Updating?**

1. Make sure the CSS is applied after `st.set_page_config()`
2. Check that the hex color codes are valid
3. Try refreshing the browser page

### **Finding the Right CSS Selector**

1. Right-click on the element you want to style
2. Select "Inspect Element"
3. Look at the CSS classes in the developer tools
4. Use those class names in your CSS

## 🎨 **Advanced: Creating Your Own Theme System**

If you want to create a more sophisticated theme system:

1. **Create a theme class**:

```python
class Theme:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

    def apply(self, st):
        css = self.generate_css()
        st.markdown(css, unsafe_allow_html=True)
```

2. **Store themes in a database or config file**
3. **Add theme switching functionality**
4. **Save user preferences**

## 🎨 **Resources**

- [Streamlit Documentation](https://docs.streamlit.io/)
- [CSS Color Picker](https://www.w3schools.com/colors/colors_picker.asp)
- [Material Design Colors](https://material.io/design/color/)
- [Coolors Color Palette Generator](https://coolors.co/)

## 🎨 **Quick Reference**

### **Common Color Codes**

- Blue: `#3498db`
- Green: `#27ae60`
- Red: `#e74c3c`
- Orange: `#f39c12`
- Purple: `#9b59b6`
- Gray: `#95a5a6`
- Dark Blue: `#2c3e50`
- White: `#ffffff`
- Black: `#000000`

### **CSS Properties**

- `background-color`: Sets background color
- `color`: Sets text color
- `border-radius`: Rounds corners
- `padding`: Adds internal spacing
- `margin`: Adds external spacing
- `font-weight`: Makes text bold/normal
- `border`: Adds borders

Happy styling! 🎨✨
