"""
Smoke tests - Basic functionality checks.

These tests verify that the app loads and core components are present.
"""

import pytest
from playwright.sync_api import Page, expect


class TestSmoke:
    """Smoke tests for basic app functionality."""

    def test_app_loads(self, page: Page):
        """Test that the app loads successfully."""
        # Check that the title is present
        expect(page.locator("text=Система управління даними датчиків біогазу")).to_be_visible()

    def test_tabs_present(self, page: Page):
        """Test that both Engineer and Analyst tabs are present."""
        # Check Engineer tab
        engineer_tab = page.locator("text=👷 Інженер")
        expect(engineer_tab).to_be_visible()

        # Check Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик")
        expect(analyst_tab).to_be_visible()

    def test_language_selector_present(self, page: Page):
        """Test that language selector is present."""
        # Check for Ukrainian flag/text
        language_selector = page.locator("text=🇺🇦 Українська")
        expect(language_selector).to_be_visible()

    def test_no_streamlit_branding(self, page: Page):
        """Test that Streamlit branding is hidden."""
        # Check that the hamburger menu is not visible
        # (It might exist in DOM but should be hidden with CSS)

        # Check that no "Made with Streamlit" text is visible
        streamlit_text = page.locator("text=Made with Streamlit")
        expect(streamlit_text).not_to_be_visible()

    def test_engineer_interface_loads(self, page: Page):
        """Test that Engineer interface loads with key sections."""
        # Check that "Add New Record" section is present and expanded
        add_record_section = page.locator("text=➕ Додати новий запис")
        expect(add_record_section).to_be_visible()

        # Check that form fields are present
        sensor_field = page.locator("text=Sensor*")
        expect(sensor_field).to_be_visible()

        date_field = page.locator("text=Date*")
        expect(date_field).to_be_visible()

        value_field = page.locator("text=Value*")
        expect(value_field).to_be_visible()

    def test_analyst_interface_loads(self, page: Page):
        """Test that Analyst interface loads with charts tab."""
        # Click on Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик")
        analyst_tab.click()

        # Wait for page to load
        page.wait_for_timeout(1000)

        # Check that Charts tab is present
        charts_tab = page.locator("text=📈 Charts").or_(page.locator("text=📈 Графіки"))
        expect(charts_tab).to_be_visible()

        # Check that chart title is present
        chart_title = page.locator("text=Interactive Multi-Sensor Chart").or_(
            page.locator("text=Інтерактивний графік")
        )
        expect(chart_title).to_be_visible()

    def test_mobile_responsive(self, mobile_page: Page):
        """Test that app is responsive on mobile viewport."""
        # Check that title is visible (might wrap on mobile)
        title = mobile_page.locator("text=Система управління даними датчиків біогазу")
        expect(title).to_be_visible()

        # Check that tabs are visible
        engineer_tab = mobile_page.locator("text=👷 Інженер")
        expect(engineer_tab).to_be_visible()

        # Check that language selector is visible
        language_selector = mobile_page.locator("text=🇺🇦 Українська")
        expect(language_selector).to_be_visible()
