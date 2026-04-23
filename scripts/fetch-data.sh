#!/bin/bash

# This script fetches channel data from API or falls back to cache

TIMESTAMP=$(date +%s%3N)
URL="https://api.ovation-bdofficial.workers.dev/database.json?nocache=$TIMESTAMP"
OUTPUT_FILE="data.json"
CACHE_FILE=".github/data-cache.json"

echo "Attempting to fetch from API: $URL"

# Try multiple times
for attempt in 1 2 3; do
    echo "Attempt $attempt..."
    
    curl -s -f \
        -H "Origin: https://torongoplus.vercel.app" \
        -H "Referer: https://torongoplus.vercel.app/" \
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
        --max-time 10 \
        "$URL" -o "$OUTPUT_FILE.tmp" 2>/dev/null
    
    if [ -s "$OUTPUT_FILE.tmp" ] && grep -q '"channels"' "$OUTPUT_FILE.tmp"; then
        echo "✓ Successfully fetched data from API"
        mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"
        exit 0
    fi
    
    echo "  Attempt $attempt failed, retrying..."
    sleep 2
done

echo "⚠ All API attempts failed, using cached data..."

if [ -f "$CACHE_FILE" ]; then
    cp "$CACHE_FILE" "$OUTPUT_FILE"
    echo "✓ Using cached data from $CACHE_FILE"
    
    if [ -s "$OUTPUT_FILE" ]; then
        CHANNELS=$(python3 -c "import json; print(len(json.load(open('$OUTPUT_FILE')).get('channels', [])))" 2>/dev/null || echo "0")
        echo "Channels available in cache: $CHANNELS"
        exit 0
    fi
fi

echo "ERROR: No data available (API failed and no cache found)"
rm -f "$OUTPUT_FILE.tmp"
exit 1
