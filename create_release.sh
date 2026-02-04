#!/bin/bash
# Helper script to create a release PR from develop to main

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Creating Release PR${NC}"
echo ""

# Check if we're on develop
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "develop" ]; then
    echo -e "${YELLOW}⚠️  You're on '${CURRENT_BRANCH}', switching to develop...${NC}"
    git checkout develop
fi

# Pull latest
echo -e "${BLUE}📥 Pulling latest changes...${NC}"
git pull origin develop

# Show what will be released
echo ""
echo -e "${BLUE}📝 Changes since last release:${NC}"
echo ""
git log main..develop --oneline --no-decorate | head -20
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

$(git log main..develop --pretty=format:"- %s" | head -20)

---

Ready for production deployment.
This will auto-tag and deploy to Streamlit Cloud."

# Create PR
echo ""
echo -e "${BLUE}🔨 Creating pull request...${NC}"
gh pr create \
    --base main \
    --head develop \
    --title "$PR_TITLE" \
    --body "$PR_BODY"

echo ""
echo -e "${GREEN}✅ Pull request created!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review PR on GitHub"
echo "2. Merge using: ${BLUE}gh pr merge --squash --delete-branch=false${NC}"
echo "3. Or merge via GitHub web UI"
echo ""
echo -e "${GREEN}After merge:${NC}"
echo "• Auto-tag will be created (v0.1.x)"
echo "• GitHub release will be published"
echo "• Streamlit Cloud will auto-deploy"
