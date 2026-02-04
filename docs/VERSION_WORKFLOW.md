# VERSION File Workflow

Quick reference guide for managing app versions.

---

## 📋 Overview

The app version is stored in the **`VERSION`** file at the root of the repository. This ensures the deployed app always shows the correct version number.

**Why not use git tags?**
- Git tags are created **after** merge
- Streamlit deploys **during** merge
- Tag doesn't exist in deployment context
- Result: Wrong version displayed

**Solution**: Commit the version number with the code in the `VERSION` file.

---

## 🚀 Quick Start: Release New Version

### Step 1: Update VERSION File

```bash
# On your feature branch
echo "v0.1.11" > VERSION
```

### Step 2: Commit the Change

```bash
git add VERSION
git commit -m "Bump version to v0.1.11"
git push origin your-branch
```

### Step 3: Create PR and Merge

```bash
gh pr create --base main --head your-branch --title "Release v0.1.11: description"
gh pr merge --squash --delete-branch
```

### Result

✅ **Streamlit deploys with v0.1.11** (reads from VERSION file)
✅ **GitHub Action creates v0.1.11 tag** (automatic)
✅ **GitHub Release published** with notes

---

## 📊 Version Number Guidelines

### Format: vMAJOR.MINOR.PATCH

**Patch** (v0.1.X → v0.1.Y)
- Bug fixes
- Small improvements
- No breaking changes
- Example: v0.1.10 → v0.1.11

**Minor** (v0.X.0 → v0.Y.0)
- New features
- Enhancements
- Backwards compatible
- Example: v0.1.11 → v0.2.0

**Major** (vX.0.0 → vY.0.0)
- Breaking changes
- Major rewrites
- API changes
- Example: v0.2.0 → v1.0.0

---

## 📝 Example Scenarios

### Bug Fix Release

```bash
# Current version: v0.1.10
echo "v0.1.11" > VERSION
git add VERSION
git commit -m "Bump version to v0.1.11

fix: timezone display issue"
git push
```

### New Feature Release

```bash
# Current version: v0.1.11
echo "v0.2.0" > VERSION
git add VERSION
git commit -m "Bump version to v0.2.0

feat: add export to PDF functionality"
git push
```

### Breaking Change Release

```bash
# Current version: v0.2.5
echo "v1.0.0" > VERSION
git add VERSION
git commit -m "Bump version to v1.0.0

BREAKING CHANGE: new authentication system"
git push
```

---

## 🔍 Verification

### Check Current Version Locally

```bash
cat VERSION
# Output: v0.1.10
```

### Check Version in Running App

```python
from streamlit_app import get_app_version
print(get_app_version())
# Output: v0.1.10
```

### Check Deployed Version

Visit https://biogas-sensor.streamlit.app and look at the version number in the header.

---

## ⚠️ Common Mistakes

### ❌ Don't: Forget to Update VERSION

```bash
# Bad: Merge without updating VERSION
git push origin feature-xyz
gh pr merge  # ← Deployed app shows old version!
```

### ✅ Do: Always Update VERSION Before Merge

```bash
# Good: Update VERSION first
echo "v0.1.11" > VERSION
git add VERSION
git commit -m "Bump version to v0.1.11"
git push origin feature-xyz
gh pr merge  # ← Deployed app shows v0.1.11 ✅
```

### ❌ Don't: Use Inconsistent Format

```bash
# Bad formats:
echo "0.1.11" > VERSION      # Missing 'v' prefix
echo "v0.1" > VERSION        # Missing patch number
echo "version 0.1.11" > VERSION  # Extra text
```

### ✅ Do: Use Standard Format

```bash
# Good format:
echo "v0.1.11" > VERSION     # Correct: v + semver
```

---

## 🔧 Troubleshooting

### Problem: Deployed App Shows Wrong Version

**Cause**: VERSION file not updated before merge

**Fix**:
1. Update VERSION file on a new branch
2. Commit and push
3. Create PR and merge
4. Redeploy will show correct version

### Problem: Git Tag Doesn't Match VERSION

**Cause**: Manual tag creation or VERSION update after merge

**Fix**:
1. Git tags are created automatically by GitHub Action
2. Always update VERSION **before** merging
3. Tag will match VERSION content automatically

---

## 🤖 Automation

### GitHub Action (Already Configured)

The `.github/workflows/tag-on-merge.yml` workflow:
1. Triggers on merge to main
2. Reads version from VERSION file
3. Creates matching git tag
4. Publishes GitHub release

You don't need to do anything - it's automatic!

---

## 📚 Related Documentation

- [Deployment Guide](DEPLOYMENT.md) - Full deployment documentation
- [Development Workflow](DEVELOPMENT.md) - Development guidelines
- [Project Status](PROJECT_STATUS.md) - Current project status

---

## ✅ Checklist for Every Release

Before merging:
- [ ] Update VERSION file with new version
- [ ] Commit VERSION change
- [ ] Version follows semver format (vX.Y.Z)
- [ ] Version number is incremented correctly
- [ ] PR title includes version number

After merging:
- [ ] Check Streamlit Cloud shows correct version
- [ ] Verify git tag was created
- [ ] Confirm GitHub release published

---

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for more details.
