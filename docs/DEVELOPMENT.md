# Development Workflow

Git workflow for the Biogas Sensor App using **GitHub Flow** with ephemeral feature branches.

---

## 🌳 Branch Strategy (GitHub Flow)

```
main (production)
  ↓ Tagged: v0.1.0, v0.1.1, v0.1.2...
  ↓ Auto-deploys to Streamlit Cloud
  ↓
  ├─ feature/... (created fresh, deleted after merge)
  ├─ fix/...     (created fresh, deleted after merge)
  └─ docs/...    (created fresh, deleted after merge)
```

### **Branches**

- **`main`** - Production branch, auto-deploys to Streamlit Cloud, tagged releases
- **Feature branches** - Short-lived branches for work, deleted after merge

### **Key Principles**

- ✅ Always create feature branches from latest `main`
- ✅ Feature branches are **ephemeral** (deleted after merge)
- ✅ No long-lived development branch
- ✅ Clean, simple, no "X commits ahead" confusion

---

## 💻 Daily Development Workflow

### **Starting New Work**

```bash
# 1. Get latest main
git checkout main
git pull origin main

# 2. Create fresh feature branch
git checkout -b feature/cool-thing
# or use generic name:
git checkout -b develop

# Now you're ready to code! 🎉
```

### **Making Changes (Vibe Mode)**

```bash
# Work with Claude Code
# Make changes, iterate fast

# Commit when you feel like it (no hooks, no friction)
git add .
git commit -m "feat: add cool thing"

# Keep committing as you go
git commit -m "fix: minor adjustment"
git commit -m "docs: update readme"

# Push to GitHub when ready
git push origin feature/cool-thing
# or:
git push origin develop
```

**No pre-commit hooks** → Fast, fluid development ✨

---

## 🚀 Deploying to Production

When you're ready to release:

### **Option A: Using GitHub CLI (Recommended)**

```bash
# From your feature branch
gh pr create \
  --base main \
  --head feature/cool-thing \
  --title "Release: Brief description" \
  --body "## Changes
- Feature 1
- Feature 2
- Bug fix 3

Ready to deploy to production."

# Merge with auto-delete
gh pr merge --squash --delete-branch
```

**✨ That's it!** Branch is deleted automatically. Start fresh next time.

### **Option B: Using Helper Script**

```bash
# Create PR to main
./create_release.sh

# Follow prompts
# Script will create PR
# Merge on GitHub with "Squash and merge" + check "Delete branch"
```

### **Option C: Using GitHub Web UI**

1. Go to: https://github.com/ybatsiun/biogas-sensor/pulls
2. Click "New pull request"
3. Base: `main` ← Compare: `feature/cool-thing` (or `develop`)
4. Create PR
5. Click "Squash and merge"
6. ✅ **Check "Delete branch"** ← Important!
7. Confirm

---

## 🏷️ Auto-Versioning

**Automatic on every merge to main:**

```
Merge PR to main
  ↓
GitHub Action runs
  ↓
Creates tag: v0.1.0 → v0.1.1 → v0.1.2
  ↓
Creates GitHub Release with notes
  ↓
Streamlit Cloud auto-deploys
  ↓
✅ Production updated!
```

### **Version Format**

- **Patch bumps automatically**: `v0.1.0` → `v0.1.1` → `v0.1.2`
- **Manual major/minor**: Edit tag if needed

---

## 🔄 Complete Development Cycle

### **Example: Adding a New Feature**

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-auth

# 3. Work on feature (vibe mode)
git add .
git commit -m "feat: add user authentication"
git commit -m "feat: add login page"
git commit -m "fix: validation"
git push origin feature/user-auth

# 4. Create PR
gh pr create --base main --head feature/user-auth \
  --title "Feature: User Authentication"

# 5. Merge with auto-delete
gh pr merge --squash --delete-branch

# 6. Start next feature (fresh from main)
git checkout main
git pull origin main
git checkout -b feature/next-thing
```

**Clean slate every time!** ✨

---

## 🧪 Testing Strategy (Vibe Development)

### **During Development**

**No required testing** - Iterate fast! 🚀

```bash
# Optional: Test if you want confidence
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

---

## 🎯 Branch Naming Conventions

For solo vibe-dev, keep it simple:

### **Recommended Patterns**

