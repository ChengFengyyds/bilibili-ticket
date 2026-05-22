#!/usr/bin/env python3
"""测试登录状态"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.bilibili_api import BilibiliAPI
from config import Config


def test_login_status():
    """测试登录状态"""
    print("=" * 60)
    print("测试 B站 登录状态")
    print("=" * 60)
    
    # 创建 API 实例
    api = BilibiliAPI()
    
    # 加载 Cookie
    print(f"\n1. 加载 Cookie 文件...")
    print(f"   文件路径: {Config.COOKIE_FILE}")
    
    if os.path.exists(Config.COOKIE_FILE):
        print(f"   ✅ Cookie 文件存在")
    else:
        print(f"   ❌ Cookie 文件不存在")
        return
    
    # 加载 Cookie
    if api.load_cookies(Config.COOKIE_FILE):
        print(f"   ✅ Cookie 加载成功")
        print(f"   共加载 {len(api.cookies)} 个 Cookie")
    else:
        print(f"   ❌ Cookie 加载失败")
        return
    
    # 测试登录
    print(f"\n2. 测试登录状态...")
    user_info = api.get_user_info()
    
    if user_info:
        is_login = user_info.get('isLogin', False)
        if is_login:
            print(f"   ✅ 登录成功！")
            print(f"   用户名: {user_info.get('uname')}")
            print(f"   UID: {user_info.get('mid')}")
            print(f"   VIP状态: {'是' if user_info.get('vipStatus') else '否'}")
            print(f"   会员等级: {user_info.get('level_info', {}).get('current_level', 0)}")
        else:
            print(f"   ❌ 未登录（Cookie 可能已过期）")
    else:
        print(f"   ❌ 无法获取用户信息")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    test_login_status()
