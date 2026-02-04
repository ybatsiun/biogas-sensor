"""
Biogas Sensor App - Main Application
PhD Dissertation: Biogas Optimization

Streamlit application for sensor data collection and management.
"""

import streamlit as st
from components.engineer import render_engineer_interface
from components.analyst import render_analyst_interface
from utils.i18n import t, render_language_selector


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Biogas Sensor App",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)


# ============================================================================
# CUSTOM CSS FOR BETTER UI
# ============================================================================

st.markdown("""
<style>
    /* Force light mode - disable dark mode adaptation */
    :root {
        color-scheme: light only;
    }

    body, html, [data-testid="stAppViewContainer"] {
        color-scheme: light only;
        background-color: white !important;
        color: #262730 !important;
    }

    /* Hide Streamlit menu and deploy button */
    #MainMenu {visibility: hidden;}
    footer {display: none !important;}
    .stDeployButton {display: none;}

    /* Hide header toolbar but keep spinner */
    header[data-testid="stHeader"] > div:first-child {visibility: hidden;}

    /* Full screen overlay for spinner */
    .stSpinner > div {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
        z-index: 9999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        transform: none !important;
    }

    /* Center the actual spinner element */
    .stSpinner > div > div {
        position: relative !important;
    }

    /* Position toasts at top center */
    .stToast,
    [data-testid="stToast"],
    [data-testid="toastContainer"],
    .element-container:has(.stToast) {
        position: fixed !important;
        top: 20px !important;
        left: 50% !important;
        right: auto !important;
        bottom: auto !important;
        transform: translateX(-50%) !important;
        visibility: visible !important;
        display: block !important;
        z-index: 10000 !important;
    }

    /* Target Streamlit's toast notification system */
    div[class*="Toast"],
    div[class*="toast"],
    .st-emotion-cache-*[class*="toast"] {
        position: fixed !important;
        top: 20px !important;
        left: 50% !important;
        right: auto !important;
        transform: translateX(-50%) !important;
        z-index: 10000 !important;
    }

    /* Override Streamlit's default toast positioning */
    section[data-testid="stToastContainer"] {
        position: fixed !important;
        top: 20px !important;
        left: 50% !important;
        right: auto !important;
        bottom: auto !important;
        transform: translateX(-50%) !important;
        align-items: center !important;
    }

    /* Toast styling - flexible width and hide close button */
    [data-testid="stToast"] {
        min-width: 300px !important;
        max-width: 600px !important;
        width: auto !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    /* Hide the close (X) button on toasts */
    [data-testid="stToast"] button,
    [data-testid="stToast"] button[title="Close"],
    [data-testid="stToast"] button[aria-label="Close"],
    [data-testid="stToast"] [class*="close"],
    [data-testid="stToast"] [class*="Close"],
    section[data-testid="stToastContainer"] button {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Language selector dropdown fix - ensure it's fully visible */
    [data-baseweb="select"] {
        z-index: 10001 !important;
        cursor: pointer !important;
    }

    [data-baseweb="select"] > div {
        cursor: pointer !important;
    }

    /* Dropdown menu positioning - ensure it appears above everything */
    [data-baseweb="popover"] {
        z-index: 99999 !important;
        position: fixed !important;
    }

    [role="listbox"] {
        z-index: 99999 !important;
        position: fixed !important;
    }

    /* Ensure dropdown options are fully visible */
    [data-baseweb="menu"] {
        z-index: 99999 !important;
        max-height: 300px !important;
        overflow-y: auto !important;
    }

    /* Fix dropdown list positioning */
    ul[role="listbox"] {
        z-index: 99999 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        background: white !important;
        position: fixed !important;
        overflow-y: auto !important;
        max-height: 300px !important;
    }

    /* Pointer cursor for dropdown options */
    [role="option"] {
        cursor: pointer !important;
    }

    /* Ensure Deploy button doesn't overlap dropdown */
    header[data-testid="stHeader"] {
        z-index: 1000 !important;
    }

    /* Version text styling */
    .stCaption {
        color: #666 !important;
        font-size: 0.75rem !important;
    }

    /* Main header styling */
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        color: #262730 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 16px;
    }

    /* Button styling */
    .stButton button {
        border-radius: 5px;
        font-weight: 500;
    }

    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        padding: 10px;
        border-radius: 5px;
    }

    /* Container spacing - extra bottom padding for dropdown */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
    }

    /* Mobile optimization - reduce padding and margins */
    @media only screen and (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-bottom: 10rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        h2 {
            font-size: 1.3rem !important;
        }

        h3 {
            font-size: 1.1rem !important;
        }

        /* Reduce spacing between elements */
        .element-container {
            margin-bottom: 0.5rem;
        }

        /* Optimize form inputs for mobile */
        .stTextInput, .stSelectbox, .stDateInput, .stTimeInput {
            margin-bottom: 0.5rem;
        }

        /* Make date/time inputs more mobile-friendly - use native pickers */
        .stDateInput input[type="text"],
        .stTimeInput input[type="text"] {
            font-size: 16px !important;
            min-height: 44px !important;
            padding: 12px !important;
            cursor: pointer !important;
        }

        /* Force native date/time pickers on mobile - prevent keyboard */
        .stDateInput input,
        .stTimeInput input {
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
        }

        /* Improve date/time picker button size */
        .stDateInput button, .stTimeInput button {
            min-height: 44px !important;
            min-width: 44px !important;
        }

        /* Fix selectbox dropdown visibility in dark mode on mobile */
        .stSelectbox [data-baseweb="select"] {
            background-color: white !important;
        }

        .stSelectbox [role="option"] {
            background-color: white !important;
            color: #262730 !important;
        }

        .stSelectbox [role="option"]:hover {
            background-color: #f0f2f6 !important;
        }

        /* Make buttons full-width on mobile */
        .stButton button {
            width: 100%;
        }

        /* Reduce expander padding */
        .streamlit-expanderHeader {
            padding: 0.5rem;
        }

        /* Stack columns on mobile */
        .st-emotion-cache-1r4qj8v {
            flex-direction: column;
        }
    }

    /* Loading spinner centered */
    .stSpinner > div {
        text-align: center;
        display: block;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def get_app_version() -> str:
    """Get current app version from VERSION file."""
    try:
        import os
        version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
        with open(version_file, 'r') as f:
            return f.read().strip()
    except:
        return "v0.1.10"


def main():
    """Main application entry point."""

    # Language selector in top-right corner
    col1, col2 = st.columns([5, 1])
    with col1:
        # Title with version below
        st.title(f"🔬 {t('app.title')}")
        version = get_app_version()
        st.caption(version)
    with col2:
        render_language_selector()

    # Create main tabs
    tab1, tab2 = st.tabs([f"👷 {t('tabs.engineer')}", f"📊 {t('tabs.analyst')}"])

    with tab1:
        render_engineer_interface()

    with tab2:
        render_analyst_interface()


# ============================================================================
# ERROR HANDLING
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.exception(e)
