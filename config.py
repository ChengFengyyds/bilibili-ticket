"""配置文件"""
import os

class Config:
    """应用配置"""
    APP_NAME = "B站抢票工具 - VCTCN上海站"
    VERSION = "1.0.0"

    # B站相关配置
    BILIBILI_BASE_URL = "https://show.bilibili.com"
    BILIBILI_API_BASE = "https://api.bilibili.com"

    # 票务配置 - VCTCN上海站
    VCTCN_SHANGHAI = {
        "name": "VCTCN 2025 上海站",
        "event_id": "vctcn_2025_shanghai",  # 实际使用时需要替换为真实活动ID
        "description": "Valorant冠军巡回赛中国联赛2025上海站",
        "date": "2025年9月",
        "venue": "上海"
    }

    # 抢票配置
    GRAB_INTERVAL = 0.5  # 抢票轮询间隔（秒）
    MONITOR_INTERVAL = 5  # 监控轮询间隔（秒）
    MAX_RETRY = 100  # 最大重试次数
    TIMEOUT = 30  # 请求超时（秒）

    # 用户数据目录
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".bilibili-ticket")
    COOKIE_FILE = os.path.join(DATA_DIR, "cookies.json")
    LOG_FILE = os.path.join(DATA_DIR, "ticket.log")

    # UI配置
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    THEME_COLOR = "#00A1D6"  # B站主题色
