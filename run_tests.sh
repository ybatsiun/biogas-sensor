#!/bin/bash
#
# E2E Test Runner Script
# Usage: ./run_tests.sh [options]
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
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

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_error "Please edit .env file with your Supabase credentials before running tests."
    exit 1
fi

# Check if test dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    print_info "Installing test dependencies..."
    pip install -r requirements-test.txt
    print_success "Test dependencies installed"
fi

# Check if Playwright browsers are installed
if [ ! -d "$HOME/.cache/ms-playwright" ] && [ ! -d "$HOME/Library/Caches/ms-playwright" ]; then
    print_info "Installing Playwright browsers..."
    playwright install chromium
    print_success "Playwright browsers installed"
fi

# Parse command line arguments
MODE="all"
HEADED="false"
SLOW_MO=0

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
        --help)
            echo "Usage: ./run_tests.sh [options]"
            echo ""
            echo "Options:"
            echo "  --smoke      Run only smoke tests"
            echo "  --engineer   Run only engineer interface tests"
            echo "  --analyst    Run only analyst interface tests"
            echo "  --i18n       Run only internationalization tests"
            echo "  --headed     Run tests in headed mode (visible browser)"
            echo "  --debug      Run tests in debug mode (slow motion + headed)"
            echo "  --parallel   Run tests in parallel"
            echo "  --help       Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run_tests.sh                # Run all tests"
            echo "  ./run_tests.sh --smoke        # Run only smoke tests"
            echo "  ./run_tests.sh --headed       # Run with visible browser"
            echo "  ./run_tests.sh --debug        # Run in debug mode"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Determine which tests to run
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

# Build pytest command
PYTEST_CMD="pytest $TEST_PATH"
PYTEST_CMD="$PYTEST_CMD --headed=$HEADED"

if [ $SLOW_MO -gt 0 ]; then
    PYTEST_CMD="$PYTEST_CMD --slowmo=$SLOW_MO"
fi

if [ -n "$PARALLEL" ]; then
    PYTEST_CMD="$PYTEST_CMD $PARALLEL"
fi

PYTEST_CMD="$PYTEST_CMD -v"

# Run tests
print_info "Command: $PYTEST_CMD"
echo ""

if eval $PYTEST_CMD; then
    echo ""
    print_success "All tests passed! 🎉"
    exit 0
else
    echo ""
    print_error "Some tests failed. Check output above for details."
    exit 1
fi
