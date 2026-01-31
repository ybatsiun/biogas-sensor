# Production Deployment Strategy

## 🔐 1. Secrets Management

### Current Setup
- ✅ `.env` file (local development, gitignored)
- ✅ `.env.example` template for onboarding
- ✅ Supabase anon key is safe for client-side (RLS would protect data)

### Production Secrets Management

#### Option A: Streamlit Cloud (Recommended for this project)
**Secrets location**: Streamlit Cloud Dashboard → App Settings → Secrets

```toml
# .streamlit/secrets.toml (for Streamlit Cloud)
SUPABASE_URL = "https://uzgfhqhnlggkgrfeykhj.supabase.co"
SUPABASE_KEY = "your_anon_key_here"
```

**How it works**:
1. Create `.streamlit/secrets.toml` in your app settings (web UI only)
2. Never commit this file to git
3. Access via `st.secrets["SUPABASE_URL"]` in code

**Advantages**:
- ✅ No code changes needed (dotenv loads from secrets automatically)
- ✅ Web UI for managing secrets
- ✅ Secrets encrypted at rest
- ✅ Free tier includes secrets management

#### Option B: Environment Variables (Alternative)
For other hosting platforms (Heroku, Railway, Render):
- Set environment variables via platform dashboard
- No code changes needed (python-dotenv reads from env)

#### Option C: HashiCorp Vault / AWS Secrets Manager (Enterprise)
**Only if you need**:
- Secret rotation
- Audit trails
- Multiple teams accessing secrets
- Compliance requirements (HIPAA, SOC 2)

**Current verdict**: **NOT NEEDED** for PhD project at this stage.

---

### Secret Rotation Strategy

**Current risk**: LOW
- Supabase anon key is meant for client-side use
- Protected by RLS policies (when enabled)
- No sensitive operations exposed

**Rotation schedule**:
- 📅 Every 90 days (optional)
- 🚨 Immediately if compromised
- 🔄 Use Supabase dashboard → Settings → API → Regenerate keys

---

### Multi-Environment Secrets

```
# Local Development
.env                          # Your dev credentials

# Staging/Test
Streamlit Cloud (test app)    # Test Supabase project
OR
Supabase Branch               # Preview database

# Production
Streamlit Cloud (prod app)    # Production Supabase project
```

---

## 🚀 2. DEPLOYMENT WORKFLOW

### Recommended: GitHub Actions + Streamlit Cloud Auto-Deploy

#### Branch Strategy
```
main          → Production (auto-deploy to Streamlit Cloud)
develop       → Staging (auto-deploy to Streamlit Cloud test app)
feature/*     → Local development + preview PRs
```

#### Step-by-Step Setup

**1. GitHub Repository Setup**
```bash
cd /Users/yevhen/biogas-sensor-app/biogas-sensor-app
git init
git add .
git commit -m "Initial commit: Biogas Sensor App v1.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/biogas-sensor-app.git
git push -u origin main
```

**2. Streamlit Cloud Production Setup**
- Go to https://share.streamlit.io
- Click "New app"
- Connect GitHub repo
- Select branch: `main`
- Set secrets in app settings
- Deploy!

**3. Streamlit Cloud Staging Setup** (Optional but recommended)
- Create another app in Streamlit Cloud
- Connect to same repo
- Select branch: `develop`
- Use separate Supabase project or branch
- Deploy!

---

### Deployment Checklist

**Before deploying to production**:
- [ ] Run E2E tests locally (see section 3)
- [ ] Check `.gitignore` excludes `.env`
- [ ] Verify `requirements.txt` is up to date
- [ ] Test on staging environment first
- [ ] Review Supabase usage (check if close to limits)
- [ ] Backup production database
- [ ] Document new features in CHANGELOG.md

**After deployment**:
- [ ] Smoke test: Open production URL
- [ ] Test: Add a record
- [ ] Test: Switch languages
- [ ] Test: View charts
- [ ] Monitor Streamlit Cloud logs for errors
- [ ] Check Supabase dashboard for query performance

---

### GitHub Actions CI/CD Pipeline (Optional)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest playwright
        playwright install chromium

    - name: Run E2E tests
      env:
        SUPABASE_URL: ${{ secrets.SUPABASE_TEST_URL }}
        SUPABASE_KEY: ${{ secrets.SUPABASE_TEST_KEY }}
      run: |
        pytest tests/e2e/

    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results/
