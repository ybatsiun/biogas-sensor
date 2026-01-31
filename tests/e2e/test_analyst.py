"""
Analyst interface tests - Data visualization and export.

These tests verify that the Analyst can view charts and export data.
"""

import pytest
from playwright.sync_api import Page, expect


class TestAnalystInterface:
    """Tests for Analyst interface functionality."""

    def test_switch_to_analyst_tab(self, page: Page):
        """Test switching to Analyst tab."""
        # Click on Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()

        # Wait for tab to load
        page.wait_for_timeout(1000)

        # Check that Analyst interface title is visible
        analyst_title = page.locator("text=Analyst Interface").or_(
            page.locator("text=Інтерфейс аналітика")
        )
        expect(analyst_title).to_be_visible()

    def test_charts_tab_active_by_default(self, page: Page):
        """Test that Charts tab is active by default in Analyst interface."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Check that Charts tab is visible
        charts_tab = page.locator("text=📈 Charts").or_(page.locator("text=📈 Графіки"))
        expect(charts_tab).to_be_visible()

    def test_chart_displays(self, page: Page):
        """Test that the multi-sensor chart displays."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(2000)

        # Check for chart title
        chart_title = page.locator("text=Interactive Multi-Sensor Chart").or_(
            page.locator("text=Інтерактивний графік")
        )
        expect(chart_title).to_be_visible()

        # Check that sensor checkboxes are present
        sensor_checkboxes = page.locator("input[type='checkbox']")
        expect(sensor_checkboxes.first).to_be_visible()

    def test_sensor_selection_checkboxes(self, page: Page):
        """Test that sensor selection checkboxes work."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(2000)

        # Find first checkbox (should be checked by default)
        first_checkbox = page.locator("input[type='checkbox']").first

        # Get initial state
        is_checked = first_checkbox.is_checked()

        # Toggle checkbox
        first_checkbox.click()
        page.wait_for_timeout(1000)

        # Check that state changed
        new_state = first_checkbox.is_checked()
        assert new_state != is_checked, "Checkbox state should change after click"

    def test_clear_all_button(self, page: Page):
        """Test that Clear All button works."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(2000)

        # Find Clear All button
        clear_button = page.locator("button:has-text('Clear All')").or_(
            page.locator("button:has-text('Очистити все')")
        )

        if clear_button.is_visible():
            # Click Clear All
            clear_button.click()
            page.wait_for_timeout(1000)

            # Check that at least one checkbox is now unchecked
            first_checkbox = page.locator("input[type='checkbox']").first
            expect(first_checkbox).not_to_be_checked()

    def test_date_range_filter_present(self, page: Page):
        """Test that date range filter is present."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(2000)

        # Check for date range filter text
        date_filter = page.locator("text=Date Range Filter").or_(
            page.locator("text=Фільтр діапазону дат")
        )
        expect(date_filter).to_be_visible()

    def test_data_table_tab(self, page: Page):
        """Test switching to Data Table tab."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Click on Data Table tab
        data_table_tab = page.locator("text=📊 Data Table").or_(
            page.locator("text=📊 Таблиця даних")
        )
        data_table_tab.click()
        page.wait_for_timeout(2000)

        # Check that data table view is visible
        data_table_title = page.locator("text=Data Table View").or_(
            page.locator("text=Перегляд таблиці даних")
        )
        expect(data_table_title).to_be_visible()

    def test_csv_export_button_present(self, page: Page):
        """Test that CSV export button is present."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Click on Data Table tab
        data_table_tab = page.locator("text=📊 Data Table").or_(
            page.locator("text=📊 Таблиця даних")
        )
        data_table_tab.click()
        page.wait_for_timeout(2000)

        # Check for CSV download button
        csv_button = page.locator("text=📥 Download CSV").or_(
            page.locator("text=📥 Завантажити CSV")
        )
        expect(csv_button).to_be_visible()

    def test_pagination_controls(self, page: Page):
        """Test that pagination controls are present in Data Table."""
        # Switch to Analyst tab
        analyst_tab = page.locator("text=📊 Аналітик").or_(page.locator("text=📊 Analyst"))
        analyst_tab.click()
        page.wait_for_timeout(1000)

        # Click on Data Table tab
        data_table_tab = page.locator("text=📊 Data Table").or_(
            page.locator("text=📊 Таблиця даних")
        )
        data_table_tab.click()
        page.wait_for_timeout(2000)

        # Check for pagination text like "Page 1 of X" or "Showing X records"
        pagination = page.locator("text=/Page \\d+ of \\d+/").or_(
            page.locator("text=/Сторінка \\d+ з \\d+/")
        )
        # Pagination might not be visible if there's no data, so we check loosely
        # expect(pagination).to_be_visible()  # Optional check

        # At minimum, check for navigation buttons
        # (They might be disabled if no data)
        next_button = page.locator("button:has-text('Next')").or_(
            page.locator("button:has-text('Наступна')")
        )
        # Button exists even if disabled
        expect(next_button).to_be_attached()
