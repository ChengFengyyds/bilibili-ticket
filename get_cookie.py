"""Cookie获取辅助工具

使用浏览器自动化获取B站Cookie
需要安装 selenium 和 webdriver
"""

import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config import Config


class CookieGetter:
    """Cookie获取器"""

    def __init__(self):
        self.driver = None

    def setup_driver(self):
        """设置浏览器驱动"""
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_cookies(self):
        """获取B站Cookie"""
        try:
            self.setup_driver()

            print("正在打开B站登录页面...")
            self.driver.get("https://passport.bilibili.com/login")

            input("请在浏览器中完成登录，然后按回车键继续...")

            cookies = {}
            for cookie in self.driver.cookies:
                cookies[cookie['name']] = cookie['value']

            print(f"\n成功获取 {len(cookies)} 个Cookie")

            os.makedirs(Config.DATA_DIR, exist_ok=True)
            with open(Config.COOKIE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)

            print(f"Cookie已保存到: {Config.COOKIE_FILE}")
            return True

        except Exception as e:
            print(f"获取Cookie失败: {e}")
            return False

        finally:
            if self.driver:
                self.driver.quit()


def main():
    """主函数"""
    print("=" * 60)
    print("B站Cookie获取工具")
    print("=" * 60)
    print("\n此工具将打开浏览器让您登录B站")
    print("请确保已安装Chrome浏览器和selenium\n")

    getter = CookieGetter()
    if getter.get_cookies():
        print("\n✅ Cookie获取成功！")
        print("现在可以运行主程序了：python main.py")
    else:
        print("\n❌ Cookie获取失败")


if __name__ == '__main__':
    main()
