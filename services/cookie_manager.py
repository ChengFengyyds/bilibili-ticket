"""Cookie管理服务"""
import json
import os
from typing import Optional
from services.bilibili_api import BilibiliAPI
from config import Config


class CookieManager:
    """Cookie管理器"""

    def __init__(self, api: BilibiliAPI):
        self.api = api
        self.cookie_file = Config.COOKIE_FILE
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)

    def load(self) -> bool:
        """加载本地Cookie"""
        if not os.path.exists(self.cookie_file):
            return False
        return self.api.load_cookies(self.cookie_file)

    def save(self) -> bool:
        """保存当前Cookie到本地"""
        return self.api.save_cookies(self.cookie_file)

    def update(self, cookies_dict: dict) -> bool:
        """更新Cookie"""
        try:
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies_dict, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"更新Cookie失败: {e}")
            return False

    def clear(self):
        """清除Cookie"""
        try:
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
            return True
        except Exception:
            return False

    def is_valid(self) -> bool:
        """检查Cookie是否有效"""
        return self.api.is_logged_in()
