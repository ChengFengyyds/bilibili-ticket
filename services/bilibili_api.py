"""B站API服务模块"""
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
        """获取票务信息"""
        try:
            url = f"{Config.BILIBILI_BASE_URL}/api/ticket/v2/get"
            params = {'event_id': event_id}
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

    def get_seat_list(self, event_id: str) -> Optional[List[Dict]]:
        """获取座位列表"""
        try:
            url = f"{Config.BILIBILI_BASE_URL}/api/ticket/v2/seat/list"
            params = {'event_id': event_id}
            response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                return None
        except Exception as e:
            print(f"获取座位列表异常: {e}")
            return None

    def grab_ticket(self, event_id: str, seat_id: str, quantity: int = 1) -> Dict:
        """抢票"""
        try:
            url = f"{Config.BILIBILI_BASE_URL}/api/ticket/v2/grab"
            data = {
                'event_id': event_id,
                'seat_id': seat_id,
                'quantity': quantity
            }
            response = self.session.post(url, json=data, timeout=Config.TIMEOUT)
            response.raise_for_status()
            result = response.json()

            return {
                'success': result.get('code') == 0,
                'message': result.get('message', ''),
                'data': result.get('data')
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'抢票异常: {str(e)}',
                'data': None
            }

    def check_order(self, order_id: str) -> Optional[Dict]:
        """查询订单状态"""
        try:
            url = f"{Config.BILIBILI_API_BASE}/v1/order/info"
            params = {'order_id': order_id}
            response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
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

    def auto_grab_ticket(self, event_id: str, preferred_seats: List[str] = None,
                         max_retry: int = None, interval: float = None,
                         callback=None) -> Dict:
        """
        自动抢票主逻辑
        :param event_id: 活动ID
        :param preferred_seats: 优先座位ID列表
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

            if ticket_info.get('status') == 'sold_out':
                if callback:
                    callback("票已售罄，继续监控...")
                time.sleep(interval)
                continue

            if ticket_info.get('status') == 'available':
                if callback:
                    callback("检测到有票！开始抢票...")

                if preferred_seats:
                    for seat_id in preferred_seats:
                        result = self.grab_ticket(event_id, seat_id)
                        if result['success']:
                            if callback:
                                callback(f"抢票成功！座位ID: {seat_id}")
                            return result
                else:
                    seat_list = self.get_seat_list(event_id)
                    if seat_list:
                        for seat in seat_list:
                            if seat.get('available'):
                                seat_id = seat.get('id')
                                result = self.grab_ticket(event_id, seat_id)
                                if result['success']:
                                    if callback:
                                        callback(f"抢票成功！座位ID: {seat_id}")
                                    return result

            time.sleep(interval)

        return {
            'success': False,
            'message': f'已达到最大重试次数 ({max_retry})',
            'data': None
        }
