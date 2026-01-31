"""
UI helper utilities for loading spinners and mobile detection.
"""

import streamlit as st
from contextlib import contextmanager
from utils.i18n import t


def is_mobile() -> bool:
    """
    Detect if the user is on a mobile device.

    Returns:
        True if mobile device, False otherwise
    """
    # Streamlit doesn't have direct mobile detection, but we can use viewport width
    # This is a heuristic approach - consider viewport width < 768px as mobile
    return st.session_state.get('is_mobile', False)


@contextmanager
def loading_spinner(message: str = None):
    """
    Context manager for showing centered loading spinner with overlay.

    Args:
        message: Loading message to display (default: translated "Loading")

    Usage:
        with loading_spinner("Creating sensor..."):
            # Your code here
            queries.create_sensor(...)
    """
    if message is None:
        message = t('common.loading')

    # Use Streamlit's built-in spinner
    with st.spinner(f"⏳ {message}..."):
        yield


def show_mobile_hint():
    """Show a hint about mobile optimizations."""
    if is_mobile():
        st.info("📱 Mobile view optimized. Sections are collapsible to reduce scrolling.")


def render_collapsible_section(title: str, content_func, expanded: bool = False, count: int = None):
    """
    Render a collapsible section with optional item count.

    Args:
        title: Section title
        content_func: Function to render content inside the expander
        expanded: Whether section is expanded by default
        count: Optional count to show in title (e.g., "Recent Records (10)")
    """
    # Add count to title if provided
    display_title = f"{title} ({count})" if count else title

    with st.expander(display_title, expanded=expanded):
        content_func()


def get_mobile_record_limit() -> int:
    """
    Get the number of records to show on mobile.

    Returns:
        10 for mobile, 100 for desktop
    """
    return 10 if is_mobile() else 100
