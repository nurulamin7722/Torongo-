import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

m3u = "#EXTM3U\n"

channels = data.get("channels", [])
print(f"Processing {len(channels)} channels")

for ch in channels:
    name = ch.get("name", "No Name")
    url = ch.get("url", "")
    logo = ch.get("logo", "")

    if url:  # Only add if URL exists
        m3u += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n'
        print(f"Added: {name}")

with open("torongo_plus.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print(f"M3U generated successfully with {len(channels)} channels!")
print(f"M3U file size: {len(m3u)} bytes")