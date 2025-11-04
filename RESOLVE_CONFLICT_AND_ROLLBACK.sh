#!/bin/bash

# Quantum Nexus - Resolve Conflict and Rollback Script
# Resolves unmerged files conflict and rolls back to v6.7.58
# Date: 2025-11-05

echo "=================================================="
echo "Quantum Nexus - Resolve Conflict & Rollback"
echo "=================================================="
echo ""

# Step 1: Navigate to project directory
echo "Step 1: Navigating to project directory..."
cd /root/quantum-nexus || exit 1

# Step 2: Check git status
echo ""
echo "Step 2: Checking git status..."
git status

# Step 3: Abort any active merge
echo ""
echo "Step 3: Aborting any active merge..."
if git merge --abort 2>/dev/null; then
    echo "✅ Merge aborted"
else
    echo "ℹ️  No active merge to abort"
fi

# Step 4: Reset any uncommitted changes
echo ""
echo "Step 4: Resetting uncommitted changes..."
git reset --hard HEAD
echo "✅ Working directory cleaned"

# Step 5: Remove any untracked files (optional - be careful!)
echo ""
read -p "Remove untracked files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git clean -fd
    echo "✅ Untracked files removed"
else
    echo "⏭️  Skipped removing untracked files"
fi

# Step 6: Fetch latest from GitHub
echo ""
echo "Step 6: Fetching latest from GitHub..."
git fetch origin
if [ $? -eq 0 ]; then
    echo "✅ Fetched successfully"
else
    echo "❌ Git fetch failed!"
    exit 1
fi

# Step 7: Reset to v6.7.58 commit
echo ""
echo "Step 7: Resetting to commit 8d8ebf3 (v6.7.58)..."
if git reset --hard 8d8ebf3; then
    echo "✅ Reset to v6.7.58 successful"
else
    echo "❌ Git reset failed!"
    exit 1
fi

# Step 8: Verify
echo ""
echo "Step 8: Verifying..."
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "Current commit: $CURRENT_COMMIT"
if [ "$CURRENT_COMMIT" = "8d8ebf3" ]; then
    echo "✅ Confirmed: Rolled back to commit 8d8ebf3"
else
    echo "⚠️  Warning: Current commit is $CURRENT_COMMIT (expected 8d8ebf3)"
fi

# Step 9: Check status again
echo ""
echo "Step 9: Final git status..."
git status

echo ""
echo "=================================================="
echo "✅ Conflict Resolved & Rollback Complete!"
echo "=================================================="
echo ""
echo "Next: Run ROLLBACK_v6.7.58.sh to copy files and restart services"
echo ""
