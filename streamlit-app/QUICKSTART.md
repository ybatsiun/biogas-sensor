# Quick Start Guide

## Start the Application Locally

### 1. Install Dependencies (One-time setup)
```bash
cd /Users/yevhen/biogas-sensor-app
pip3 install -r requirements.txt
```

### 2. Run the Application
```bash
python3 -m streamlit run streamlit_app.py
```

### 3. Access the App
- Your browser will automatically open at: `http://localhost:8501`
- If not, manually navigate to that URL

### 4. Test the Application
- Follow the comprehensive testing guide in `MANUAL_TESTING_CHECKLIST.md`
- Estimated testing time: 10-15 minutes

---

## Troubleshooting

### "Command not found: streamlit"
The streamlit command may not be in your PATH. Try:
```bash
python3 -m streamlit run streamlit_app.py
```

### "Supabase connection failed"
Verify your `.env` file exists with correct credentials:
```
SUPABASE_URL=https://uzgfhqhnlggkgrfeykhj.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Dependencies conflict
Clean install:
```bash
pip3 uninstall -y streamlit supabase pandas plotly python-dotenv
pip3 install -r requirements.txt
```

---

## What to Test

1. **Engineer Tab**: Create, edit, delete sensors and records
2. **Analyst Tab**: View charts, filter data, export CSV
3. **Validations**: Try invalid inputs (future dates, non-numbers)
4. **Charts**: Interact with plots (zoom, pan, hover)
5. **Data Export**: Download and verify CSV files

See `MANUAL_TESTING_CHECKLIST.md` for detailed step-by-step instructions.

---

## Project Structure Reminder

```
/Users/yevhen/biogas-sensor-app/
├── streamlit_app.py          # Main application - RUN THIS
├── requirements.txt           # Dependencies
├── .env                       # Supabase credentials (not in git)
├── database/                  # Database layer
├── components/                # UI components
└── utils/                     # Utilities
```

---

## Quick Commands

| Command | Action |
|---------|--------|
| `python3 -m streamlit run streamlit_app.py` | Start the app |
| `Ctrl+C` | Stop the app |
| `python3 -m streamlit run streamlit_app.py --server.port 8502` | Run on different port |
| `python3 -m streamlit cache clear` | Clear Streamlit cache |

---

**Ready to test? Start the app and open `MANUAL_TESTING_CHECKLIST.md`!**
