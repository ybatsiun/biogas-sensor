# Deployment Guide

Complete guide for deploying the Biogas Sensor App to production.

---

## 🚀 Production Environment

**Platform**: Streamlit Cloud
**URL**: https://biogas-sensor.streamlit.app
**Branch**: `main` (auto-deploys on push)
**Database**: Supabase PostgreSQL

---

## 🔐 Secrets Management

### Streamlit Cloud Secrets

Secrets are configured in Streamlit Cloud Dashboard:

**Location**: App Settings → Advanced Settings → Secrets

**Format** (TOML):
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_key"
```

### How Code Reads Secrets

```python
# database/client.py
url = os.getenv("SUPABASE_URL")  # ← Reads from Streamlit secrets
key = os.getenv("SUPABASE_KEY")
```

Streamlit Cloud automatically injects secrets as environment variables. No code changes needed.

---

## 🌳 Deployment Workflow

### Current Setup

```
develop branch
   ↓ (work here daily)
Create PR to main
   ↓ (when ready to release)
Merge to main (squash)
   ↓ (automatic)
GitHub Auto-Tags (v0.1.0 → v0.1.1)
   ↓ (automatic)
Streamlit Cloud Deploys (~2-3 min)
   ↓
✅ Live in Production!
```

### Daily Development

```bash
# Work on develop
git checkout develop
git add .
git commit -m "feat: new feature"
git push origin develop

# No hooks, no forced testing
```

### Releasing to Production

**Method 1: Helper Script**
```bash
./create_release.sh
# → Creates PR, shows changes
# → Merge on GitHub
```

**Method 2: GitHub CLI**
```bash
gh pr create --base main --head develop --title "Release: description"
gh pr merge --squash --delete-branch=false
```

**Method 3: GitHub Web UI**
1. Go to: https://github.com/ybatsiun/biogas-sensor/pulls
2. Click "New pull request"
3. Base: `main` ← Compare: `develop`
4. Click "Squash and merge"

**Result**: Auto-tagged, auto-deployed within 2-3 minutes.

---

## 🏷️ Versioning

### VERSION File Workflow

**Important**: The app version is stored in the `VERSION` file (not retrieved from git tags).

**Why?** Git tags are created AFTER merge, but Streamlit deploys DURING merge. Using a committed VERSION file ensures the deployed app shows the correct version immediately.

### Releasing a New Version

**Before merging to main**, update the VERSION file:

```bash
# 1. On your feature branch, update VERSION file
echo "v0.1.11" > VERSION

# 2. Commit the change
git add VERSION
git commit -m "Bump version to v0.1.11"

# 3. Create PR and merge to main
gh pr create --base main --head your-branch --title "Release v0.1.11"
gh pr merge --squash --delete-branch=false
```

**Result**:
1. ✅ Streamlit deploys with correct version (from VERSION file)
2. ✅ GitHub Action creates matching git tag automatically
3. ✅ GitHub release published with notes

### Version Format

- **Patch** (v0.1.X): Bug fixes, small changes
- **Minor** (v0.X.0): New features, enhancements
- **Major** (vX.0.0): Breaking changes

**Examples**:
- `v0.1.10` → `v0.1.11` (bug fix)
- `v0.1.11` → `v0.2.0` (new feature)
- `v0.2.0` → `v1.0.0` (breaking change)

### How It Works

```python
# streamlit_app.py
def get_app_version() -> str:
    """Get current app version from VERSION file."""
    with open('VERSION', 'r') as f:
        return f.read().strip()
```

The VERSION file is committed with your code, so the deployed app always shows the correct version.

---

## 🚢 Deployment Steps (First Time)

### 1. Prepare Repository

```bash
# Already done!
✅ Git repository initialized
✅ Code pushed to GitHub
✅ develop branch created
```

### 2. Set Up Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Click "New app"
3. Connect GitHub account
4. Select repository: `ybatsiun/biogas-sensor`
5. Configure:
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.10 or higher

### 3. Configure Secrets

1. In Streamlit Cloud → Your app → Settings → Advanced Settings
2. Add secrets in TOML format:
   ```toml
   SUPABASE_URL = "https://uzgfhqhnlggkgrfeykhj.supabase.co"
   SUPABASE_KEY = "your_key_here"
   ```
3. Click "Save"

### 4. Deploy

Click "Deploy" button

**Wait ~2-3 minutes** for initial deployment.

---

## 🔄 Updating Production

### Standard Update

```bash
# On develop
git add .
git commit -m "fix: bug fix"
git push origin develop

# Create release
./create_release.sh

# Merge PR on GitHub
# → Auto-deploys to production
```

### Hotfix

```bash
# Quick fix on develop
git commit -m "fix: urgent bug"
git push origin develop

# Fast release
gh pr create --base main --head develop --title "Hotfix: bug"
gh pr merge --squash --delete-branch=false

