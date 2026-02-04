# Development Workflow

Git workflow for the Biogas Sensor App optimized for vibe-development with Claude Code.

---

## 🌳 Branch Strategy

```
main (production)
  ↓
  Tagged: v0.1.0, v0.1.1, v0.1.2...
  ↓
develop (development)
  ↓
  Your work happens here
```

### Branches

- **`main`** - Production branch, auto-deploys to Streamlit Cloud
- **`develop`** - Development branch, your active work

---

## 💻 Daily Development Workflow

### **Starting Work**

```bash
# Make sure you're on develop
git checkout develop

# Pull latest changes
git pull origin develop

# Start coding with Claude Code! 🎉
```

### **Making Changes (Vibe Mode)**

```bash
# Work with Claude Code
# Make changes, iterate fast

# Commit when you feel like it (no hooks, no friction)
git add .
git commit -m "feat: add new feature"

# Keep committing as you go
git commit -m "fix: minor adjustment"
git commit -m "refactor: improve code"

# Push to GitHub when ready
git push origin develop
```

**No pre-commit hooks** → Fast, fluid development ✨

---

## 🚀 Deploying to Production

When you're ready to release:

### **Option A: Using GitHub CLI (Recommended)**

```bash
# From develop branch
gh pr create \
  --base main \
  --head develop \
  --title "Release: [Brief description]" \
  --body "## Changes
- Feature 1
- Feature 2
- Bug fix 3

Ready to deploy to production."

# After PR is reviewed (or immediately if solo)
gh pr merge --squash --delete-branch=false
```

### **Option B: Using Helper Script**

```bash
# Create PR to main
./create_release.sh

# Follow prompts
```

### **Option C: Using GitHub Web UI**

1. Go to: https://github.com/ybatsiun/biogas-sensor/pulls
2. Click "New pull request"
3. Base: `main` ← Compare: `develop`
4. Create PR
5. Click "Squash and merge"

---

## 🏷️ Auto-Versioning

**Automatic on every merge to main:**

```
Merge PR to main
  ↓
GitHub Action runs
  ↓
Creates tag: v0.1.0 → v0.1.1
  ↓
Creates GitHub Release with notes
  ↓
Streamlit Cloud auto-deploys
  ↓
✅ Production updated!
```

### Version Format

- **Patch bumps automatically**: `v0.1.0` → `v0.1.1` → `v0.1.2`
- **Manual major/minor**: Edit tag if needed

### First Release

```bash
# Start versioning from v0.1.0
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

Next merge will create `v0.1.1`, then `v0.1.2`, etc.

---

## 🧪 Testing Strategy (Vibe Development)

### **During Development (develop branch)**

**No required testing** - Iterate fast! 🚀

```bash
# Optional: Test if you want
python3 -m pytest tests/e2e/test_smoke.py  # Quick smoke tests

# Optional: Test specific feature
python3 -m pytest tests/e2e/test_engineer.py

# Or ask Claude Code to run tests for you
```

### **Before Release (Optional)**

```bash
# Run full test suite if you want confidence
python3 -m pytest

# Or just deploy and test in production (it's just you!)
```

### **In Production**

- ✅ Streamlit Cloud monitors app health
- ✅ You can test manually at https://biogas-sensor.streamlit.app
- ✅ Easy rollback: Just revert and merge again

---

## 🔄 Common Scenarios

### **Scenario 1: Quick Fix**

```bash
# On develop
git pull origin develop

# Make fix
# ... edit files ...

git add .
git commit -m "fix: urgent bug fix"
git push origin develop

# Create PR and merge
gh pr create --base main --head develop --title "Hotfix: bug fix"
gh pr merge --squash --delete-branch=false

# ✅ Auto-tagged and deployed!
```

### **Scenario 2: Feature Development**

```bash
# Work on develop for days/weeks
git commit -m "feat: start new feature"
git commit -m "feat: add more functionality"
git commit -m "fix: adjust behavior"
git push origin develop

# When feature is ready
gh pr create --base main --head develop --title "Feature: new analytics"
# Review, then merge
# ✅ All commits squashed into one, tagged, deployed!
```

### **Scenario 3: Rollback**

```bash
# Something broke in production!

# Option A: Revert on GitHub
1. Go to main branch commits
2. Find bad commit
3. Click "Revert"
4. Merge revert PR
5. ✅ Auto-tagged and deployed!

# Option B: Local revert
git checkout main
git pull
git revert HEAD
git push origin main
# ✅ Auto-tagged and deployed!
```

---

## 🎯 Best Practices for Vibe-Dev

### **✅ Do This**

1. **Commit often** - No hooks, no friction
2. **Push to develop frequently** - Back up your work
3. **Test manually when you feel like it** - No requirements
4. **Create PR when ready for production** - Squash all commits
5. **Let automation handle versioning** - Tags auto-created

### **❌ Don't Do This**

1. **Don't commit directly to main** - Always use develop → PR → main
2. **Don't manually create tags** - Auto-versioning handles it
3. **Don't worry about commit messages on develop** - They get squashed
4. **Don't feel pressured to test** - It's optional during development

---

## 🛠️ Helper Commands

```bash
# Check current branch
git branch

# Switch to develop
git checkout develop

# View recent commits
git log --oneline -10

# View all tags
git tag -l

# Compare develop with main
git log main..develop --oneline

# See what would be in the PR
git diff main...develop
```

---

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────┐
│ develop branch                          │
│                                         │
│ • Fast iteration with Claude Code       │
│ • No hooks, no friction                 │
│ • Commit whenever                       │
│ • Optional testing                      │
└─────────────────────────────────────────┘
              ↓ (when ready)
┌─────────────────────────────────────────┐
│ Create PR: develop → main               │
│                                         │
│ • Review changes (optional)             │
│ • Squash merge                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ main branch                             │
│                                         │
│ • Auto-tag: v0.1.0 → v0.1.1            │
│ • Auto-release notes                    │
│ • Streamlit Cloud deploys               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Production                              │
│ https://biogas-sensor.streamlit.app     │
└─────────────────────────────────────────┘
```

---

## 🎉 Summary

**Your workflow:**

```bash
# Work on develop (iterate fast)
git commit -m "whatever"
git push origin develop

# When ready for production
gh pr create --base main --head develop --title "Release: cool stuff"
gh pr merge --squash --delete-branch=false

# ✅ Done! Auto-tagged, auto-deployed
```

**That's it!** No complex branching, no forced testing, maximum flow state. 🌊

---

**Questions?** Check GitHub Actions at: https://github.com/ybatsiun/biogas-sensor/actions
