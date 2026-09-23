#!/usr/bin/env bash
# =============================================================================
# IBM Db2 AI Use Cases — one-command installation script
# Usage:  bash install.sh
# =============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

info()    { echo -e "${GREEN}[INFO]${RESET}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; exit 1; }
section() { echo -e "\n${BOLD}──────────────────────────────────────────────${RESET}"; echo -e "${BOLD} $*${RESET}"; echo -e "${BOLD}──────────────────────────────────────────────${RESET}"; }

# ─────────────────────────────────────────────────────────────────────────────
section "1 / 6 — Checking Python version"
# ─────────────────────────────────────────────────────────────────────────────
PYTHON=$(command -v python3 || command -v python || true)
if [[ -z "$PYTHON" ]]; then
  error "Python 3.10+ is required but was not found. Install from https://www.python.org/"
fi

PY_VERSION=$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
  error "Python 3.10+ required. Found $PY_VERSION"
fi
info "Python $PY_VERSION ✓"

# ─────────────────────────────────────────────────────────────────────────────
section "2 / 6 — Creating virtual environment"
# ─────────────────────────────────────────────────────────────────────────────
if [[ ! -d ".venv" ]]; then
  "$PYTHON" -m venv .venv
  info "Virtual environment created in .venv/"
else
  info ".venv/ already exists — skipping creation"
fi

# Activate
# shellcheck disable=SC1091
source .venv/bin/activate
info "Virtual environment activated"

# Upgrade pip
pip install --quiet --upgrade pip setuptools wheel
info "pip upgraded"

# ─────────────────────────────────────────────────────────────────────────────
section "3 / 6 — Installing IBM Db2 system driver (ibm_db)"
# ─────────────────────────────────────────────────────────────────────────────
# ibm_db needs system-level C headers on Linux.
# On macOS/Windows the pypi wheel is usually self-contained.
OS=$(uname -s)

if [[ "$OS" == "Linux" ]]; then
  info "Linux detected — checking for required build tools"
  if command -v apt-get &>/dev/null; then
    info "Installing build-essential and libxml2-dev (requires sudo)"
    sudo apt-get install -y --quiet build-essential libxml2-dev libpython3-dev 2>/dev/null || warn "apt-get failed — continuing anyway"
  elif command -v yum &>/dev/null; then
    info "Installing gcc and python3-devel (requires sudo)"
    sudo yum install -y gcc python3-devel libxml2-devel 2>/dev/null || warn "yum failed — continuing anyway"
  else
    warn "Cannot detect package manager — skipping system libs. If ibm_db fails to compile, install gcc and python3-dev manually."
  fi
fi

info "Installing ibm_db and ibm_db_sa..."
pip install --quiet "ibm_db>=3.2.3" "ibm_db_sa>=0.4.0"
info "ibm_db ✓"

# ─────────────────────────────────────────────────────────────────────────────
section "4 / 6 — Installing AI frameworks (Haystack, LangChain, CrewAI)"
# ─────────────────────────────────────────────────────────────────────────────
info "Installing Haystack + IBM Db2 integration..."
pip install --quiet "haystack-ai>=2.6.0" "db2-haystack>=0.2.0"
info "Haystack ✓"

info "Installing LangChain + IBM Db2 integration + Ollama connector..."
pip install --quiet \
  "langchain>=0.3.0" \
  "langchain-community>=0.3.0" \
  "langchain-ollama>=0.2.0"
info "LangChain ✓"

info "Installing CrewAI..."
pip install --quiet "crewai>=0.80.0" "crewai-tools>=0.14.0"
info "CrewAI ✓"

# ─────────────────────────────────────────────────────────────────────────────
section "5 / 6 — Installing remaining dependencies"
# ─────────────────────────────────────────────────────────────────────────────
pip install --quiet -r requirements.txt
info "All Python dependencies installed ✓"

# ─────────────────────────────────────────────────────────────────────────────
section "6 / 6 — Checking Ollama + Granite model"
# ─────────────────────────────────────────────────────────────────────────────
if command -v ollama &>/dev/null; then
  info "Ollama found ✓"

  info "Pulling granite3.1-dense:8b (this may take a few minutes the first time)..."
  ollama pull granite3.1-dense:8b && info "granite3.1-dense:8b ✓" || warn "ollama pull failed — run 'ollama pull granite3.1-dense:8b' manually"

  info "Pulling nomic-embed-text (embedding model)..."
  ollama pull nomic-embed-text && info "nomic-embed-text ✓" || warn "ollama pull nomic-embed-text failed — run manually"
else
  warn "Ollama is NOT installed."
  warn "Install it from https://ollama.com and then run:"
  warn "  ollama pull granite3.1-dense:8b"
  warn "  ollama pull nomic-embed-text"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Environment file
# ─────────────────────────────────────────────────────────────────────────────
if [[ ! -f ".env" ]]; then
  cp .env.example .env
  warn ".env created from .env.example — EDIT IT with your Db2 credentials before running any use case"
else
  info ".env already exists"
fi

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}  Installation complete!${RESET}"
echo -e "${GREEN}${BOLD}════════════════════════════════════════════════${RESET}"
echo ""
echo "  Next steps:"
echo "    1. Edit .env with your IBM Db2 credentials"
echo "    2. Make sure Ollama is running:  ollama serve"
echo "    3. Start with Wave 1:"
echo "       cd 01_enterprise_knowledge_rag && python main.py"
echo ""
echo "  To activate the virtual environment in future sessions:"
echo "    source .venv/bin/activate"
echo ""