# ✅ Deployed in 2-3 minutes
```

---

## 🔙 Rollback

### Option A: Revert on GitHub

1. Go to: https://github.com/ybatsiun/biogas-sensor/commits/main
2. Find bad commit
3. Click "..." → "Revert"
4. Create PR → Merge
5. ✅ Auto-deploys previous version

### Option B: Local Revert

```bash
git checkout main
git pull
git revert HEAD
git push origin main
# ✅ Auto-deploys reverted version
```

### Option C: Streamlit Cloud Reboot

1. Streamlit Cloud → App → Settings
2. Click "Reboot app"
3. Select previous commit from dropdown
4. Click "Reboot"

---

## 🔍 Monitoring

### Streamlit Cloud Dashboard

**Location**: https://share.streamlit.io

**Monitor**:
- App status (running/stopped)
- Logs (real-time)
- Resource usage
- Deployment history

### Health Checks

**Manual**:
1. Visit https://biogas-sensor.streamlit.app
2. Test engineer interface (add record)
3. Test analyst interface (view charts)
4. Test language switching

**Automated** (future):
- Set up Uptime Robot or similar
- Monitor app availability
- Alert on downtime

---

## ⚠️ Troubleshooting

### App Won't Start

**Check logs** in Streamlit Cloud dashboard:

```
Common issues:
- Missing dependencies in requirements.txt
- Secrets not configured
- Python version mismatch
- Import errors
```

### Fix:
1. Review error logs
2. Fix issue on develop
3. Create PR to main
4. Merge → Auto-deploys fix

### Database Connection Fails

**Check**:
1. Secrets configured correctly (TOML format)
2. Supabase project is active
3. Network not restricted

### App is Slow

**Solutions**:
- Streamlit Cloud auto-sleeps after inactivity
- First load takes ~10-15 seconds (cold start)
- Upgrade to paid tier for always-on

---

## 📊 Deployment Checklist

### Before Each Release

- [ ] Code pushed to develop or feature branch
- [ ] **Update VERSION file** with new version number
- [ ] Commit VERSION file change
- [ ] Tested locally (optional)
- [ ] Review changes: `git log main..your-branch --oneline`
- [ ] Create PR to main
- [ ] Review PR (optional for solo dev)
- [ ] Merge (squash)

### After Release

- [ ] Wait for deployment (~2-3 min)
- [ ] Check Streamlit Cloud logs (no errors)
- [ ] Test live app manually
- [ ] Verify version tag created

### If Issues Found

- [ ] Revert immediately (see Rollback section)
- [ ] Fix on develop
- [ ] Test fix
- [ ] Create new release

---

## 🎯 Best Practices

### ✅ Do This

1. **Always work on develop** - Never commit directly to main
2. **Test locally when you want** - No forced testing
3. **Squash merge to main** - Clean commit history
4. **Let automation handle tags** - Don't create manually
5. **Monitor deployment logs** - Catch issues early

### ❌ Don't Do This

1. **Don't commit secrets** - Already gitignored
2. **Don't push directly to main** - Use PR workflow
3. **Don't skip testing critical changes** - Optional but recommended
4. **Don't delete main branch** - It's production!

---

## 🔒 Security Considerations

### Secrets

- ✅ Secrets in Streamlit Cloud (encrypted)
- ✅ `.env` gitignored
- ✅ Supabase anon key (safe for client-side)

### Future Enhancements

When needed:
- Enable RLS (Row Level Security) on Supabase
- Add authentication
- Implement rate limiting
- Add audit logging

**Current status**: No authentication needed (single user)

---

## 📈 Scaling Considerations

### Current Setup

- **Free tier** Streamlit Cloud
- **Free tier** Supabase
- Single user
- Low traffic

### When to Upgrade

**Streamlit Cloud**:
- App needs to be always-on
- Need more resources
- Multiple apps

**Supabase**:
- More storage needed
- Higher API limits
- Need database backups

---

## 🆘 Support

### Streamlit Issues

- Docs: https://docs.streamlit.io
- Community: https://discuss.streamlit.io
- Status: https://status.streamlit.io

### Supabase Issues

- Docs: https://supabase.com/docs
- Community: https://github.com/supabase/supabase/discussions

---

## 📝 Deployment History

**v0.1.10** (Feb 5, 2026) - Version display fix
- Fixed version display using VERSION file instead of git tags
- Ensures deployed app shows correct version immediately
- Updated documentation with VERSION file workflow

**v0.1.9** (Feb 5, 2026) - Timezone handling
- Fixed timezone handling - store UTC, display local time
- Created timezone utilities (Europe/Kiev)
- User input converted from local to UTC before storage
- All timestamps display in user's local timezone

**v0.1.8** (Feb 5, 2026) - Dark mode disabled
- Disabled dark mode support entirely
- Force light mode across all devices
- Consistent UI experience

**v0.1.5-v0.1.7** (Feb 4-5, 2026) - UI/UX improvements
- Version display in header
- Cleaner layout (removed redundant headers)
- Fixed dropdown visibility issues
- Mobile dark mode improvements
- Date/time picker UX enhancements

**v0.1.0-v0.1.4** (Feb 4, 2026) - Initial production deployment
- Core CRUD operations
- Data visualization
- Multi-language support
- E2E test suite
- Auto-versioning workflow

---

**Need help?** Check logs in Streamlit Cloud dashboard or review [Development Workflow](DEVELOPMENT.md).
