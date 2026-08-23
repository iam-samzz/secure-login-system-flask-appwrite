#!/bin/bash
# macOS double-clickable launcher: starts a Python HTTP server and opens index.html
# Made to be double-clickable (.command) — Terminal will open and run this script.
cd "$(dirname "$0")"
# Prefer python3, fallback to python
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo "Python not found. Please install Python 3."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi
PORT=8000
URL="http://localhost:$PORT/index.html"
# Start server in foreground so terminal stays open and shows logs
echo "Starting Python HTTP server on http://localhost:$PORT (press Ctrl+C to stop)"
# Open browser after a short delay to ensure server has started
( sleep 0.8; open "$URL" ) &
exec "$PYTHON" -m http.server "$PORT" --bind 127.0.0.1
