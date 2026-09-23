#!/usr/bin/env bash
# =============================================================================
# push.sh — Quick push helper for db2-enterprise-ai-use-cases
#
# Usage:
#   bash push.sh                        → commits all changes with auto message
#   bash push.sh "your commit message"  → commits with your message
#   bash push.sh --status               → shows git status only (no push)
# =============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# ── Status-only mode ──────────────────────────────────────────────────────────
if [[ "${1:-}" == "--status" ]]; then
  echo -e "${BOLD}Current git status:${RESET}"
  git status --short
  echo ""
  echo -e "${BOLD}Last 5 commits:${RESET}"
  git log --oneline -5
  exit 0
fi

# ── Check for changes ─────────────────────────────────────────────────────────
if git diff --quiet && git diff --staged --quiet && [[ -z "$(git ls-files --others --exclude-standard)" ]]; then
  echo -e "${YELLOW}Nothing to commit — working tree clean.${RESET}"
  git log --oneline -3
  exit 0
fi

# ── Stage all changes ─────────────────────────────────────────────────────────
echo -e "${CYAN}Staging all changes...${RESET}"
git add .

# ── Build commit message ──────────────────────────────────────────────────────
if [[ -n "${1:-}" ]]; then
  COMMIT_MSG="$1"
else
  # Auto-generate a message based on what changed
  CHANGED_FILES=$(git diff --staged --name-only | head -10 | tr '\n' ' ')
  CHANGED_COUNT=$(git diff --staged --name-only | wc -l | tr -d ' ')
  COMMIT_MSG="chore: update ${CHANGED_COUNT} file(s) — ${CHANGED_FILES}"
fi

# ── Commit ────────────────────────────────────────────────────────────────────
echo -e "${CYAN}Committing: ${BOLD}${COMMIT_MSG}${RESET}"
git commit -m "$COMMIT_MSG"

# ── Push ──────────────────────────────────────────────────────────────────────
echo -e "${CYAN}Pushing to origin/main...${RESET}"
git push origin main

echo ""
echo -e "${GREEN}${BOLD}✓ Pushed successfully to github.com:DhruvChaturvediIBM/db2-enterprise-ai-use-cases${RESET}"
echo -e "${GREEN}  https://github.com/DhruvChaturvediIBM/db2-enterprise-ai-use-cases${RESET}"
