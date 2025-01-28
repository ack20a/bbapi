import requests
import re
import time

from api.config import get_settings

settings = get_settings()
base_url = settings.PROXY_URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Cache variables
cached_vid = None
cache_time = 0
CACHE_DURATION = 36000  # Cache duration in seconds (10 hour)

def getVid(force_refresh=False):
    global cached_vid, cache_time
    current_time = time.time()

    # 检查是否强制刷新或缓存值是否仍然有效
    if not force_refresh and cached_vid and (current_time - cache_time) < CACHE_DURATION:
        print("using cached_vid:", cached_vid)
        return cached_vid

    try:
        # 获取初始 HTML 内容
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        content = response.text

        # 使用正则表达式查找特定的 static/chunks 路径
        js_files = re.findall(r'static/chunks/\d{4}-[a-fA-F0-9]+\.js', content)
        for js_file in js_files:
            # 构造 JS 文件的完整 URL
            full_url = f"{base_url}/_next/{js_file}"

            # 请求 JS 文件内容
            js_response = requests.get(full_url, headers=headers)
            js_response.raise_for_status()

            # 在 JS 内容中使用正则表达式搜索 h-value
            v_pattern = r'([a-zA-Z0-9]+)="([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"'
            v_match = re.search(v_pattern, js_response.text)

            if v_match:
                v_value = v_match.group(2)
                print("找到 v-value:", v_value)
                # 更新缓存
                cached_vid = v_value
                cache_time = current_time
                return v_value
        print("未找到 v-value")
    except requests.exceptions.RequestException as e:
        print(f"发生错误: {e}")
        return None
