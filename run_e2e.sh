#!/bin/bash
#
# Comprehensive E2E Test Runner with Coverage and Reporting
#
# This script:
# - Spins up Streamlit app automatically (via conftest.py)
# - Runs E2E tests with Playwright
# - Calculates code coverage
# - Generates HTML test report and coverage report
# - Displays summary of results
#
# Usage: ./run_e2e.sh [options]
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo ""
    echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="test-results"
HTML_REPORT="${RESULTS_DIR}/report_${TIMESTAMP}.html"
COVERAGE_HTML_DIR="${RESULTS_DIR}/coverage-html"
COVERAGE_XML="${RESULTS_DIR}/coverage.xml"
COVERAGE_REPORT="${RESULTS_DIR}/coverage.txt"

# Parse command line arguments
MODE="all"
HEADED="false"
SLOW_MO=0
PARALLEL=""
COVERAGE=true
HTML_REPORT_ENABLED=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --smoke)
            MODE="smoke"
            shift
            ;;
        --engineer)
            MODE="engineer"
            shift
            ;;
        --analyst)
            MODE="analyst"
            shift
            ;;
        --i18n)
            MODE="i18n"
            shift
            ;;
        --headed)
            HEADED="true"
            shift
            ;;
        --debug)
            HEADED="true"
            SLOW_MO=1000
            shift
            ;;
        --parallel)
            PARALLEL="-n auto"
            shift
            ;;
        --no-coverage)
            COVERAGE=false
            shift
            ;;
        --no-report)
            HTML_REPORT_ENABLED=false
            shift
            ;;
        --help)
            echo "Usage: ./run_e2e.sh [options]"
            echo ""
            echo "Options:"
            echo "  --smoke          Run only smoke tests"
            echo "  --engineer       Run only engineer interface tests"
            echo "  --analyst        Run only analyst interface tests"
            echo "  --i18n           Run only internationalization tests"
            echo "  --headed         Run tests in headed mode (visible browser)"
            echo "  --debug          Run tests in debug mode (slow motion + headed)"
            echo "  --parallel       Run tests in parallel"
            echo "  --no-coverage    Skip code coverage calculation"
            echo "  --no-report      Skip HTML report generation"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run_e2e.sh                    # Run all tests with coverage"
            echo "  ./run_e2e.sh --smoke            # Run only smoke tests"
            echo "  ./run_e2e.sh --headed           # Run with visible browser"
            echo "  ./run_e2e.sh --debug            # Run in debug mode"
            echo "  ./run_e2e.sh --parallel         # Run tests in parallel"
            echo "  ./run_e2e.sh --no-coverage      # Skip coverage"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Display header
print_header "E2E Test Suite with Coverage & Reporting"

# Step 1: Check environment
print_step "Step 1/6: Checking environment..."

if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_error "Please edit .env file with your Supabase credentials before running tests."
    exit 1
fi
print_success "Environment file found"

# Step 2: Install dependencies
print_step "Step 2/6: Checking dependencies..."

if ! python3 -c "import pytest" 2>/dev/null; then
    print_info "Installing test dependencies..."
    pip3 install -r requirements-test.txt
    print_success "Test dependencies installed"
else
    print_success "Test dependencies already installed"
fi

if ! python3 -c "import pytest_cov" 2>/dev/null && [ "$COVERAGE" = true ]; then
    print_info "Installing coverage dependencies..."
    pip3 install pytest-cov pytest-html
    print_success "Coverage dependencies installed"
fi

# Step 3: Install Playwright browsers
print_step "Step 3/6: Checking Playwright browsers..."

if [ ! -d "$HOME/.cache/ms-playwright" ] && [ ! -d "$HOME/Library/Caches/ms-playwright" ]; then
    print_info "Installing Playwright browsers..."
    playwright install chromium
    print_success "Playwright browsers installed"
else
    print_success "Playwright browsers already installed"
fi

# Step 4: Prepare test results directory
print_step "Step 4/6: Preparing test results directory..."

mkdir -p "$RESULTS_DIR"
print_success "Test results directory ready: $RESULTS_DIR"

