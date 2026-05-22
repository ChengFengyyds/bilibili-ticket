"""B站API服务模块 - 使用真实的 Bilibili 会员购票务 API"""
import requests
import json
import time
from typing import Dict, Optional, List
from config import Config


class BilibiliAPI:
    """B站API交互类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': Config.BILIBILI_BASE_URL,
            'Origin': Config.BILIBILI_BASE_URL
        })
        self.cookies = {}

    def load_cookies(self, cookies_file: str) -> bool:
        """加载Cookies"""
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies_dict = json.load(f)
                self.cookies = cookies_dict
                for key, value in cookies_dict.items():
                    self.session.cookies.set(key, value)
            return True
        except Exception as e:
            print(f"加载Cookies失败: {e}")
            return False

    def save_cookies(self, cookies_file: str) -> bool:
        """保存Cookies"""
        try:
            cookies_dict = {cookie.name: cookie.value for cookie in self.session.cookies}
            with open(cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies_dict, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存Cookies失败: {e}")
            return False

    def get_ticket_info(self, event_id: str) -> Optional[Dict]:
        """获取票务信息 - 使用真实的 Bilibili API"""
        try:
            url = f"{Config.BILIBILI_BASE_URL}/api/ticket/project/getV2"
            params = {
                'version': '134',
                'id': event_id,
                'project_id': event_id,
                'requestSource': 'pc-new'
            }
            response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 0:
                return data.get('data')
            else:
                print(f"获取票务信息失败: {data.get('message', '未知错误')}")
                return None
        except Exception as e:
            print(f"获取票务信息异常: {e}")
            return None

    def get_screen_list(self, event_id: str) -> List[Dict]:
        """获取场次/票档列表"""
        try:
            project_data = self.get_ticket_info(event_id)
            if project_data:
                return project_data.get('screen_list', [])
            return []
        except Exception as e:
            print(f"获取场次列表异常: {e}")
            return []

    def get_seat_list(self, event_id: str, screen_id: Optional[str] = None) -> Optional[List[Dict]]:
        """获取座位列表"""
        try:
            # 实际上 Bilibili 的座位信息通常在 screen_list 中
            screen_list = self.get_screen_list(event_id)
            if screen_list:
                return screen_list
            return None
        except Exception as e:
            print(f"获取座位列表异常: {e}")
            return None

    def grab_ticket(self, event_id: str, screen_id: str, quantity: int = 1) -> Dict:
        """抢票 - 占位实现，需要真实 API"""
        # 注意：实际抢票需要登录和复杂的交互，这里提供基础框架
        return {
            'success': False,
            'message': '需要完整的登录和交互流程',
            'data': None
        }

    def check_order(self, order_id: str) -> Optional[Dict]:
        """查询订单状态"""
        try:
            url = f"{Config.BILIBILI_API_BASE}/x/web-interface/nav"
            response = self.session.get(url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 0:
                return data.get('data')
            return None
        except Exception as e:
            print(f"查询订单异常: {e}")
            return None

    def get_user_info(self) -> Optional[Dict]:
        """获取用户信息"""
        try:
            url = f"{Config.BILIBILI_API_BASE}/x/web-interface/nav"
            response = self.session.get(url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 0:
                return data.get('data')
            return None
        except Exception as e:
            print(f"获取用户信息异常: {e}")
            return None

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        user_info = self.get_user_info()
        return user_info is not None and user_info.get('isLogin', False)

    def auto_grab_ticket(self, event_id: str, preferred_screens: List[str] = None,
                         max_retry: int = None, interval: float = None,
                         callback=None) -> Dict:
        """
        自动抢票主逻辑
        :param event_id: 活动ID
        :param preferred_screens: 优先票档/场次名称列表
        :param max_retry: 最大重试次数
        :param interval: 抢票间隔
        :param callback: 状态回调函数
        """
        max_retry = max_retry or Config.MAX_RETRY
        interval = interval or Config.GRAB_INTERVAL

        for attempt in range(max_retry):
            if callback:
                callback(f"第 {attempt + 1} 次尝试抢票...")

            ticket_info = self.get_ticket_info(event_id)
            if not ticket_info:
                time.sleep(interval)
                continue

            status = ticket_info.get('status')
            
            # 获取票档列表
            screen_list = ticket_info.get('screen_list', [])
            
            if not screen_list:
                time.sleep(interval)
                continue

            available_screens = []
            for screen in screen_list:
                # 检查是否有可售的票档
                if screen.get('sale_flag') == 1:
                    available_screens.append(screen)

            if available_screens:
                if callback:
                    callback(f"发现 {len(available_screens)} 个可售场次...")

                # 优先选择用户指定的票档
                target_screen = None
                if preferred_screens:
                    for pref_screen_name in preferred_screens:
                        for screen in available_screens:
                            if pref_screen_name in screen.get('name', ''):
                                target_screen = screen
                                break
                        if target_screen:
                            break

                if not target_screen:
                    # 如果没有匹配的，选第一个可售的
                    target_screen = available_screens[0]

                if target_screen:
                    if callback:
                        callback(f"选择场次: {target_screen.get('name')}")
                    
                    # 这里需要完整的抢票流程
                    return {
                        'success': False,
                        'message': '发现可售票档，需要完整的登录和交互流程',
                        'data': target_screen
                    }

            time.sleep(interval)

        return {
            'success': False,
            'message': f'已达到最大重试次数 ({max_retry})',
            'data': None
        }
