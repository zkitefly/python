import requests
import re
import json

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
            "time": "/".join(release_times[i].split(".")[::-1]),
            "ispreview": "pre" in names[i].lower(),
            "mcversion": names[i].split(" ")[0],
            "filename": ("preview_" if "pre" in names[i].lower() else "") + "OptiFine_" + names[i].replace(" ", "_") + ".jar",
            "forge": forge_versions[i].replace("Forge ", "").replace("#", "") if "N/A" not in forge_versions[i] else None
        }
        entry["name"] = entry["mcversion"] + "-OptiFine_" + names[i].replace(" ", "_").replace(entry["mcversion"] + "_", "")
        versions.append(entry)

    # 将数据保存为 optifine.json 文件
    with open("optifine.json", "w", encoding="utf-8") as file:
        json.dump(versions, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
