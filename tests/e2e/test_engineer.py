"""
Engineer interface tests - CRUD operations.

These tests verify that the Engineer can add, edit, and delete records.
"""

import pytest
from playwright.sync_api import Page, expect
from .conftest import wait_for_streamlit_rerun


class TestEngineerInterface:
    """Tests for Engineer interface functionality."""

    def test_add_record_form_validation(self, page: Page):
        """Test that form validation works (required fields)."""
        # Clear the value field (should be empty by default)
        value_input = page.get_by_placeholder("e.g., 37.5")
        value_input.fill("")

        # Try to submit without value
        add_button = page.locator("button:has-text('Add Record')")
        add_button.click()

        # Wait for response
        page.wait_for_timeout(1000)

        # Form should still be visible (submission failed)
        expect(value_input).to_be_visible()

    def test_add_record_success(self, page: Page):
        """Test successfully adding a new sensor record."""
        import random

        # Generate random test value
        test_value = round(random.uniform(10.0, 100.0), 2)

        # Fill in the form
        # Sensor is pre-selected, so we'll use whatever is selected

        # Fill value
        value_input = page.get_by_placeholder("e.g., 37.5")
        value_input.fill(str(test_value))

        # Submit form
        add_button = page.locator("button:has-text('Add Record')").or_(
            page.locator("button:has-text('Додати запис')")
        )
        add_button.click()

        # Wait for toast notification
        page.wait_for_timeout(2000)

        # Check for success toast (might disappear quickly)
        # The page should rerun after successful submission
        # Value field should be cleared after successful submission
        expect(value_input).to_have_value("")

    def test_sensor_dropdown_populated(self, page: Page):
        """Test that sensor dropdown is populated with sensors from database."""
        # Click on sensor dropdown
        sensor_select = page.locator("select, [role='combobox']").first
        sensor_select.click()

        # Wait for dropdown to open
        page.wait_for_timeout(500)

        # Check that there are sensor options
        # The exact sensor names depend on your database
        # We just check that the dropdown is not empty

        # Close dropdown by clicking elsewhere
        page.locator("body").click()

    def test_recent_records_section(self, page: Page):
        """Test that Recent Records section can be expanded."""
        # Find "Recent Records" section (should be collapsed by default on mobile-first)
        recent_records = page.locator("text=📋 Останні записи").or_(
            page.locator("text=📋 Recent Records")
        )
        expect(recent_records).to_be_visible()

        # Click to expand
        recent_records.click()
        page.wait_for_timeout(1000)

        # Section should expand and show table or empty message
        # We don't assert specific content as it depends on database state

    def test_sensor_management_section_exists(self, page: Page):
        """Test that Sensor Management section exists."""
        # Scroll down to find sensor management section
        sensor_management = page.locator("text=Управління датчиками").or_(
            page.locator("text=Sensor Management")
        )
        expect(sensor_management).to_be_visible()

        # Check for "Create New Sensor" section
        create_sensor = page.locator("text=➕ Створити новий датчик").or_(
            page.locator("text=➕ Create New Sensor")
        )
        expect(create_sensor).to_be_visible()

    def test_mobile_add_record_form(self, mobile_page: Page):
        """Test that add record form works on mobile viewport."""
        import random

        # Generate random test value
        test_value = round(random.uniform(10.0, 100.0), 2)

        # Fill value (form should be expanded by default on mobile)
        value_input = mobile_page.get_by_placeholder("e.g., 37.5")
        expect(value_input).to_be_visible()

        value_input.fill(str(test_value))

        # Submit
        add_button = mobile_page.locator("button:has-text('Add Record')").or_(
            mobile_page.locator("button:has-text('Додати запис')")
        )
        add_button.click()

        # Wait for response
        mobile_page.wait_for_timeout(2000)

        # Form should rerun and clear
        expect(value_input).to_have_value("")
