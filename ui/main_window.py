"""主窗口UI"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QLineEdit,
                             QGroupBox, QMessageBox, QProgressBar, QStatusBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from services.bilibili_api import BilibiliAPI
from services.cookie_manager import CookieManager
from core.auto_grabber import AutoGrabber
from config import Config
from utils.logger import get_logger


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.api = BilibiliAPI()
        self.cookie_manager = CookieManager(self.api)
        self.grabber = AutoGrabber(self.api)
        self.logger = get_logger()

        self.init_ui()
        self.load_cookies()
        self.setup_connections()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.VERSION}")
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.create_header(main_layout)
        self.create_login_section(main_layout)
        self.create_event_section(main_layout)
        self.create_control_section(main_layout)
        self.create_log_section(main_layout)
        self.create_status_bar()

    def create_header(self, parent_layout):
        """创建标题区域"""
        header_group = QGroupBox()
        header_layout = QVBoxLayout()
        header_group.setLayout(header_layout)

        title = QLabel("🎮 B站抢票工具 - VCTCN上海站")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("自动监控并抢票 · 支持B站大型活动")
        subtitle.setFont(QFont("Microsoft YaHei", 10))
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        parent_layout.addWidget(header_group)

    def create_login_section(self, parent_layout):
        """创建登录区域"""
        login_group = QGroupBox("登录状态")
        login_layout = QVBoxLayout()
        login_group.setLayout(login_layout)

        self.login_status_label = QLabel("❌ 未登录")
        self.login_status_label.setFont(QFont("Microsoft YaHei", 10))

        login_btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("🔐 登录B站")
        self.logout_btn = QPushButton("退出登录")
        self.logout_btn.setEnabled(False)
        self.refresh_btn = QPushButton("🔄 刷新状态")

        login_btn_layout.addWidget(self.login_btn)
        login_btn_layout.addWidget(self.logout_btn)
        login_btn_layout.addWidget(self.refresh_btn)
        login_btn_layout.addStretch()

        login_layout.addWidget(self.login_status_label)
        login_layout.addLayout(login_btn_layout)
        parent_layout.addWidget(login_group)

    def create_event_section(self, parent_layout):
        """创建活动信息区域"""
        event_group = QGroupBox("活动信息")
        event_layout = QVBoxLayout()
        event_group.setLayout(event_layout)

        self.event_name_label = QLabel(f"📅 {Config.VCTCN_SHANGHAI['name']}")
        self.event_name_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))

        self.event_info_label = QLabel(
            f"📍 地点: {Config.VCTCN_SHANGHAI['venue']} | "
            f"🗓️ 时间: {Config.VCTCN_SHANGHAI['date']}"
        )

        event_id_layout = QHBoxLayout()
        event_id_layout.addWidget(QLabel("活动ID:"))
        self.event_id_input = QLineEdit()
        self.event_id_input.setPlaceholderText("请输入B站活动ID")
        self.event_id_input.setText(Config.VCTCN_SHANGHAI['event_id'])
        event_id_layout.addWidget(self.event_id_input)

        event_layout.addWidget(self.event_name_label)
        event_layout.addWidget(self.event_info_label)
        event_layout.addLayout(event_id_layout)
        parent_layout.addWidget(event_group)

    def create_control_section(self, parent_layout):
        """创建控制区域"""
        control_group = QGroupBox("抢票控制")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)

        self.start_btn = QPushButton("🚀 开始自动抢票")
        self.start_btn.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00A1D6;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00B5E5;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)

        self.stop_btn = QPushButton("⏹️ 停止抢票")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #F45D5D;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
            }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        control_layout.addLayout(btn_layout)
        control_layout.addWidget(self.progress_bar)
        parent_layout.addWidget(control_group)

    def create_log_section(self, parent_layout):
        """创建日志区域"""
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setMaximumHeight(200)

        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.clicked.connect(self.log_text.clear)

        log_layout.addWidget(self.log_text)
        log_layout.addWidget(clear_log_btn)
        parent_layout.addWidget(log_group)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def setup_connections(self):
        """设置信号连接"""
        self.login_btn.clicked.connect(self.on_login)
        self.logout_btn.clicked.connect(self.on_logout)
        self.refresh_btn.clicked.connect(self.refresh_login_status)
        self.start_btn.clicked.connect(self.on_start_grab)
        self.stop_btn.clicked.connect(self.on_stop_grab)

    def load_cookies(self):
        """加载Cookie"""
        if self.cookie_manager.load():
            self.refresh_login_status()

    def refresh_login_status(self):
        """刷新登录状态"""
        if self.cookie_manager.is_valid():
            user_info = self.api.get_user_info()
            if user_info:
                uname = user_info.get('uname', '未知用户')
                self.login_status_label.setText(f"✅ 已登录: {uname}")
                self.login_btn.setEnabled(False)
                self.logout_btn.setEnabled(True)
                self.start_btn.setEnabled(True)
                self.log(f"用户 {uname} 已登录")
                self.status_bar.showMessage(f"已登录: {uname}")
            else:
                self.login_status_label.setText("❌ 登录已过期")
                self.login_btn.setEnabled(True)
                self.log("登录已过期，请重新登录")
        else:
            self.login_status_label.setText("❌ 未登录")
            self.login_btn.setEnabled(True)
            self.logout_btn.setEnabled(False)
            self.start_btn.setEnabled(False)

    def on_login(self):
        """登录处理"""
        from PyQt5.QtWidgets import QFileDialog
        from PyQt5.QtCore import QSettings

        cookie_file, _ = QFileDialog.getOpenFileName(
            self,
            "选择Cookie文件",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if cookie_file:
            if self.api.load_cookies(cookie_file):
                self.cookie_manager.save()
                self.refresh_login_status()
                QMessageBox.information(self, "成功", "登录成功！")
            else:
                QMessageBox.warning(self, "失败", "Cookie加载失败，请检查文件格式")

    def on_logout(self):
        """退出登录"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要退出登录吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cookie_manager.clear()
            self.refresh_login_status()
            QMessageBox.information(self, "成功", "已退出登录")

    def on_start_grab(self):
        """开始抢票"""
        event_id = self.event_id_input.text().strip()

        if not event_id:
            QMessageBox.warning(self, "错误", "请输入活动ID")
            return

        if not self.cookie_manager.is_valid():
            QMessageBox.warning(self, "错误", "请先登录B站账号")
            return

        self.log("=" * 50)
        self.log("🚀 开始自动抢票")
        self.log(f"活动ID: {event_id}")

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.event_id_input.setEnabled(False)
        self.status_bar.showMessage("正在抢票...")

        self.grabber.start(
            event_id=event_id,
            status_callback=self.log,
            success_callback=self.on_grab_success
        )

    def on_stop_grab(self):
        """停止抢票"""
        self.grabber.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.event_id_input.setEnabled(True)
        self.status_bar.showMessage("已停止")
        self.log("⏹️ 已停止自动抢票")

    def on_grab_success(self, result):
        """抢票成功回调"""
        self.log("🎉🎉🎉 抢票成功！！！ 🎉🎉🎉")
        self.log(f"详情: {result.get('message', '')}")

        QMessageBox.information(
            self,
            "🎉 抢票成功",
            f"恭喜！您已成功抢到票！\n{result.get('message', '')}\n\n请在B站APP中完成支付。"
        )

        self.on_stop_grab()

    def log(self, message: str):
        """添加日志"""
        self.log_text.append(message)
        self.logger.info(message)

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.grabber.is_running:
            self.grabber.stop()
        event.accept()
