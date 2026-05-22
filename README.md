# Bilibili 抢票工具 - VCTCN 上海九月比赛

一个用于自动抢 bilibili VCTCN 上海九月比赛门票的桌面应用。

## ⚠️ 重要说明

这是一个 **PyQt5 GUI 桌面应用**，需要在有图形界面的环境中运行：

- ✅ **推荐**：Windows/Mac/Linux 本地安装 Python 运行
- ⚠️ **GitHub Codespaces**：仅支持命令行模式，无法运行图形界面
- ✅ **Docker**：可在本地构建 Docker 镜像运行（需要 X11 转发）

## 🚀 GitHub Codespaces 使用方法

### 启动 Codespaces

1. 访问你的 GitHub 仓库：https://github.com/ChengFengyyds/bilibili-ticket
2. 点击 **Code** 按钮
3. 切换到 **Codespaces** 标签
4. 点击 **Create codespace on main**
5. 等待环境配置完成（约 2-3 分钟）

### 在 Codespaces 中运行

由于这是 GUI 应用，Codespaces 仅支持命令行模式：

```bash
# 查看帮助信息
python test_api.py

# 运行 Cookie 获取工具（需要浏览器）
python get_cookie.py

# 查看配置文件
cat config.py
```

### 编辑代码

Codespaces 提供了完整的 VS Code 编辑器，你可以在浏览器中：
- 查看和编辑代码
- 调试程序
- 使用终端
- 安装扩展

## 💻 本地运行（推荐）

如果你想在本地运行完整的 GUI 应用：

### 1. 安装 Python

**Windows:**
- 下载 Python 3.11+：https://www.python.org/downloads/
- 安装时勾选 ✅ "Add Python to PATH"

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. 克隆项目

```bash
git clone https://github.com/ChengFengyyds/bilibili-ticket.git
cd bilibili-ticket
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
python main.py
```

## 📁 项目结构

```
bilibili-ticket/
├── main.py                 # 应用入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖列表
├── core/
│   └── auto_grabber.py    # 自动抢票核心逻辑
├── services/
│   ├── bilibili_api.py    # Bilibili API 接口
│   ├── cookie_manager.py   # Cookie 管理
│   └── ticket_monitor.py   # 票务监控服务
├── ui/
│   └── main_window.py     # PyQt5 主窗口
├── utils/
│   └── logger.py          # 日志工具
├── get_cookie.py          # Cookie 获取工具
└── test_api.py            # API 测试脚本
```

## 🔧 配置说明

在 `config.py` 中修改以下配置：

```python
# 事件ID（从 bilibili 票务页面获取）
EVENT_ID = "your_event_id_here"

# Cookie 文件路径
COOKIE_FILE = "cookies.json"

# 轮询间隔（秒）
POLL_INTERVAL = 3

# 自动抢票间隔（秒）
GRAB_INTERVAL = 0.1
```

## 📝 使用步骤

1. **获取 Cookie**
   - 运行 `python get_cookie.py`
   - 使用 Selenium 打开浏览器登录 bilibili
   - 自动保存 Cookie 到 `cookies.json`

2. **配置 Event ID**
   - 在 bilibili 票务页面找到活动 ID
   - 修改 `config.py` 中的 `EVENT_ID`

3. **运行应用**
   - 运行 `python main.py`
   - 登录 bilibili 账号
   - 启动监控和抢票功能

## ⚠️ 注意事项

- 请确保 Cookie 有效且未过期
- 抢票成功与否取决于网络和服务器响应
- 请遵守 bilibili 平台规则，不要频繁请求
- 此工具仅供学习交流使用

## 📜 License

MIT License
