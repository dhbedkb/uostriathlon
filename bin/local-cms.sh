#!/usr/bin/env bash
set -e

echo "Starting Decap local backend proxy..."
echo "Run this from the repository root."
echo
echo "Terminal 1:"
echo "  npx decap-server"
echo
echo "Terminal 2:"
echo "  bundle exec jekyll serve"
echo
echo "Then open:"
echo "  http://127.0.0.1:4000/uostriathlon/admin/local.html"
echo
echo "If uploads show 404 filenames, decap-server is not running or is running from the wrong folder."
