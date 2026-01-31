# E2E Test Suite

End-to-end tests for the Biogas Sensor Data Management System using Playwright and pytest.

## 📦 Installation

### 1. Install test dependencies

```bash
pip install -r requirements-test.txt
```

### 2. Install Playwright browsers

```bash
playwright install chromium
```

## 🚀 Running Tests

### Run all tests

```bash
python3 -m pytest
# or use the test runner script
./run_tests.sh
```

### Run specific test files

```bash
# Smoke tests only
python3 -m pytest tests/e2e/test_smoke.py
# or
./run_tests.sh --smoke

# Engineer interface tests
python3 -m pytest tests/e2e/test_engineer.py
# or
./run_tests.sh --engineer

# Analyst interface tests
python3 -m pytest tests/e2e/test_analyst.py
# or
./run_tests.sh --analyst

# i18n tests
python3 -m pytest tests/e2e/test_i18n.py
# or
./run_tests.sh --i18n
```

### Run tests with specific markers

```bash
# Run only smoke tests
python3 -m pytest -m smoke

# Run everything except slow tests
python3 -m pytest -m "not slow"
```

### Run tests in parallel (faster)

```bash
python3 -m pytest -n auto
```

**Note**: Use `python3 -m pytest` instead of just `pytest` if pytest is not in your PATH.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (already exists) with:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

For CI/CD, you can also set:

```env
TEST_APP_URL=http://localhost:8501  # Default
```

If `TEST_APP_URL` is set to localhost, tests will automatically start the Streamlit app.
If set to a remote URL (e.g., staging environment), tests will use that instead.

## 📊 Test Structure

```
tests/
├── __init__.py
├── README.md              # This file
└── e2e/
    ├── __init__.py
    ├── conftest.py        # Pytest fixtures and configuration
    ├── test_smoke.py      # Basic smoke tests
    ├── test_engineer.py   # Engineer interface tests
    ├── test_analyst.py    # Analyst interface tests
    └── test_i18n.py       # Internationalization tests
```

## 🧪 Test Categories

### Smoke Tests (`test_smoke.py`)
- ✅ App loads
- ✅ Tabs present
- ✅ Language selector visible
- ✅ No Streamlit branding
- ✅ Mobile responsive

### Engineer Tests (`test_engineer.py`)
- ✅ Add record form validation
- ✅ Add record success
- ✅ Sensor dropdown populated
- ✅ Recent records section
- ✅ Mobile add record

### Analyst Tests (`test_analyst.py`)
- ✅ Switch to Analyst tab
- ✅ Charts display
- ✅ Sensor selection checkboxes
- ✅ Clear all button
- ✅ Date range filter
- ✅ Data table tab
- ✅ CSV export button
- ✅ Pagination controls

### i18n Tests (`test_i18n.py`)
- ✅ Default language (Ukrainian)
- ✅ Switch to English
- ✅ Switch to Polish
- ✅ Language persists across tabs
- ✅ All UI elements translated
- ✅ Mobile language selector

## 📝 Writing New Tests

Example test structure:

```python
from playwright.sync_api import Page, expect

class TestMyFeature:
    """Tests for my new feature."""

    def test_feature_works(self, page: Page):
        """Test that my feature works."""
        # Arrange: Navigate and setup
        page.goto("http://localhost:8501")

        # Act: Perform action
        button = page.locator("button:has-text('My Button')")
        button.click()

        # Assert: Verify result
        expect(page.locator("text=Success")).to_be_visible()
```

## 🐛 Debugging Tests

### Run tests with video recording

```bash
python3 -m pytest --video=on
```

### Run tests with screenshots on failure

```bash
python3 -m pytest --screenshot=only-on-failure
```

### Run tests with trace (full debugging)

```bash
python3 -m pytest --tracing=on
```

### Run single test with debugging

```bash
python3 -m pytest tests/e2e/test_smoke.py::TestSmoke::test_app_loads -v
# or
./run_tests.sh --debug
```

## 🔄 CI/CD Integration

See `.github/workflows/ci.yml` for GitHub Actions setup.

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main`

## 📊 Test Reports

Test results are saved to `test-results/` directory (gitignored).

Generate HTML report:

```bash
python3 -m pytest --html=test-results/report.html --self-contained-html
```

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear test names that describe what is being tested
3. **One Assertion per Test**: Keep tests focused
4. **Use Fixtures**: Reuse common setup code via conftest.py
5. **Wait for Elements**: Always wait for elements before interacting
6. **Clean Up**: Tests should clean up after themselves (handled by fixtures)

## ⚡ Performance Tips

1. **Headless Mode**: Faster for CI/CD
2. **Parallel Execution**: Use `-n auto` for pytest-xdist
3. **Selective Testing**: Use markers to run subsets of tests
4. **Reuse Browser Context**: Done automatically via fixtures

## 🔗 Resources

- [Playwright Docs](https://playwright.dev/python/)
- [pytest Docs](https://docs.pytest.org/)
- [Streamlit Testing](https://docs.streamlit.io/develop/api-reference/utilities/st.testing)
