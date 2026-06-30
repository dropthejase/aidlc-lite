#!/usr/bin/env bash
set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/framework" && pwd)"

# ─── colours ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}${*}${RESET}"; }
success() { echo -e "${GREEN}${*}${RESET}"; }
warn()    { echo -e "${YELLOW}${*}${RESET}"; }
error()   { echo -e "${RED}${*}${RESET}"; }
bold()    { echo -e "${BOLD}${*}${RESET}"; }

# ─── welcome ────────────────────────────────────────────────────────────────
echo
bold "┌─────────────────────────────────────────────┐"
bold "│          AIDLC-Lite Setup                   │"
bold "└─────────────────────────────────────────────┘"
echo
echo "This script installs the AIDLC-Lite framework into your project."
echo "It will copy .claude/ and CLAUDE.md from framework/ into your project root."
echo

# ─── agent selection ────────────────────────────────────────────────────────
bold "Which AI coding agent are you using?"
echo "  1) Claude Code  (supported)"
echo "  2) Gemini CLI   (coming soon)"
echo "  3) Codex        (coming soon)"
echo "  4) Kiro         (coming soon)"
echo
read -rp "$(echo -e "${BOLD}Agent [1-4]:${RESET} ")" agent_choice

case "$agent_choice" in
  1) agent="claude" ;;
  2|3|4)
    warn ""
    warn "Multi-agent support is coming soon. Only Claude Code is supported right now."
    warn "Re-run this script and choose option 1, or copy framework/ manually."
    echo
    exit 0
    ;;
  *)
    error "Invalid choice. Exiting."
    exit 1
    ;;
esac

echo
success "Great — installing for Claude Code."
echo

# ─── target path ────────────────────────────────────────────────────────────
bold "Enter the absolute path to your project root:"
read -rp "$(echo -e "${BOLD}Project path:${RESET} ")" target_raw

# expand ~ and strip trailing slash
target="${target_raw/#\~/$HOME}"
target="${target%/}"

if [[ ! -d "$target" ]]; then
  error "Directory not found: $target"
  exit 1
fi

if [[ ! -d "$target/.git" ]]; then
  warn "Warning: $target does not appear to be a git repository."
  warn "AIDLC-Lite uses git worktrees for isolation — it works best in a git repo."
  echo
  read -rp "$(echo -e "${YELLOW}Continue anyway? [y/N]:${RESET} ")" confirm_nogit
  [[ "$confirm_nogit" =~ ^[Yy]$ ]] || exit 0
fi

echo

# ─── conflict check ─────────────────────────────────────────────────────────
conflicts=()
[[ -d "$target/.claude" ]]   && conflicts+=(".claude/")
[[ -f "$target/CLAUDE.md" ]] && conflicts+=("CLAUDE.md")

if [[ ${#conflicts[@]} -gt 0 ]]; then
  warn "The following already exist in $target:"
  for f in "${conflicts[@]}"; do warn "  $f"; done
  echo
  warn "They will be backed up to .claude.bak/ and CLAUDE.md.bak before overwriting."
  echo
  read -rp "$(echo -e "${YELLOW}Proceed and back up existing files? [y/N]:${RESET} ")" confirm_backup
  [[ "$confirm_backup" =~ ^[Yy]$ ]] || exit 0

  [[ -d "$target/.claude" ]]   && cp -R "$target/.claude" "$target/.claude.bak"
  [[ -f "$target/CLAUDE.md" ]] && cp "$target/CLAUDE.md" "$target/CLAUDE.md.bak"
  success "Backed up existing files."
  echo
fi

# ─── preview ────────────────────────────────────────────────────────────────
bold "What will be installed:"
echo "  $target/.claude/          ← skills, agents, hooks, references"
echo "  $target/CLAUDE.md         ← skill routing table + core principles"
echo
bold "After install, open the project in Claude Code and run:"
echo "  /aidlc-init"
echo

read -rp "$(echo -e "${BOLD}Install now? [y/N]:${RESET} ")" confirm_install
[[ "$confirm_install" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ─── install ────────────────────────────────────────────────────────────────
echo
cp -R "$FRAMEWORK_DIR/.claude" "$target/"
cp "$FRAMEWORK_DIR/CLAUDE.md" "$target/"

success "Done! AIDLC-Lite installed into $target"
echo
info "Next step: open $target in Claude Code and run /aidlc-init"
echo
