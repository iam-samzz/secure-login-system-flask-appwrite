#!/usr/bin/env bash
# POSIX/Linux launcher: starts a Python HTTP server and opens index.html
# Usage: double-click or run from a terminal. Attempts to open the default browser.
cd "$(dirname "$0")"
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo "Python not found. Please install Python 3."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi
PORT=8000
URL="http://localhost:$PORT/index.html"
# Determine open command
if command -v xdg-open >/dev/null 2>&1; then
  OPEN_CMD="xdg-open"
elif command -v gnome-open >/dev/null 2>&1; then
  OPEN_CMD="gnome-open"
elif command -v open >/dev/null 2>&1; then
  OPEN_CMD="open"
else
  OPEN_CMD=""
fi
# Start server in foreground
echo "Starting Python HTTP server on http://localhost:$PORT (press Ctrl+C to stop)"
# Open browser shortly after starting server
if [ -n "$OPEN_CMD" ]; then
  ( sleep 0.8; "$OPEN_CMD" "$URL" ) &
else
  echo "No known open command found (xdg-open/open). Please open $URL manually in a browser."
fi
exec "$PYTHON" -m http.server "$PORT" --bind 127.0.0.1
