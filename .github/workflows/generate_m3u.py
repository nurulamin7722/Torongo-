import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

m3u = "#EXTM3U\n"

for ch in data.get("channels", []):
    name = ch.get("name", "No Name")
    url = ch.get("url", "")
    logo = ch.get("logo", "")

    m3u += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n'

with open("torongo_plus.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("M3U generated successfully!")