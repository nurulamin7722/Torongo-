#!/usr/bin/env python3
"""
Generate M3U playlist from Torongo+ database
"""
import json
import os

def generate_m3u():
    """Generate M3U playlist from data.json"""
    
    # Check if data.json exists
    if not os.path.exists('data.json'):
        print("Error: data.json not found")
        return
    
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in data.json")
        return
    except Exception as e:
        print(f"Error reading data.json: {e}")
        return
    
    # Generate M3U content
    m3u_content = "#EXTM3U\n"
    
    # Process data based on structure
    if isinstance(data, dict):
        items = data.get('items', [])
    elif isinstance(data, list):
        items = data
    else:
        print("Error: Unexpected data format")
        return
    
    for item in items:
        if isinstance(item, dict):
            name = item.get('name', 'Unknown')
            url = item.get('url', '')
            tvg_id = item.get('tvg_id', '')
            tvg_name = item.get('tvg_name', name)
            logo = item.get('logo', '')
            
            if url:
                # Format: #EXTINF with metadata
                extinf = f'#EXTINF:-1'
                if tvg_id:
                    extinf += f' tvg-id="{tvg_id}"'
                if logo:
                    extinf += f' tvg-logo="{logo}"'
                if tvg_name:
                    extinf += f' tvg-name="{tvg_name}"'
                extinf += f',{name}'
                
                m3u_content += extinf + '\n'
                m3u_content += url + '\n'
    
    # Write M3U file
    try:
        with open('torongo_plus.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        print(f"✓ Successfully generated torongo_plus.m3u with {len(items)} items")
    except Exception as e:
        print(f"Error writing M3U file: {e}")

if __name__ == '__main__':
    generate_m3u()
