#!/bin/bash
# Quick start script for Biogas Sensor App

echo "🔬 Starting Biogas Sensor App..."
echo ""

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found"
    echo "Please run this script from the biogas-sensor-app directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create .env file with your Supabase credentials"
    exit 1
fi

# Start the app
echo "✅ Starting Streamlit..."
echo "📱 Browser will open automatically at http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the app"
echo ""

python3 -m streamlit run streamlit_app.py
