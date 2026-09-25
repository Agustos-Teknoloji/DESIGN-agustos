#!/usr/bin/env bash
# The local gate. The one list of checks that must pass before a push.
#
# .githooks/pre-push runs this file. Run it by hand at any time:
#   scripts/ci.sh
#
# The checks use Python 3.12 or newer. Set PYTHON to choose an interpreter.
# Otherwise the script uses python3 if it is new enough, then the
# python@3.12 install of mise. It installs nothing.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

is_new_enough() {
  "$1" -c 'import sys; sys.exit(sys.version_info < (3, 12))' 2>/dev/null
}

if [ -n "${PYTHON:-}" ]; then
  py="$PYTHON"
elif is_new_enough python3; then
  py="python3"
elif command -v mise >/dev/null 2>&1 && mise_dir="$(mise where python@3.12 2>/dev/null)"; then
  py="$mise_dir/bin/python3"
else
  echo "scripts/ci.sh: Python 3.12 or newer is required." >&2
  echo "Install it with 'mise install python@3.12', or set PYTHON=/path/to/python3.12." >&2
  exit 1
fi

if ! is_new_enough "$py"; then
  echo "scripts/ci.sh: $py is older than Python 3.12." >&2
  exit 1
fi

echo "Python: $("$py" --version 2>&1) ($py)"

echo "==> Validate generated adapters"
"$py" scripts/build_design_system.py --check

echo "==> Validate generated Office artifacts"
"$py" scripts/check_office_artifacts.py --check

echo "==> Run design-system tests"
"$py" -m unittest discover -s tests
