# encoding:utf-8
import os  # 操作系统路径操作模块
from lxml import etree  # HTML 解析库
import json  # JSON 数据处理模块
import tqdm  # 进度条显示模块

# ================== 用户可配置参数 ==================
# 输入文件路径：存储抓取的网页 HTML 内容（一行一个页面）
INPUT_FILE_PATH = os.path.join(os.getcwd(), r"inputdata\doubantop250.txt")
# 输出文件路径：最终生成的电影信息 JSON 文件
OUTPUT_FILE_PATH = os.path.join(os.getcwd(), r"outputdata\doubantop250.json")

# XPath 配置（可根据豆瓣 Top250 页面结构调整）
XPATH_MOVIE_ITEMS = '//*[@id="content"]/div/div[1]/ol/li'  # 所有电影条目的根节点
XPATH_TITLE = "./div/div[2]/div[1]/a/span/text()"  # 电影标题
XPATH_INFO = "./div/div[2]/div[2]/p[1]/text()"  # 导演、年份、国家、类型等信息
XPATH_SCORE = "./div/div[2]/div[2]/div/span[2]/text()"  # 评分
XPATH_COMMENT = "./div/div[2]/div[2]/div/span[4]/text()"  # 评论数
XPATH_QUOTE = "./div/div[2]/div[2]/p[2]/span/text()"  # 引言/一句话描述

# ===================================================


def parse_movies(data):
    """
    解析 HTML 数据并提取电影信息
    :param data: 包含整个页面的 HTML 字符串
    :return: 提取后的电影信息列表
    """
    html = etree.HTML(data)  # 将字符串转换为 lxml 的 HTML 对象
    movies_items = html.xpath(XPATH_MOVIE_ITEMS)  # 使用 XPath 提取所有电影条目
    all_movies = []  # 初始化电影列表

    for item in tqdm.tqdm(movies_items, desc="正在解析电影数据"):
        # 提取并清洗电影标题
        titles = item.xpath(XPATH_TITLE)
        cleaned_titles = [title.replace('\xa0/\xa0', '').strip() for title in titles]  # 去除特殊空格与前后空格
        main_title = cleaned_titles[0] if len(cleaned_titles) > 0 else ''  # 主标题
        other_titles = cleaned_titles[1:] if len(cleaned_titles) > 1 else []  # 其他标题

        # 提取并清洗导演、年份、国家、类型信息
        infos = item.xpath(XPATH_INFO)
        cleaned_infos = [info.replace('\xa0', '').strip() for info in infos]
        director = ''
        year = ''
        country = ''
        genre = []
        if len(cleaned_infos) > 0:
            info_str1 = ''.join(cleaned_infos[0])
            director_part = info_str1.split('主演')[0]  # 截取“主演”前的内容
            director = director_part.replace('导演: ', '').strip()  # 提取导演名

            info_str2 = ''.join(cleaned_infos[1])
            year = info_str2.split('/')[0].strip()  # 年份
            country = info_str2.split('/')[1].strip()  # 国家
            genre = info_str2.split('/')[2].strip().split(' ')  # 类型，按空格分割成列表

        # 提取评分
        score = item.xpath(XPATH_SCORE)[0].strip() if item.xpath(XPATH_SCORE) else ''

        # 提取评论人数，并去除“人评价”
        comment = item.xpath(XPATH_COMMENT)[0].strip().replace('人评价', '') if item.xpath(XPATH_COMMENT) else ''

        # 提取引言
        quote = item.xpath(XPATH_QUOTE)[0].strip() if item.xpath(XPATH_QUOTE) else ''

        # 构建电影字典
        movie = {
            "title": main_title,
            "other_titles": other_titles,
            "director": director,
            "year": year,
            "country": country,
            "genre": genre,
            "score": score,
            "comments": comment,
            "quote": quote
        }
        all_movies.append(movie)

    return all_movies


def save_to_json(data, output_path):
    """
    将提取的数据保存为 JSON 文件
    :param data: 要保存的数据（列表格式）
    :param output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # 美化输出，不转义中文字符


def main():
    """
    主函数：读取输入文件 -> 解析电影数据 -> 保存为 JSON 文件
    """
    # 创建 outputdata 文件夹（如果不存在）
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH), exist_ok=True)

    # 读取文件内容
    with open(INPUT_FILE_PATH, "r", encoding="utf-8") as f:
        data = f.read()

    # 解析数据
    all_movies = parse_movies(data)

    # 保存为 JSON
    save_to_json(all_movies, OUTPUT_FILE_PATH)
    print("数据已保存到文件：", OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()