# Step 5: Determine test suite
print_step "Step 5/6: Configuring test suite..."

case $MODE in
    smoke)
        TEST_PATH="tests/e2e/test_smoke.py"
        print_info "Running smoke tests..."
        ;;
    engineer)
        TEST_PATH="tests/e2e/test_engineer.py"
        print_info "Running engineer interface tests..."
        ;;
    analyst)
        TEST_PATH="tests/e2e/test_analyst.py"
        print_info "Running analyst interface tests..."
        ;;
    i18n)
        TEST_PATH="tests/e2e/test_i18n.py"
        print_info "Running internationalization tests..."
        ;;
    all)
        TEST_PATH="tests/e2e/"
        print_info "Running all E2E tests..."
        ;;
esac

# Step 6: Build and run pytest command
print_step "Step 6/6: Running tests..."
echo ""

# Build pytest command
PYTEST_CMD="python3 -m pytest $TEST_PATH"

# Add basic options
PYTEST_CMD="$PYTEST_CMD -v"

# Add headed mode if requested
if [ "$HEADED" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD --headed"
fi

# Add slow motion if debug mode
if [ $SLOW_MO -gt 0 ]; then
    PYTEST_CMD="$PYTEST_CMD --slowmo=$SLOW_MO"
fi

# Add parallel execution
if [ -n "$PARALLEL" ]; then
    PYTEST_CMD="$PYTEST_CMD $PARALLEL"
fi

# Add coverage
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=. --cov-report=term-missing"
    PYTEST_CMD="$PYTEST_CMD --cov-report=html:${COVERAGE_HTML_DIR}"
    PYTEST_CMD="$PYTEST_CMD --cov-report=xml:${COVERAGE_XML}"
fi

# Add HTML report
if [ "$HTML_REPORT_ENABLED" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --html=${HTML_REPORT} --self-contained-html"
fi

# Display command (for transparency)
print_info "Command: $PYTEST_CMD"
echo ""

# Run tests
if eval $PYTEST_CMD; then
    TEST_RESULT=0
else
    TEST_RESULT=1
fi

# Display results summary
echo ""
print_header "Test Results Summary"

if [ $TEST_RESULT -eq 0 ]; then
    print_success "All tests passed! 🎉"
else
    print_error "Some tests failed. Check details above."
fi

# Coverage summary
if [ "$COVERAGE" = true ]; then
    echo ""
    print_info "Coverage Report:"

    if [ -f "${COVERAGE_XML}" ]; then
        # Extract coverage percentage from XML
        COVERAGE_PCT=$(python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('${COVERAGE_XML}')
    root = tree.getroot()
    line_rate = float(root.attrib['line-rate']) * 100
    print(f'{line_rate:.2f}%')
except:
    print('N/A')
" 2>/dev/null || echo "N/A")

        echo -e "  ${CYAN}Total Coverage:${NC} ${BOLD}${COVERAGE_PCT}${NC}"
    fi

    if [ -d "${COVERAGE_HTML_DIR}" ]; then
        print_success "HTML Coverage Report: ${COVERAGE_HTML_DIR}/index.html"
    fi
fi

# HTML test report
if [ "$HTML_REPORT_ENABLED" = true ] && [ -f "${HTML_REPORT}" ]; then
    echo ""
    print_success "HTML Test Report: ${HTML_REPORT}"
fi

# Quick links
echo ""
print_header "Quick Access"
echo -e "  ${CYAN}Open Coverage Report:${NC}"
echo -e "    open ${COVERAGE_HTML_DIR}/index.html"
echo ""
if [ "$HTML_REPORT_ENABLED" = true ]; then
    echo -e "  ${CYAN}Open Test Report:${NC}"
    echo -e "    open ${HTML_REPORT}"
    echo ""
fi

# Final status
echo ""
if [ $TEST_RESULT -eq 0 ]; then
    print_header "✅ Test Suite Completed Successfully"
    exit 0
else
    print_header "❌ Test Suite Completed with Failures"
    exit 1
fi
