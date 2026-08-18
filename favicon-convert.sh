#!/usr/bin/env bash
set -euo pipefail

SRC="base-favicon.png"
OUT="favicons"

mkdir -p "$OUT"

# Normalize source onto a square transparent 1024x1024 canvas.
# This avoids distortion if the source isn't perfectly square.
magick "$SRC" \
  -filter Lanczos \
  -resize 1024x1024 \
  -background none \
  -gravity center \
  -extent 1024x1024 \
  -strip \
  "$OUT/master.png"

# Standard browser favicons
magick "$OUT/master.png" -resize 16x16   "$OUT/favicon-16x16.png"
magick "$OUT/master.png" -resize 32x32   "$OUT/favicon-32x32.png"
magick "$OUT/master.png" -resize 48x48   "$OUT/favicon-48x48.png"

# Apple / iPhone / iPad home screen
magick "$OUT/master.png" -resize 180x180 "$OUT/apple-touch-icon.png"

# Android / Chrome / PWA
magick "$OUT/master.png" -resize 192x192 "$OUT/android-chrome-192x192.png"
magick "$OUT/master.png" -resize 512x512 "$OUT/android-chrome-512x512.png"

# Optional additional sizes useful for shortcuts / various platforms
magick "$OUT/master.png" -resize 96x96   "$OUT/favicon-96x96.png"
magick "$OUT/master.png" -resize 256x256 "$OUT/favicon-256x256.png"
magick "$OUT/master.png" -resize 384x384 "$OUT/favicon-384x384.png"

# Multi-resolution classic favicon.ico
magick \
  "$OUT/favicon-16x16.png" \
  "$OUT/favicon-32x32.png" \
  "$OUT/favicon-48x48.png" \
  "$OUT/favicon.ico"

# Remove intermediate master
rm "$OUT/master.png"
