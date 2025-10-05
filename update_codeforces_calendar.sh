#!/bin/bash
# Regenerate the Codeforces calendar ICS and open it in Calendar (macOS).

set -euo pipefail

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

python3 contest_calendar.py \
  --platforms codeforces \
  --reminder 10 \
  --output codeforces_contests.ics \
  --quiet

open "$SCRIPT_DIR/codeforces_contests.ics"
