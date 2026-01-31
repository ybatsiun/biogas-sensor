"""
Internationalization (i18n) tests - Multi-language support.

These tests verify that language switching works correctly.
"""

import pytest
from playwright.sync_api import Page, expect


class TestInternationalization:
    """Tests for multi-language support."""

    def test_default_language_is_ukrainian(self, page: Page):
        """Test that Ukrainian is the default language."""
        # Check that Ukrainian flag/text is visible
        language_selector = page.locator("text=🇺🇦 Українська")
        expect(language_selector).to_be_visible()

        # Check that interface text is in Ukrainian
        engineer_tab = page.locator("text=👷 Інженер")
        expect(engineer_tab).to_be_visible()

    def test_switch_to_english(self, page: Page):
        """Test switching to English language."""
        # Click on language selector
        language_selector = page.locator("text=🇺🇦 Українська")
        language_selector.click()
        page.wait_for_timeout(500)

        # Select English
        english_option = page.locator("text=🇬🇧 English")
        english_option.click()

        # Wait for page to reload
        page.wait_for_timeout(2000)

        # Check that language changed to English
        expect(page.locator("text=🇬🇧 English")).to_be_visible()

        # Check that interface text is now in English
        engineer_tab = page.locator("text=👷 Engineer")
        expect(engineer_tab).to_be_visible()

        # Check that title changed
        title = page.locator("text=Biogas Sensor Data Management System")
        expect(title).to_be_visible()

    def test_switch_to_polish(self, page: Page):
        """Test switching to Polish language."""
        # Click on language selector
        language_selector = page.locator("text=🇺🇦 Українська")
        language_selector.click()
        page.wait_for_timeout(500)

        # Select Polish
        polish_option = page.locator("text=🇵🇱 Polski")
        polish_option.click()

        # Wait for page to reload
        page.wait_for_timeout(2000)

        # Check that language changed to Polish
        expect(page.locator("text=🇵🇱 Polski")).to_be_visible()

        # Check that interface text is now in Polish
        engineer_tab = page.locator("text=👷 Inżynier")
        expect(engineer_tab).to_be_visible()

    def test_language_persists_across_tabs(self, page: Page):
        """Test that language selection persists when switching tabs."""
        # Switch to English
        language_selector = page.locator("text=🇺🇦 Українська")
        language_selector.click()
        page.wait_for_timeout(500)

        english_option = page.locator("text=🇬🇧 English")
        english_option.click()
        page.wait_for_timeout(2000)

        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Analyst")
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Check that language is still English
        expect(page.locator("text=🇬🇧 English")).to_be_visible()

        # Check that Analyst interface is in English
        analyst_title = page.locator("text=Analyst Interface")
        expect(analyst_title).to_be_visible()

        # Switch back to Engineer tab
        engineer_tab = page.locator("text=👷 Engineer")
        engineer_tab.click()
        page.wait_for_timeout(1000)

        # Language should still be English
        expect(page.locator("text=🇬🇧 English")).to_be_visible()

    def test_all_ui_elements_translated_english(self, page: Page):
        """Test that all major UI elements are translated in English."""
        # Switch to English
        language_selector = page.locator("text=🇺🇦 Українська")
        language_selector.click()
        page.wait_for_timeout(500)

        english_option = page.locator("text=🇬🇧 English")
        english_option.click()
        page.wait_for_timeout(2000)

        # Check Engineer interface elements
        expect(page.locator("text=Engineer Interface")).to_be_visible()
        expect(page.locator("text=Record Management")).to_be_visible()
        expect(page.locator("text=Add New Record")).to_be_visible()
        expect(page.locator("text=Sensor Management")).to_be_visible()

        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Analyst")
        analyst_tab.click()
        page.wait_for_timeout(2000)

        # Check Analyst interface elements
        expect(page.locator("text=Analyst Interface")).to_be_visible()
        expect(page.locator("text=Charts")).to_be_visible()
        expect(page.locator("text=Data Table")).to_be_visible()

    def test_mobile_language_selector(self, mobile_page: Page):
        """Test that language selector works on mobile."""
        # Check that language selector is visible on mobile
        language_selector = mobile_page.locator("text=🇺🇦 Українська")
        expect(language_selector).to_be_visible()

        # Click to open dropdown
        language_selector.click()
        mobile_page.wait_for_timeout(500)

        # Check that language options are visible
        english_option = mobile_page.locator("text=🇬🇧 English")
        expect(english_option).to_be_visible()

        # Select English
        english_option.click()
        mobile_page.wait_for_timeout(2000)

        # Verify language changed
        expect(mobile_page.locator("text=🇬🇧 English")).to_be_visible()
