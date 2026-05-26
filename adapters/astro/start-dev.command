#!/usr/bin/env bash
#
# Double-click this file to start the Astro dev server.
# Site will open at  http://localhost:4321
#
# Run from the directory this script lives in (the Astro adapter root),
# regardless of where it was launched from.
#

set -e
cd "$(dirname "$0")"

echo "==============================================================="
echo "  Ağustos Design System — local dev"
echo "  Project: $(pwd)"
echo "==============================================================="
echo ""

# Check Node is available
if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node.js is not installed."
  echo "   Install it from https://nodejs.org (the LTS version is fine)"
  echo "   then double-click this file again."
  echo ""
  read -p "Press Return to close…"
  exit 1
fi

echo "→ Node $(node --version)"
echo "→ npm  $(npm --version)"
echo ""

# Install dependencies if node_modules is missing or stale
if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ]; then
  echo "→ Installing dependencies (one-time, ~30s)…"
  npm install --no-audit --no-fund
  echo ""
fi

echo "→ Starting dev server…"
echo "  Open  http://localhost:4321  in your browser when ready."
echo "  Press Ctrl-C in this window to stop."
echo ""

# Open the URL in the default browser ~2 seconds after the server boots
( sleep 2 && open "http://localhost:4321" ) &

# Hand control to Astro
exec npm run dev
