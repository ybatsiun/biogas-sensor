# 🔬 Biogas Sensor Data Management System

A robust sensor data collection and management system for PhD dissertation research on Biogas Optimization.

## 📋 Overview

This application provides a comprehensive interface for:
- **Engineers**: Manual sensor data entry and CRUD operations
- **Analysts**: Interactive data visualization and export capabilities

**Current Phase**: Step 0 (Infrastructure & Manual CRUD)

## ✨ Features

### Engineer Interface
- ✅ Create, edit, and delete sensors (name, unit, comment)
- ✅ Add sensor records with timestamp and value
- ✅ Edit existing records (sensor, time, value)
- ✅ Form validation (numbers only, no future dates)
- ✅ Real-time success/error feedback

### Analyst Interface
- ✅ Interactive multi-sensor line charts (Plotly)
- ✅ Configurable sensor selection (overlay multiple sensors)
- ✅ Date range filtering
- ✅ Zoom, pan, hover tooltips
- ✅ Data table view with pagination
- ✅ Sort by date (ascending/descending)
- ✅ CSV export (full dataset)

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.31.0
- **Database**: Supabase (PostgreSQL)
- **Visualization**: Plotly 5.18.0
- **Language**: Python 3.11+

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Supabase account (free tier)

### Local Setup

1. **Clone the repository** (when available):
   ```bash
   git clone <your-repo-url>
   cd biogas-sensor-app
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_publishable_key
   ```

5. **Run the application**:
   ```bash
   python3 -m streamlit run streamlit_app.py
   ```

6. **Open your browser**:
   The app will automatically open at `http://localhost:8501`

## 🗄️ Database Schema

### `sensors` Table
| Column  | Type   | Description                |
|---------|--------|----------------------------|
| id      | UUID   | Primary key (auto-generated) |
| name    | TEXT   | Sensor name (required)     |
| unit    | TEXT   | Measurement unit (optional) |
| comment | TEXT   | Description (optional)     |

### `sensor_records` Table
| Column       | Type        | Description                |
|--------------|-------------|----------------------------|
| id           | UUID        | Primary key (auto-generated) |
| sensor_id    | UUID        | Foreign key to sensors     |
| recorded_at  | TIMESTAMPTZ | Timestamp of recording     |
| value        | FLOAT8      | Measured value             |

**Indexes**:
- `idx_sensor_records_sensor_id` on `sensor_id`
- `idx_sensor_records_recorded_at` on `recorded_at`

## 🚀 Usage Guide

### Adding a New Sensor
1. Navigate to the **Engineer** tab
2. Expand "➕ Create New Sensor"
3. Fill in the sensor name (required), unit, and comment
4. Click "Create Sensor"

### Recording Sensor Data
1. Navigate to the **Engineer** tab
2. Expand "➕ Add New Record"
3. Select the sensor from the dropdown
4. Set the date and time (defaults to now)
5. Enter the measured value
6. Click "Add Record"

### Editing Records
1. Find the record in "Recent Records (Last 100)"
2. Click "✏️ Edit"
3. Modify the sensor, timestamp, or value
4. Click "💾 Save"

### Visualizing Data
1. Navigate to the **Analyst** tab
2. Click the **📈 Charts** sub-tab
3. Select sensors using checkboxes
4. Adjust the date range
5. Interact with the chart (zoom, pan, hover)

### Exporting Data
1. Navigate to the **Analyst** tab
2. Click the **📊 Data Table** sub-tab
3. Apply filters as needed
4. Click "📥 Download CSV"

## 📁 Project Structure

```
biogas-sensor-app/
├── .env                    # Environment variables (not in git)
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── streamlit_app.py        # Main application entry point
├── README.md               # This file
├── database/
│   ├── __init__.py
│   ├── client.py           # Supabase client wrapper
│   └── queries.py          # Database query functions
├── components/
│   ├── __init__.py
│   ├── engineer.py         # Engineer CRUD interface
│   └── analyst.py          # Analyst visualization interface
└── utils/
    ├── __init__.py
    └── validation.py       # Input validation utilities
```

## 🧪 Testing

### Manual Testing Checklist
See [MANUAL_TESTING_CHECKLIST.md](MANUAL_TESTING_CHECKLIST.md) for comprehensive testing instructions.

### Key Test Cases
- ✅ Create sensor with all fields
- ✅ Create sensor with only required fields
- ✅ Edit sensor name and unit
- ✅ Delete sensor (verify cascade delete of records)
- ✅ Add record with current timestamp
- ✅ Add record with past timestamp
- ✅ Reject future timestamps
- ✅ Reject non-numeric values
- ✅ Edit record (change sensor, time, value)
- ✅ Delete record
- ✅ View multiple sensors on chart
- ✅ Filter data by date range
- ✅ Export data to CSV
- ✅ Pagination in data table

## 🔒 Security

- **Environment Variables**: Secrets stored in `.env` (excluded from git)
- **Supabase**: Uses publishable key (not service role key)
- **No Authentication**: Step 0 focuses on functionality (authentication in future phases)

## 🐛 Troubleshooting

### "ModuleNotFoundError"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

### "Supabase connection failed"
- Verify `.env` file exists with correct credentials
- Check `SUPABASE_URL` and `SUPABASE_KEY`
- Ensure Supabase project is active

### "Cannot record future timestamps"
- This is expected behavior - timestamps cannot be in the future
- Use current or past date/time

### App is slow
- Check database indexes are created
- Limit data queries with date range filters
- Consider caching for large datasets

## 📚 Documentation

- [Implementation Plan](BIOGAS-SENSOR-PLAN_v1.md) - Detailed development plan
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Deploy to Streamlit Community Cloud
- [Project Instructions](CLAUDE.md) - Project context and principles

## 🚀 Deployment

See [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) for step-by-step instructions on deploying to Streamlit Community Cloud (free tier).

Quick steps:
1. Push code to GitHub
2. Sign in to Streamlit Community Cloud
3. Connect your repository
4. Configure secrets (Supabase credentials)
5. Deploy!

## 🔮 Future Enhancements

**Post-Step 0 Roadmap**:
- Authentication system (Supabase Auth)
- Audit logging for all changes
- Bulk CSV import
- Python gateway for IoT sensor integration
- Time-series modeling
- Explainable AI (XAI) for biogas optimization
- Mobile app (React Native + Supabase)
- Real-time data streaming
- Grafana dashboards
- Row Level Security (RLS)

## 📝 License

This project is part of a PhD dissertation. All rights reserved.

## 👤 Author

PhD Researcher - Biogas Optimization

---

**Version**: 1.0
**Last Updated**: 2026-01-31
**Status**: ✅ Production Ready (Step 0)
