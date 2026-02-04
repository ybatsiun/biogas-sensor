"""
Analyst interface tests - Data table accessibility.

These tests verify that the Analyst interface loads and table sections are accessible.
"""

import pytest
from playwright.sync_api import Page, expect


class TestAnalystInterface:
    """Tests for Analyst interface data table accessibility."""

    def test_switch_to_analyst_tab(self, page: Page):
        """Test switching to Analyst tab."""
        # Click on Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик")
        analyst_tab.click()

        # Wait for tab to load
        page.wait_for_timeout(1000)

        # Check that Analyst interface title is visible
        analyst_title = page.locator("text=Інтерфейс аналітика")
        expect(analyst_title).to_be_visible()

    def test_data_table_tab_visible(self, page: Page):
        """Test that Data Table tab is visible."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик")
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Check that Data Table tab exists
        data_table_tab = page.locator("text=📊 Таблиця даних")
        expect(data_table_tab).to_be_visible()