```

**Advantages**:
- ✅ Automatic testing on every push
- ✅ Prevents broken code from reaching production
- ✅ Test results visible in PR
- ✅ Free for public repos

---

## 🧪 3. E2E TEST SUITE

### Test Strategy

**What to test**:
1. ✅ **Smoke tests**: App loads, database connects
2. ✅ **Critical path**: Engineer adds record → Analyst views it
3. ✅ **Multi-language**: Switch between UK/EN/PL
4. ✅ **Data integrity**: Record appears in database
5. ❌ **NOT testing**: Complex chart interactions (too flaky)

**Test framework**: Playwright (Python) + pytest

---

### Test Environment Setup

```bash
# Install test dependencies
pip install pytest playwright pytest-playwright
playwright install chromium
```

---

## 🏗️ 4. TEST ENVIRONMENT ARCHITECTURE

### Recommended: Supabase Branching (Preview Databases)

Supabase offers **preview databases** for testing without affecting production.

#### Option A: Supabase Branch (Recommended)
```
Production:
  - Project: uzgfhqhnlggkgrfeykhj
  - Database: Production data

Test/Staging:
  - Supabase Branch: "staging" or "test"
  - Database: Fresh schema, seed data
  - Cost: ~$0.01/hour (only when active)
```

**Advantages**:
- ✅ Isolated test data
- ✅ Same schema as production (migrations applied)
- ✅ Can merge schema changes to prod
- ✅ Automatic cleanup

#### Option B: Separate Supabase Project
```
Production Project:
  - uzgfhqhnlggkgrfeykhj

Test Project:
  - Create new project: "biogas-sensor-test"
  - Free tier available
  - Completely isolated
