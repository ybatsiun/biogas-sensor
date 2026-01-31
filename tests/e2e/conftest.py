"""
Pytest configuration and fixtures for E2E tests.
"""

import os
import subprocess
import time
from typing import Generator
import pytest
from playwright.sync_api import Page, Browser, BrowserContext, expect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
APP_URL = os.getenv("TEST_APP_URL", "http://localhost:8501")
STREAMLIT_PORT = 8501
STARTUP_TIMEOUT = 15  # seconds


@pytest.fixture(scope="session")
def streamlit_app():
    """
    Start Streamlit app for testing session.

    Only starts if APP_URL is localhost, otherwise assumes app is already running.
    """
    if "localhost" in APP_URL or "127.0.0.1" in APP_URL:
        print(f"\n🚀 Starting Streamlit app on port {STREAMLIT_PORT}...")

        # Start Streamlit in background
        process = subprocess.Popen(
            [
                "python3", "-m", "streamlit", "run",
                "streamlit_app.py",
                f"--server.port={STREAMLIT_PORT}",
                "--server.headless=true",
                "--server.runOnSave=false",
                "--browser.gatherUsageStats=false",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )

        # Wait for app to be ready
        print(f"⏳ Waiting for app to start at {APP_URL}...")
        time.sleep(STARTUP_TIMEOUT)

        print(f"✅ Streamlit app is running at {APP_URL}")

        yield process

        # Cleanup
        print("\n🛑 Stopping Streamlit app...")
        process.terminate()
        process.wait(timeout=5)
        print("✅ Streamlit app stopped")
    else:
        print(f"\n✅ Using existing app at {APP_URL}")
        yield None


@pytest.fixture(scope="function")
def page(streamlit_app, browser: Browser) -> Generator[Page, None, None]:
    """
    Create a new browser page for each test.

    This ensures test isolation - each test starts with a fresh page.
    """
    context: BrowserContext = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US",
    )

    page = context.new_page()

    # Navigate to app
    page.goto(APP_URL, wait_until="networkidle", timeout=30000)

    # Wait for Streamlit to be fully loaded
    page.wait_for_selector("text=Інженер", timeout=30000)

    yield page

    # Cleanup
    context.close()


@pytest.fixture(scope="function")
def mobile_page(streamlit_app, browser: Browser) -> Generator[Page, None, None]:
    """
    Create a mobile viewport page for testing responsive design.
    """
    context: BrowserContext = browser.new_context(
        viewport={"width": 375, "height": 667},  # iPhone SE
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
        is_mobile=True,
        has_touch=True,
    )

    page = context.new_page()
    page.goto(APP_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_selector("text=Інженер", timeout=30000)

    yield page

    context.close()


def wait_for_streamlit_rerun(page: Page, timeout: int = 5000):
    """
    Wait for Streamlit to complete a rerun after an action.

    Streamlit shows a spinner during reruns, so we wait for it to appear and disappear.
    """
    try:
        # Wait for spinner to appear (if it does)
        page.wait_for_selector("[data-testid='stSpinner'], text='RUNNING'", timeout=1000)
        # Wait for spinner to disappear
        page.wait_for_selector("[data-testid='stSpinner'], text='RUNNING'", state="hidden", timeout=timeout)
    except:
        # Spinner might not appear for fast operations
        # Wait a short time for the rerun to complete
        time.sleep(0.5)


# Playwright auto-fixtures
# These are provided by pytest-playwright plugin:
# - browser: Browser instance
# - browser_context: BrowserContext instance
# - page: Page instance (we override this above for custom setup)
