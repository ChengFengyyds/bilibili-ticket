"""日志工具"""
import logging
import os
from datetime import datetime
from config import Config


class Logger:
    """日志管理器"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        """初始化日志器"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)

        self.logger = logging.getLogger('BilibiliTicket')
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(
            Config.LOG_FILE,
            encoding='utf-8',
            mode='a'
        )
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """记录信息"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录错误"""
        self.logger.error(message)

    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)


def get_logger() -> Logger:
    """获取日志实例"""
    return Logger()
