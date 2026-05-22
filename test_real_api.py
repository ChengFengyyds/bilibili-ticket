import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

# 测试真实的 API
url = "https://show.bilibili.com/api/ticket/project/getV2"
params = {
    'version': '134',
    'id': '1001074',
    'project_id': '1001074',
    'requestSource': 'pc-new'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://show.bilibili.com/platform/detail.html?id=1001074&from=pc_ticketlist&msource=pc_web',
    'Origin': 'https://show.bilibili.com'
}

try:
    print("Testing real Bilibili ticket API...")
    response = requests.get(url, params=params, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess! Response data:")
        print(f"Code: {data.get('code')}")
        print(f"Message: {data.get('message')}")
        
        if data.get('code') == 0:
            project_data = data.get('data')
            print(f"\nProject Data:")
            print(f"  Project Name: {project_data.get('name', 'N/A')}")
            print(f"  Project ID: {project_data.get('id', 'N/A')}")
            print(f"  Status: {project_data.get('status', 'N/A')}")
            print(f"  Venue: {project_data.get('venue_name', 'N/A')}")
            
            # 检查是否有票档
            screen_list = project_data.get('screen_list', [])
            if screen_list:
                print(f"\n  Ticket Screen Count: {len(screen_list)}")
                for i, screen in enumerate(screen_list[:3]):
                    print(f"    Screen {i+1}: {screen.get('name', 'N/A')}")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
