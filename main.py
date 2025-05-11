import requests  # HTTP 请求库
import os        # 操作系统路径操作
import time      # 控制请求间隔时间
import tqdm      # 显示进度条

# ================== 用户可配置参数 ==================
# 请求目标 URL
URL = "https://movie.douban.com/top250"

# 请求头信息（User-Agent 等）
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://movie.douban.com/top250?start=0&filter=",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}

# Cookies（模拟登录状态）
COOKIES = {
    "ll": "\"118290\"",
    "bid": "Js8UNhwgzTM",
    "_pk_id.100001.4cf6": "8140237adfa1b962.1742831623.",
    "__yadk_uid": "F6p24KrilUkFCgCEkaps43h8Lie5ARzD",
    "_vwo_uuid_v2": "D9B86B0D908713F4593DD6F2905E36A7D|d74ed41d08eae77b42aaa6aba907799b",
    "__utma": "223695111.637368789.1742831623.1742831623.1746960297.2",
    "__utmc": "223695111",
    "__utmz": "223695111.1746960297.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
    "__utmt": "1",
    "__utmb": "223695111.0.10.1746960297",
    "_pk_ref.100001.4cf6": "%5B%22%22%2C%22%22%2C1746960297%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D",
    "_pk_ses.100001.4cf6": "1",
    "ap_v": "0,6.0",
    "loc-last-index-location-id": "\"118290\""
}

# 请求参数：用于分页抓取
START_STEP = 25            # 每页步长
PAGE_COUNT = 10            # 总共抓取的页面数
TOTAL_ITEMS = START_STEP * PAGE_COUNT  # 总电影数量（默认 250）

# 输出文件路径
INPUT_DIR = os.path.join(os.getcwd(), "inputdata")
OUTPUT_FILENAME = "doubantop250.txt"
OUTPUT_FILE_PATH = os.path.join(INPUT_DIR, OUTPUT_FILENAME)

# 请求超时时间（秒）
REQUEST_TIMEOUT = 10

# 请求间隔时间（秒），防止被封 IP
REQUEST_INTERVAL = 1

# ===================================================


def fetch_page(url, params, headers, cookies, timeout):
    """
    抓取单个页面
    :param url: 请求地址
    :param params: 请求参数
    :param headers: 请求头
    :param cookies: Cookie
    :param timeout: 请求超时时间
    :return: 页面 HTML 内容
    """
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        params=params,
        timeout=timeout
    )
    if response.status_code != 200:
        raise Exception(f"HTTP 状态码异常: {response.status_code}")
    return response.text


def save_to_file(content, file_path, is_last=False):
    """
    将页面内容写入文件，每页占一行
    :param content: 页面内容字符串
    :param file_path: 文件路径
    :param is_last: 是否为最后一行
    """
    cleaned_content = content.replace('\n', '').replace('\r', '')  # 去除换行符，确保一行
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(cleaned_content + ('' if is_last else '\n'))  # 最后一行不加换行符


def main():
    """主函数：循环抓取多页数据并保存"""
    os.makedirs(INPUT_DIR, exist_ok=True)  # 创建 inputdata 目录（如果不存在）

    start_range = range(0, TOTAL_ITEMS, START_STEP)  # 分页起始值列表

    for i, start in enumerate(tqdm.tqdm(start_range, desc="正在抓取豆瓣 Top250")):
        params = {
            "start": str(start),
            "filter": ""
        }
        try:
            html_content = fetch_page(URL, params, HEADERS, COOKIES, REQUEST_TIMEOUT)
            is_last = (i == len(start_range) - 1)
            save_to_file(html_content, OUTPUT_FILE_PATH, is_last=is_last)
            print(f"第 {i + 1} 页抓取完毕")
            time.sleep(REQUEST_INTERVAL)  # 防止请求频率过高
        except Exception as e:
            print(f"抓取失败（页 {i + 1}）: {e}")

    print("所有页面抓取完毕")


if __name__ == "__main__":
    main()
