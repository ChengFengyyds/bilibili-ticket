"""测试脚本

用于测试B站API连接和基础功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.bilibili_api import BilibiliAPI
from config import Config


def test_api_connection():
    """测试API连接"""
    print("=" * 60)
    print("B站API连接测试")
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
        print(f"   状态: {ticket_info.get('status')}")
        print(f"   已售: {ticket_info.get('sold', 0)}/{ticket_info.get('total', 0)}")
    else:
        print("   ⚠️ 无法获取票务信息（可能是活动ID不正确或活动未开放）")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

    return True


def main():
    """主函数"""
    test_api_connection()


if __name__ == '__main__':
    main()