```

**Advantages**:
- ✅ 100% isolated
- ✅ Free tier (500MB, unlimited API calls)
- ✅ Can break things without worry

**Disadvantages**:
- ❌ Need to manage two projects
- ❌ Schema drift risk (prod vs test)

---

### My Recommendation: **Supabase Branch + Separate Streamlit App**

```
┌─────────────────────────────────────────┐
│         LOCAL DEVELOPMENT               │
│  - .env with dev Supabase creds         │
│  - Run: streamlit run streamlit_app.py  │
└─────────────────────────────────────────┘
                  ↓
         git push to feature/*
                  ↓
┌─────────────────────────────────────────┐
│      STAGING (Streamlit Cloud)          │
│  - Branch: develop                      │
│  - Supabase: Branch "staging"           │
│  - URL: biogas-sensor-staging.app       │
│  - E2E tests run against this           │
└─────────────────────────────────────────┘
                  ↓
    Merge develop → main (after tests pass)
                  ↓
┌─────────────────────────────────────────┐
│     PRODUCTION (Streamlit Cloud)        │
│  - Branch: main                         │
│  - Supabase: Production project         │
│  - URL: biogas-sensor.app               │
│  - Real user data                       │
└─────────────────────────────────────────┘
```

---

## 🚨 CONCERNS & RISKS

### 1. ❗ NO ROW LEVEL SECURITY (RLS)
**Current state**: Database is open to anyone with the anon key

**Risk**:
- Anyone can read all sensor data
- Anyone can insert/update/delete records
- No user isolation

**Mitigation** (if needed in future):
```sql
-- Enable RLS on tables
ALTER TABLE sensors ENABLE ROW LEVEL SECURITY;
ALTER TABLE sensor_records ENABLE ROW LEVEL SECURITY;

-- Allow public read (for now)
CREATE POLICY "Allow public read" ON sensors FOR SELECT USING (true);
CREATE POLICY "Allow public read" ON sensor_records FOR SELECT USING (true);

-- Restrict writes (require authentication)
CREATE POLICY "Authenticated users can insert" ON sensors FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');
```

**Current verdict**: **ACCEPTABLE** for PhD project (internal use only)

---

### 2. ❗ NO AUTHENTICATION
**Current state**: Anyone with the URL can access the app

**Risk**:
- Unauthorized data entry
- Data tampering
- No audit trail of who changed what

**Mitigation options**:
1. **Streamlit built-in auth** (community cloud has basic auth)
2. **Supabase Auth** (email/password, OAuth)
3. **Network-level protection** (VPN, IP whitelist)

**Current verdict**: **ACCEPTABLE** for Step 0, **REQUIRED** for production use

---

### 3. ❗ NO DATABASE BACKUPS
**Current state**: Relying on Supabase automatic backups

**Risk**:
- Accidental data deletion
- No point-in-time recovery beyond Supabase retention

**Mitigation**:
```bash
# Manual backup script
pg_dump "postgresql://postgres:[PASSWORD]@db.uzgfhqhnlggkgrfeykhj.supabase.co:5432/postgres" \
  > backup_$(date +%Y%m%d).sql
```

**Recommendation**:
- ✅ Free tier: 7 days of backups (Supabase handles this)
- ⚠️ If critical data: Upgrade to Pro ($25/mo) for point-in-time recovery

---

### 4. ❗ NO ERROR MONITORING
**Current state**: Errors only visible in Streamlit Cloud logs

**Risk**:
- Silent failures
- No alerting for critical errors
- Difficult to debug production issues

**Mitigation options**:
1. **Sentry** (error tracking, free tier available)
2. **Streamlit built-in logs** (current solution)
3. **Custom logging** to external service

**Recommendation**: Add Sentry for production (5-10 lines of code)

```python
# streamlit_app.py
import sentry_sdk
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
```

---

### 5. ⚠️ LIMITED SCALABILITY
**Current setup**:
- Streamlit Cloud: 1 CPU, 800MB RAM
- Supabase Free: 500MB database, 2GB bandwidth

**Concerns**:
- If data grows beyond 500MB, need to upgrade ($25/mo)
- Streamlit Cloud has rate limits (refreshes, connections)
- No horizontal scaling

**Current verdict**: **SUFFICIENT** for PhD project (hundreds of sensors, thousands of records)

---

### 6. ⚠️ NO STAGING DATABASE SEEDING
**Current state**: Test/staging database is empty

**Risk**:
- Tests fail because no data exists
- Can't demo on staging without manual setup

**Mitigation**: Create seed data script

```python
# scripts/seed_test_data.py
# Populate test database with realistic data
```

---

## 📋 ACTION ITEMS

### Priority 1: Essential for Production
1. [ ] Set up GitHub repository
2. [ ] Deploy to Streamlit Cloud (production)
3. [ ] Configure secrets in Streamlit Cloud
4. [ ] Test production deployment
5. [ ] Create E2E test suite (basic smoke tests)

### Priority 2: Recommended Before Production
6. [ ] Set up staging environment (Supabase branch + Streamlit Cloud)
7. [ ] Enable GitHub Actions CI/CD
8. [ ] Add error monitoring (Sentry)
9. [ ] Document deployment process for team

### Priority 3: Future Enhancements
10. [ ] Enable Row Level Security (RLS)
11. [ ] Add authentication (Supabase Auth)
12. [ ] Set up automated database backups
13. [ ] Create database seeding script
14. [ ] Add monitoring dashboard (Supabase Analytics)

---

## 🎯 RECOMMENDED DEPLOYMENT PATH

**For your PhD project, I recommend**:

### Minimal Production Setup (Week 1)
```
1. GitHub repo (main branch)
2. Streamlit Cloud production app
3. Current Supabase project
4. Manual testing before each deploy
```

**Effort**: 1-2 hours
**Cost**: $0
**Risk**: Low (internal use, can fix issues quickly)

### Enhanced Setup (Week 2-3, if needed)
```
5. Add E2E test suite (pytest + playwright)
6. GitHub Actions CI (run tests on push)
7. Staging environment (separate Streamlit app)
8. Sentry error monitoring
```

**Effort**: 4-6 hours
**Cost**: $0 (free tiers)
**Risk**: Very low (automated testing catches issues)

---

**Next steps**: Should I create the E2E test suite now?

Would you like me to:
1. ✅ Build the E2E test suite with Playwright
2. ✅ Set up GitHub Actions workflow
3. ✅ Create a database seeding script for tests
4. ✅ Document the complete deployment process

Let me know your priority!