```bash
# Generic (simple, familiar)
git checkout -b develop

# Descriptive (better for tracking)
git checkout -b feature/cool-thing
git checkout -b fix/bug-name
git checkout -b docs/update-readme

# Date-based (organized)
git checkout -b dev-2026-02-05
```

**My recommendation**: Use `develop` for simplicity. Recreate it each time.

---

## 🔄 Common Scenarios

### **Scenario 1: Quick Fix**

```bash
# Start from main
git checkout main
git pull origin main

# Create fix branch
git checkout -b fix/urgent-bug

# Make fix
git add .
git commit -m "fix: urgent bug fix"
git push origin fix/urgent-bug

# Create PR and merge
gh pr create --base main --head fix/urgent-bug --title "Hotfix: urgent bug"
gh pr merge --squash --delete-branch

# ✅ Done! Branch deleted automatically
```

### **Scenario 2: Feature Development**

```bash
# Start from main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/analytics

# Work on feature for days/weeks
git commit -m "feat: start analytics"
git commit -m "feat: add charts"
git commit -m "fix: adjust layout"
git push origin feature/analytics

# When ready, create PR and merge
gh pr create --base main --head feature/analytics --title "Feature: Analytics Dashboard"
gh pr merge --squash --delete-branch

# ✅ All commits squashed into one, branch deleted
```

### **Scenario 3: Multiple Features in Progress**

```bash
# Start feature A
git checkout main
git checkout -b feature/auth
# ... work on auth ...
git push origin feature/auth

# Switch to feature B (don't wait for A)
git checkout main
git checkout -b feature/charts
# ... work on charts ...
git push origin feature/charts

# Create PRs for both
gh pr create --base main --head feature/auth --title "Feature: Auth"
gh pr create --base main --head feature/charts --title "Feature: Charts"

# Merge when ready (any order)
gh pr merge 1 --squash --delete-branch
gh pr merge 2 --squash --delete-branch

# ✅ Both branches deleted, clean slate
```

### **Scenario 4: Rollback**

```bash
# Something broke in production!

# Option A: Revert on GitHub
1. Go to main branch commits
2. Find bad commit
3. Click "Revert"
4. Create PR, merge
5. ✅ Deployed!

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

1. **Always start from main** - `git checkout main && git pull`
2. **Use fresh branches** - Create new branch each time
3. **Delete after merge** - Always use `--delete-branch` or check the box
4. **Commit often** - No hooks, no friction
5. **Test when you want** - Optional, not forced

### **❌ Don't Do This**

1. **Don't keep branches after merge** - Delete them!
2. **Don't reuse old branches** - Always create fresh
3. **Don't branch from branches** - Always branch from main
4. **Don't worry about commit history** - Squash merge cleans it up
5. **Don't force yourself to test** - Test when it feels right

---

## 🛠️ Helper Commands

```bash
# Check current branch
git branch

# List all branches
git branch -a

# Switch to main
git checkout main

# Create new branch from main
git checkout main && git pull && git checkout -b feature/new-thing

# View recent commits
git log --oneline -10

# View all tags
git tag -l

# Delete local branch (after merge)
git branch -D feature/old-branch

# Delete remote branch (if not auto-deleted)
git push origin :feature/old-branch
```

---

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────┐
│ 1. Start from main                      │
│    git checkout main && git pull        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. Create feature branch                │
│    git checkout -b feature/cool-thing   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. Work & commit (vibe mode)            │
│    • Fast iteration                     │
│    • No forced testing                  │
│    • Commit freely                      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. Create PR to main                    │
│    gh pr create --base main             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. Merge (squash) + delete branch       │
│    gh pr merge --squash --delete-branch │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 6. Auto-versioning & deploy             │
│    • Tag created (v0.1.x)               │
│    • Release published                  │
│    • Streamlit Cloud deploys            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 7. Repeat (start fresh from main)       │
│    git checkout main && git pull        │
│    git checkout -b feature/next-thing   │
└─────────────────────────────────────────┘
```

---

## 🎉 Summary

**Your workflow in 3 steps:**

1. **Create** fresh branch from main
2. **Work** and commit freely (vibe mode)
3. **Merge** PR with auto-delete

**That's it!** Simple, clean, no confusion. 🌊✨

---

**Last Updated**: February 4, 2026
**Current Version**: v0.1.2
**Workflow**: GitHub Flow (Ephemeral Branches)
