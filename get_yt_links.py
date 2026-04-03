from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 目标频道
CHANNEL_URL = "https://www.youtube.com/@ronzmlbbofficial/videos"

# 浏览器配置
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

# 自动安装驱动 → 打开Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(CHANNEL_URL)
time.sleep(3)

# 自动滚动加载全部视频
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2.5)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 提取所有视频链接
videos = driver.find_elements(By.CSS_SELECTOR, "ytd-rich-item-renderer a#thumbnail")
links = [v.get_attribute("href") for v in videos if v.get_attribute("href")]

# 去重 + 保存
links = list(dict.fromkeys(links))
with open("video_links.txt", "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + "\n")

print(f"✅ 提取完成！共拿到 {len(links)} 个视频链接")
print("✅ 链接已保存到 video_links.txt")
driver.quit()