# 📚 Documentation Index

Complete documentation for the Biogas Sensor Data Management System.

## 🆕 For New Claude Code Sessions

**👋 Starting a new session?** Read **[PROJECT_STATUS.md](PROJECT_STATUS.md)** first!

It contains:
- Complete project context
- Current version & deployment status
- Git workflow summary
- Database schema
- Known issues
- Development history
- Everything you need to continue work

---

## 📖 Documentation Guide

| Document | Purpose | Audience |
|----------|---------|----------|
| **[Project Status](PROJECT_STATUS.md)** | 🌟 **START HERE** - Complete project context | Everyone (especially new Claude sessions) |
| **[Development Workflow](DEVELOPMENT.md)** | Git workflow, branching, releasing | Developers |
| **[Testing Guide](TESTING.md)** | Testing philosophy and commands | Developers |
| **[Deployment Guide](DEPLOYMENT.md)** | Production deployment and operations | DevOps/Developers |

---

## 🚀 Quick Links

### For Development

- **Starting a new feature**: See [Development Workflow](DEVELOPMENT.md#daily-development-workflow)
- **Running tests**: See [Testing Guide](TESTING.md#test-commands-reference)
- **Creating a release**: See [Development Workflow](DEVELOPMENT.md#deploying-to-production)

### For Operations

- **Deploying to production**: See [Deployment Guide](DEPLOYMENT.md#deployment-workflow)
- **Rolling back a release**: See [Deployment Guide](DEPLOYMENT.md#rollback)
- **Troubleshooting issues**: See [Deployment Guide](DEPLOYMENT.md#troubleshooting)

### For Testing

- **E2E test suite**: See [../tests/README.md](../tests/README.md)
- **Test strategy**: See [Testing Guide](TESTING.md)
- **Latest test results**: Archived in git history

---

## 📁 Documentation Structure

```
docs/
├── README.md           # This file - documentation index
├── PROJECT_STATUS.md   # 🌟 Complete project context (START HERE)
├── DEVELOPMENT.md      # Development workflow & git strategy
├── TESTING.md          # Testing philosophy & commands
└── DEPLOYMENT.md       # Production deployment guide
```

---

## 🔄 Workflow Overview

```
┌─────────────────────────────────────┐
│ 1. Development (develop branch)     │
│    • Fast iteration                 │
│    • No forced testing              │
│    • See: DEVELOPMENT.md            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 2. Testing (optional)               │
│    • Run when you want confidence   │
│    • See: TESTING.md                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 3. Release (PR to main)             │
│    • Squash merge                   │
│    • Auto-versioning                │
│    • See: DEVELOPMENT.md            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 4. Deploy (automatic)               │
│    • Streamlit Cloud auto-deploys   │
│    • ~2-3 minutes                   │
│    • See: DEPLOYMENT.md             │
└─────────────────────────────────────┘
```

---

## 🎯 Common Tasks

### I want to...

**...start working on a new feature**
→ See [Development Workflow - Daily Workflow](DEVELOPMENT.md#daily-development-workflow)

**...test my changes**
→ See [Testing Guide - Testing Workflows](TESTING.md#testing-workflows)

**...release to production**
→ See [Development Workflow - Deploying to Production](DEVELOPMENT.md#deploying-to-production)

**...rollback a bad release**
→ See [Deployment Guide - Rollback](DEPLOYMENT.md#rollback)

**...understand the test suite**
→ See [Testing Guide - Your Test Suite](TESTING.md#your-test-suite)

**...monitor production**
→ See [Deployment Guide - Monitoring](DEPLOYMENT.md#monitoring)

---

## 🤖 Working with Claude Code

All documentation is optimized for vibe-development with Claude Code. Ask naturally:

```
"Show me how to create a release"
"How do I run tests?"
"What's the deployment process?"
"Help me rollback the last release"
```

Claude Code will guide you through the process using these docs as reference.

---

## 📝 Documentation Philosophy

These docs follow the principle:

> **Just enough documentation to be useful, not so much that it's overwhelming.**

- ✅ Practical examples
- ✅ Quick reference sections
- ✅ Copy-paste commands
- ✅ Optimized for solo vibe-dev
- ❌ No enterprise complexity
- ❌ No forced processes

---

## 🔄 Keeping Docs Updated

Documentation is updated as the project evolves. If you find:
- Outdated information
- Missing procedures
- Unclear explanations

Just ask Claude Code to update the relevant doc.

---

**Last Updated**: February 4, 2026
**Current Version**: v0.1.1
