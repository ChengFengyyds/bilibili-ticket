"""测试脚本 - 使用真实的 Bilibili API"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.bilibili_api import BilibiliAPI
from config import Config


def test_api_connection():
    """测试API连接"""
    print("=" * 60)
    print("B站API连接测试 - 真实 API")
    print("=" * 60)

    api = BilibiliAPI()

    print("\n1. 测试基础连接...")
    try:
        response = api.session.get(
            Config.BILIBILI_BASE_URL,
            timeout=Config.TIMEOUT
        )
        print(f"   ✅ 连接成功 (状态码: {response.status_code})")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return False

    print("\n2. 测试获取用户信息...")
    user_info = api.get_user_info()
    if user_info and user_info.get('isLogin'):
        print(f"   ✅ 已登录: {user_info.get('uname')}")
    else:
        print("   ⚠️ 未登录（这是正常的，如果没有Cookie的话）")

    print("\n3. 测试活动信息获取...")
    event_id = Config.VCTCN_SHANGHAI['event_id']
    print(f"   活动ID: {event_id}")

    ticket_info = api.get_ticket_info(event_id)
    if ticket_info:
        print(f"   ✅ 成功获取票务信息")
        print(f"   项目名称: {ticket_info.get('name')}")
        print(f"   项目状态: {ticket_info.get('status')}")
        
        screen_list = ticket_info.get('screen_list', [])
        if screen_list:
            print(f"   票档数量: {len(screen_list)}")
            for i, screen in enumerate(screen_list):
                sale_flag = screen.get('sale_flag', 0)
                status_text = "可售" if sale_flag == 1 else "不可售"
                print(f"    [{i+1}] {screen.get('name')} - {status_text}")
    else:
        print("   ⚠️ 无法获取票务信息")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

    return True


def main():
    """主函数"""
    test_api_connection()


if __name__ == '__main__':
    main()
