import os.path
import requests
import re
import json
from collections import defaultdict

# 发送HTTP GET请求获取网页内容
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("无法获取页面内容")

# 正则表达式搜索函数
def regex_search(pattern, text):
    return re.findall(pattern, text)

# 读取已有的index.json文件
def read_existing_index():
    if os.path.exists("index.json") and os.path.getsize("index.json") > 0:
        with open("index.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {"download": [], "file": []}

# 主函数
def main():
    url = "https://optifine.net/downloads"
    page_content = get_page(url)

    if len(page_content) < 200:
        raise Exception("获取到的版本列表长度不足")

    # 获取所有版本信息
    forge_versions = regex_search("(?<=colForge'>)[^<]*", page_content)
    release_times = regex_search("(?<=colDate'>)[^<]+", page_content)
    names = regex_search("(?<=OptiFine_)[0-9A-Za-z_.]+(?=.jar\")", page_content)

    print("forge_versions", forge_versions)
    print("release_times", release_times)
    print("names", names)
    if not len(release_times) == len(names):
        raise Exception("版本与发布时间数据无法对应")
    if not len(forge_versions) == len(names):
        raise Exception("版本与 Forge 兼容数据无法对应")
    if len(release_times) < 10:
        raise Exception("获取到的版本数量不足")

    # 转化为列表输出
    versions = []

    for i in range(len(release_times)):
        names[i] = names[i].replace("_", " ")
        entry = {
            "name": names[i].replace("HD U ", "").replace(".0 ", " "),
            "time": "-".join(release_times[i].split(".")[::-1]),
            "ispreview": "pre" in names[i].lower(),
            "mcversion": names[i].split(" ")[0],
            "filename": ("preview_" if "pre" in names[i].lower() else "") + "OptiFine_" + names[i].replace(" ", "_") + ".jar",
            "forge": forge_versions[i]
        }
        entry["name"] = names[i].replace(" ", "_").replace(entry["mcversion"] + "_", "")
        versions.append(entry)

    # 读取已有的index.json文件
    existing_index = read_existing_index()

    # 覆盖download字段
    existing_index["download"] = [
        "https://of-302-v.8mi.edu.pl/file/",
        "https://of-302-cf.8mi.edu.pl/file/",
        "https://of-302v.zkitefly.eu.org/file/",
        "https://of-302.zkitefly.eu.org/file/",
        "https://of-302v.zkitefly.free.hr/file/",
        "https://of-302.zkitefly.free.hr/file/",
        "https://of-302.burningtnt.workers.dev/file/",
    ]
    # existing_index["download"] = [
    #     "https://of-302.burningtnt.workers.dev/file/",
    #     "https://of-302.zkitefly.free.hr/file/",
    #     "https://of-302v.zkitefly.free.hr/file/",
    #     "https://of-302.zkitefly.eu.org/file/",
    #     "https://of-302v.zkitefly.eu.org/file/",
    #     "https://of-302-cf.8mi.edu.pl/file/",
    #     "https://of-302-v.8mi.edu.pl/file/",
    # ]

    # 合并数据
    existing_index["file"].extend(versions)

    # 去重
    file_time_dict = defaultdict(list)
    for file_info in existing_index["file"]:
        file_name = file_info["filename"]
        file_time = file_info["time"]
        file_time_dict[file_name].append((file_time, file_info))

    unique_files = []
    for file_name, file_infos in file_time_dict.items():
        max_time_file_info = max(file_infos, key=lambda x: x[0])
        unique_files.append(max_time_file_info[1])

    existing_index["file"] = unique_files
    
    # 根据时间降序排序
    existing_index["file"] = sorted(existing_index["file"], key=lambda x: x["time"], reverse=True)

    # 将数据保存为index.json文件
    with open("index.json", "w", encoding="utf-8") as file:
        json.dump(existing_index, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
    print("Done!")
