"""
Internationalization (i18n) utilities for multi-language support.
"""

import json
import os
import streamlit as st
from typing import Dict, Any


# Available languages
LANGUAGES = {
    "uk": {"name": "Українська", "flag": "🇺🇦"},
    "en": {"name": "English", "flag": "🇬🇧"},
    "pl": {"name": "Polski", "flag": "🇵🇱"}
}

DEFAULT_LANGUAGE = "uk"

_translations_cache: Dict[str, Dict[str, Any]] = {}


def load_translation(lang_code: str) -> Dict[str, Any]:
    """
    Load translation file for specified language.

    Args:
        lang_code: Language code (uk, en, pl)

    Returns:
        Dictionary with translations
    """
    if lang_code in _translations_cache:
        return _translations_cache[lang_code]

    translations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations")
    file_path = os.path.join(translations_dir, f"{lang_code}.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translations_cache[lang_code] = translations
            return translations
    except FileNotFoundError:
        # Fallback to English if translation not found
        if lang_code != "en":
            return load_translation("en")
        raise


def get_current_language() -> str:
    """
    Get current language from session state.

    Returns:
        Current language code
    """
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    return st.session_state.language


def set_language(lang_code: str):
    """
    Set current language in session state.

    Args:
        lang_code: Language code to set
    """
    if lang_code in LANGUAGES:
        st.session_state.language = lang_code


def t(key: str, **kwargs) -> str:
    """
    Translate a key to the current language.

    Args:
        key: Translation key in dot notation (e.g., "app.title", "engineer.sensor_name")
        **kwargs: Variables to interpolate in the translation string

    Returns:
        Translated string

    Example:
        >>> t("app.title")
        "Biogas Sensor Data Management System"
        >>> t("engineer.success_sensor_created", name="Temperature")
        "Sensor 'Temperature' created successfully!"
    """
    lang_code = get_current_language()
    translations = load_translation(lang_code)

    # Navigate through nested dictionary using dot notation
    keys = key.split('.')
    value = translations

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # Key not found, return the key itself as fallback
            return f"[{key}]"

    # Interpolate variables if any
    if kwargs and isinstance(value, str):
        try:
            return value.format(**kwargs)
        except KeyError:
            return value

    return value


def render_language_selector():
    """
    Render language selector in the UI.
    Returns the selected language code.
    """
    current_lang = get_current_language()

    # Create language options
    lang_options = list(LANGUAGES.keys())
    lang_labels = [f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}" for code in lang_options]

    # Find current index
    current_index = lang_options.index(current_lang) if current_lang in lang_options else 0

    # Render radio buttons (prevents typing arbitrary text)
    selected_label = st.radio(
        label="Language / Мова / Język",
        options=lang_labels,
        index=current_index,
        key="language_selector",
        label_visibility="collapsed",
        horizontal=True
    )

    # Get selected language code
    selected_index = lang_labels.index(selected_label)
    selected_lang = lang_options[selected_index]

    # Update if changed
    if selected_lang != current_lang:
        set_language(selected_lang)
        st.rerun()

    return selected_lang
