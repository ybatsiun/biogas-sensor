#!/bin/bash
# Helper script to create a release PR from current feature branch to main

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0;33m' # No Color

echo -e "${BLUE}🚀 Creating Release PR${NC}"
echo ""

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if we're on main
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo -e "${YELLOW}⚠️  You're on 'main'. Please switch to your feature branch first.${NC}"
    exit 1
fi

echo -e "${BLUE}Current branch: ${GREEN}${CURRENT_BRANCH}${NC}"
echo ""

# Pull latest from current branch
echo -e "${BLUE}📥 Pulling latest changes from ${CURRENT_BRANCH}...${NC}"
git pull origin "$CURRENT_BRANCH" 2>/dev/null || echo "Branch not pushed yet, that's OK."

# Show what will be released
echo ""
echo -e "${BLUE}📝 Changes since last release:${NC}"
echo ""
git log main.."$CURRENT_BRANCH" --oneline --no-decorate | head -20
echo ""

# Get PR title
echo -e "${BLUE}Enter release title (or press Enter for default):${NC}"
read -r PR_TITLE
if [ -z "$PR_TITLE" ]; then
    # Generate default title from recent commits
    RECENT_COMMIT=$(git log -1 --pretty=format:"%s")
    PR_TITLE="Release: ${RECENT_COMMIT}"
fi

# Create PR body
PR_BODY="## Changes in this release

$(git log main.."$CURRENT_BRANCH" --pretty=format:"- %s" | head -20)

---

Ready for production deployment.
This will auto-tag and deploy to Streamlit Cloud."

# Create PR
echo ""
echo -e "${BLUE}🔨 Creating pull request...${NC}"
gh pr create \
    --base main \
    --head "$CURRENT_BRANCH" \
    --title "$PR_TITLE" \
    --body "$PR_BODY"

echo ""
echo -e "${GREEN}✅ Pull request created!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review PR on GitHub"
echo "2. Merge using: ${BLUE}gh pr merge --squash --delete-branch${NC}"
echo "3. Or merge via GitHub web UI (check 'Delete branch')"
echo ""
echo -e "${GREEN}After merge:${NC}"
echo "• Branch '${CURRENT_BRANCH}' will be deleted ✅"
echo "• Auto-tag will be created (v0.1.x)"
echo "• GitHub release will be published"
echo "• Streamlit Cloud will auto-deploy"
echo ""
echo -e "${YELLOW}For next feature:${NC}"
echo "• Start fresh: ${BLUE}git checkout main && git pull && git checkout -b feature/next-thing${NC}"
