# 🔬 Biogas Sensor Data Management System

A robust sensor data collection and management system for PhD dissertation research on Biogas Optimization.

[![Production](https://img.shields.io/badge/Production-Live-success)](https://biogas-sensor.streamlit.app)
[![Version](https://img.shields.io/badge/Version-v0.1.1-blue)](https://github.com/ybatsiun/biogas-sensor/releases)

---

## 📋 Overview

This application provides a comprehensive interface for:
- **Engineers**: Manual sensor data entry and management
- **Analysts**: Interactive data visualization and export capabilities

**Live App**: https://biogas-sensor.streamlit.app

---

## ✨ Features

### 👷 Engineer Interface
- ✅ Create, edit, and delete sensors
- ✅ Add sensor records with timestamp and value
- ✅ Edit existing records
- ✅ Form validation
- ✅ Real-time toast notifications

### 📊 Analyst Interface
- ✅ Interactive multi-sensor line charts (Plotly)
- ✅ Configurable sensor selection
- ✅ Date range filtering
- ✅ Data table view with pagination
- ✅ CSV export

### 🌍 Multi-Language Support
- 🇺🇦 Ukrainian (default)
- 🇬🇧 English
- 🇵🇱 Polish

---

## 🚀 Quick Start

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Supabase credentials

# Run the app
streamlit run streamlit_app.py
```

App will open at: http://localhost:8501

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.40.2
- **Database**: Supabase (PostgreSQL)
- **Visualization**: Plotly 5.18.0
- **Testing**: Playwright + pytest
- **Language**: Python 3.10+

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[Project Status](docs/PROJECT_STATUS.md)** | 🌟 **START HERE** - Complete project context |
| [Development Workflow](docs/DEVELOPMENT.md) | Git workflow, releasing, versioning |
| [Testing Guide](docs/TESTING.md) | Testing strategy and commands |
| [Deployment Guide](docs/DEPLOYMENT.md) | Production deployment guide |
| [Test Suite](tests/README.md) | E2E test documentation |

---

## 🌳 Development Workflow

**Branches:**
- `main` - Production (auto-deploys to Streamlit Cloud)
- `develop` - Development (your active work)

**Daily workflow:**

```bash
# Work on develop
git checkout develop
git add .
git commit -m "feat: new feature"
git push origin develop

# Release to production
./create_release.sh
# Creates PR, merge to main → auto-deploys
```

See [Development Workflow](docs/DEVELOPMENT.md) for details.

---

## 🧪 Testing

```bash
# Quick smoke test
python3 -m pytest tests/e2e/test_smoke.py

# Full test suite
python3 -m pytest

# Or use the helper script
./run_tests.sh
```

See [Testing Guide](docs/TESTING.md) for testing philosophy and commands.

---

## 🚢 Deployment

**Production**: Automatically deploys from `main` branch to Streamlit Cloud

**URL**: https://biogas-sensor.streamlit.app

**Versioning**: Auto-tagged on each merge to main (v0.1.0, v0.1.1, ...)

See [Deployment Guide](docs/DEPLOYMENT.md) for details.

---

## 📁 Project Structure

```
biogas-sensor/
├── streamlit_app.py         # Main application entry
├── components/              # UI components
│   ├── engineer.py         # Engineer interface
│   └── analyst.py          # Analyst interface
├── database/               # Database layer
│   ├── client.py          # Supabase client
│   └── queries.py         # Database queries
├── utils/                  # Utilities
│   ├── i18n.py            # Internationalization
│   ├── validation.py      # Input validation
│   └── ui_helpers.py      # UI helpers
├── translations/           # Language files
│   ├── uk.json            # Ukrainian
│   ├── en.json            # English
│   └── pl.json            # Polish
├── tests/                  # E2E test suite
│   └── e2e/               # Playwright tests
├── docs/                   # Documentation
└── .github/workflows/      # CI/CD workflows
```

---

## 🔒 Environment Variables

Required in `.env`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

---

## 🤝 Contributing

This is a PhD research project. For major changes, please open an issue first.

---

## 📜 License

All rights reserved. PhD research project.

---

## 🎯 Roadmap

- [x] Manual CRUD operations
- [x] Data visualization
- [x] Multi-language support
- [x] Mobile-responsive design
- [x] E2E test suite
- [x] Production deployment
- [ ] Authentication system
- [ ] Role-based access control
- [ ] Advanced analytics

---

**Built with ❤️ for PhD research | Powered by Streamlit & Supabase**
