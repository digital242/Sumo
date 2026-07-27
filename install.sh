#!/usr/bin/env bash
#
# Sumo one-command installer.
#
#   curl -fsSL https://raw.githubusercontent.com/digital242/sumo/main/install.sh | bash
#
# or, from a checkout:
#
#   ./install.sh
#
# What it does:
#   1. checks you have Python 3.10+
#   2. installs Sumo (editable) so the `sumo` command is on your PATH
#   3. optionally sets up a local model via Ollama for real reasoning
#   4. runs `sumo doctor` so you can see it working
#
# It is safe to re-run. It never touches anything outside pip and (if you
# opt in) Ollama.

set -euo pipefail

REPO_URL="https://github.com/digital242/sumo.git"
MIN_PY_MINOR=10
BLUE='\033[0;34m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

say()  { printf "${BLUE}==>${NC} %s\n" "$1"; }
ok()   { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$1"; }
die()  { printf "${RED}✗ %s${NC}\n" "$1" >&2; exit 1; }

# --- 1. locate a suitable Python -----------------------------------------
find_python() {
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
      if "$cand" -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, ${MIN_PY_MINOR}) else 1)" 2>/dev/null; then
        echo "$cand"; return 0
      fi
    fi
  done
  return 1
}

say "Checking for Python 3.${MIN_PY_MINOR}+ ..."
PY="$(find_python)" || die "Python 3.${MIN_PY_MINOR}+ is required. Install it from https://www.python.org/downloads/ and re-run."
ok "Using $($PY --version)"

# --- 2. get the source ----------------------------------------------------
# If we're already inside a Sumo checkout, install from here. Otherwise
# clone into ./sumo.
if [ -f "pyproject.toml" ] && grep -q 'name = "sumo-ai"' pyproject.toml 2>/dev/null; then
  SRC_DIR="$(pwd)"
  say "Installing from the current checkout: ${SRC_DIR}"
else
  SRC_DIR="$(pwd)/sumo"
  if [ -d "$SRC_DIR/.git" ]; then
    say "Updating existing checkout in ${SRC_DIR} ..."
    git -C "$SRC_DIR" pull --ff-only || warn "Could not fast-forward; using the checkout as-is."
  else
    command -v git >/dev/null 2>&1 || die "git is required to clone Sumo. Install git and re-run."
    say "Cloning Sumo into ${SRC_DIR} ..."
    git clone --depth 1 "$REPO_URL" "$SRC_DIR"
  fi
fi

# --- 3. install -----------------------------------------------------------
say "Installing the \`sumo\` command ..."
"$PY" -m pip install --upgrade pip >/dev/null 2>&1 || warn "Could not upgrade pip; continuing."
"$PY" -m pip install -e "$SRC_DIR"
ok "Installed. Try: sumo --help"

# --- 4. offer to set up a local model ------------------------------------
if command -v ollama >/dev/null 2>&1; then
  ok "Ollama detected — Sumo will use it automatically for real reasoning."
  if ! ollama list 2>/dev/null | grep -q .; then
    warn "No local models pulled yet. Run:  ollama pull llama3.2"
  fi
else
  warn "Ollama not found. Sumo works now in offline mode, but for real"
  warn "reasoning install Ollama from https://ollama.com and run:"
  warn "    ollama run llama3.2"
fi

# --- 5. show it working ---------------------------------------------------
echo
say "Running \`sumo doctor\`:"
echo
( cd "$SRC_DIR" && "$PY" -m sumo.cli doctor ) || true
echo
ok "Done. Start with:  sumo chat \"hello sumo\""
