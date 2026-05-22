"""票务监控服务"""
import time
import threading
from typing import Dict, Callable, Optional
from services.bilibili_api import BilibiliAPI
from config import Config


class TicketMonitor:
    """票务监控类"""

    def __init__(self, api: BilibiliAPI):
        self.api = api
        self.is_monitoring = False
        self.monitor_thread = None
        self.callback = None

    def start_monitor(self, event_id: str, interval: float = None,
                      status_callback: Callable[[str], None] = None,
                      ticket_callback: Callable[[Dict], None] = None):
        """
        开始监控票务状态
        :param event_id: 活动ID
        :param interval: 监控间隔（秒）
        :param status_callback: 状态更新回调
        :param ticket_callback: 有票时的回调
        """
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.callback = status_callback
        interval = interval or Config.MONITOR_INTERVAL

        def monitor_task():
            last_status = None
            while self.is_monitoring:
                try:
                    ticket_info = self.api.get_ticket_info(event_id)

                    if ticket_info:
                        current_status = ticket_info.get('status', 'unknown')

                        if current_status != last_status:
                            if status_callback:
                                status_callback(self._format_status(ticket_info))
                            last_status = current_status

                        if current_status == 'available':
                            if ticket_callback:
                                ticket_callback(ticket_info)
                    else:
                        if status_callback:
                            status_callback("获取票务信息失败，5秒后重试...")

                except Exception as e:
                    if status_callback:
                        status_callback(f"监控异常: {str(e)}")

                time.sleep(interval)

        self.monitor_thread = threading.Thread(target=monitor_task, daemon=True)
        self.monitor_thread.start()

    def stop_monitor(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def get_current_status(self, event_id: str) -> Optional[Dict]:
        """获取当前票务状态"""
        return self.api.get_ticket_info(event_id)

    def _format_status(self, ticket_info: Dict) -> str:
        """格式化票务状态"""
        status = ticket_info.get('status', 'unknown')
        remaining = ticket_info.get('remaining', 0)
        sold = ticket_info.get('sold', 0)
        total = ticket_info.get('total', 0)

        status_map = {
            'available': '有票可售',
            'sold_out': '已售罄',
            'not_start': '未开始',
            'ended': '已结束',
            'unknown': '未知状态'
        }

        status_text = status_map.get(status, status)

        if status == 'available':
            return f"🎉 状态: {status_text} | 剩余: {remaining} 张 | 已售: {sold}/{total}"
        else:
            return f"📊 状态: {status_text} | 已售: {sold}/{total}"
