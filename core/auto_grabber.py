"""自动抢票核心模块"""
import time
import threading
from typing import List, Callable, Optional, Dict
from services.bilibili_api import BilibiliAPI
from services.ticket_monitor import TicketMonitor
from config import Config


class AutoGrabber:
    """自动抢票核心类"""

    def __init__(self, api: BilibiliAPI):
        self.api = api
        self.monitor = TicketMonitor(api)
        self.is_running = False
        self.grab_thread = None
        self.status_callback = None
        self.success_callback = None

    def start(self, event_id: str, preferred_seats: List[str] = None,
              status_callback: Callable[[str], None] = None,
              success_callback: Callable[[Dict], None] = None):
        """
        启动自动抢票
        :param event_id: 活动ID
        :param preferred_seats: 优先座位ID列表
        :param status_callback: 状态回调函数
        :param success_callback: 抢票成功回调
        """
        if self.is_running:
            return

        self.is_running = True
        self.status_callback = status_callback
        self.success_callback = success_callback

        def grab_task():
            self._update_status("开始监控票务状态...")

            self.monitor.start_monitor(
                event_id=event_id,
                status_callback=lambda msg: self._update_status(msg),
                ticket_callback=lambda info: self._handle_ticket_available(event_id, info, preferred_seats)
            )

        self.grab_thread = threading.Thread(target=grab_task, daemon=True)
        self.grab_thread.start()

    def stop(self):
        """停止自动抢票"""
        self.is_running = False
        self.monitor.stop_monitor()
        self._update_status("已停止自动抢票")

    def _update_status(self, message: str):
        """更新状态"""
        if self.status_callback:
            self.status_callback(message)

    def _handle_ticket_available(self, event_id: str, ticket_info: Dict,
                                 preferred_seats: List[str] = None):
        """处理有票的情况"""
        self._update_status("🎉 检测到有票！立即开始抢票...")

        result = self.api.auto_grab_ticket(
            event_id=event_id,
            preferred_seats=preferred_seats,
            callback=lambda msg: self._update_status(msg)
        )

        if result['success']:
            if self.success_callback:
                self.success_callback(result)
        else:
            self._update_status(f"抢票失败: {result['message']}")

    def grab_once(self, event_id: str, seat_id: str = None) -> Dict:
        """单次抢票"""
        self._update_status("执行单次抢票...")

        if seat_id:
            result = self.api.grab_ticket(event_id, seat_id)
        else:
            seat_list = self.api.get_seat_list(event_id)
            if seat_list:
                for seat in seat_list:
                    if seat.get('available'):
                        result = self.api.grab_ticket(event_id, seat['id'])
                        if result['success']:
                            break
            else:
                return {
                    'success': False,
                    'message': '无可用座位'
                }

        if result['success']:
            self._update_status(f"✅ {result['message']}")
        else:
            self._update_status(f"❌ {result['message']}")

        return result
