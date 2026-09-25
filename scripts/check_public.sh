#!/usr/bin/env bash
# Guard: blocks internal/confidential terms from reaching public/.
#
# 1) As a git pre-commit hook:   ln -s ../../scripts/check_public.sh .git/hooks/pre-commit
# 2) As a Claude Code hook (.claude/settings.json):
#    "hooks": { "PreToolUse": [ { "matcher": "Write|Edit",
#       "hooks": [ { "type": "command", "command": "scripts/check_public.sh --claude" } ] } ] }
#    In --claude mode the script reads the tool call JSON from stdin; exit code 2 = block + reason to Claude.

set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STOP="$ROOT/private/stopwords.txt"
if [[ ! -f "$STOP" ]]; then echo "⚠ check_public: $STOP not found — stop-word check SKIPPED (the list is never committed; restore it from your private backup)" >&2; exit 0; fi
PATTERN="$(grep -v '^\s*#' "$STOP" | grep -v '^\s*$' | paste -sd'|' -)"

if [[ "${1:-}" == "--claude" ]]; then
  INPUT="$(cat)"
  FILE="$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')"
  [[ "$FILE" == *"/public/"* || "$FILE" == *"/agent/"* ]] || exit 0
  TEXT="$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')"
  if HIT="$(echo "$TEXT" | grep -oiE "$PATTERN" | sort -u | paste -sd', ' -)"; then
    echo "Blocked: public/ must not contain internal terms: $HIT. Rephrase generically." >&2
    exit 2
  fi
  exit 0
fi

# --all: scan the files themselves (not only staged diffs)
if [[ "${1:-}" == "--all" ]]; then
  if grep -rniE "$PATTERN" "$ROOT/public" "$ROOT/agent" "$ROOT/site" "$ROOT/docs" "$ROOT/n8n" "$ROOT/prompts" "$ROOT/README.md" 2>/dev/null; then
    echo "❌ internal terms found (see above)" >&2; exit 1
  fi
  echo "✓ no internal terms in public files"; exit 0
fi

# git mode: check staged files under public/
FILES="$(git diff --cached --name-only --diff-filter=ACM -- public/ agent/ || true)"
[[ -z "$FILES" ]] && exit 0
if git diff --cached -- public/ agent/ | grep '^+' | grep -niE "$PATTERN"; then
  echo "❌ Commit blocked: internal terms found in public/ (see above)." >&2
  exit 1
fi
