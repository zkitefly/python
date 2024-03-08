import os
import json
import requests
import re
import shutil
import zipfile

# 定义文件夹和 JSON 文件的路径
json_url = "https://gp.zkitefly.eu.org/https://github.com/PrismLauncher/meta/raw/main/static/mojang/minecraft-experiments.json"
download_folder = "minecraft-experiments"
local_json_file = "minecraft-experiments.json"

# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
else:
    # 如果文件夹已经存在，删除文件夹中的所有文件
    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"删除文件 {file_path} 时出错：{e}")

# 下载 JSON 文件并保存到本地
response = requests.get(json_url)
if response.status_code == 200:
    json_data = response.json()
    with open(local_json_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
else:
    print(f"下载JSON文件失败。HTTP 错误代码：{response.status_code}")

# 读取本地JSON文件
with open(local_json_file, "r") as json_file:
    json_data = json.load(json_file)

# 获取实验数组
experiments = json_data.get("experiments", [])

if experiments:
    for experiment in experiments:
        # 获取下载链接
        download_link = experiment.get("url", None)
        
        if download_link:
            # 在下载链接前面加入指定的前缀
            modified_download_link = "https://cfp.zkitefly.eu.org/" + download_link
            
            # 获取文件名
            file_name = os.path.join(download_folder, os.path.basename(download_link))
            
            # 下载文件，最多重试两次
            max_retries = 2
            retries = 0
            while retries < max_retries:
                response = requests.get(modified_download_link)
                if response.status_code == 200:
                    with open(file_name, "wb") as file:
                        file.write(response.content)
                    print(f"成功下载文件到 {file_name}")
                    break
                else:
                    print(f"下载文件失败。即将去除反代下载重试！HTTP 错误代码：{response.status_code}")
                    if retries < max_retries - 1:
                        # 去掉 modified_download_link 重试
                        modified_download_link = download_link
                        retries += 1
                    else:
                        print(f"无法下载文件。下载链接：{download_link}")
                        break
        else:
            print("未找到下载链接。")


# 解压缩所有 zip 文件到 minecraft-experiments 文件夹中
for filename in os.listdir(download_folder):
    file_path = os.path.join(download_folder, filename)
    if filename.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(download_folder)
            print(f"成功解压文件 {filename} 到 {download_folder}")

# 复制本地 minecraft-experiments.json 到一个新的文件，将新文件名前加上 "!"
new_json_file = "!minecraft-experiments.json"
shutil.copyfile(local_json_file, new_json_file)

# 修改原始的 minecraft-experiments.json 文件中的链接
with open(local_json_file, "r") as json_file:
    original_json_data = json.load(json_file)

# 正则表达式用于定位链接中的部分
regex_pattern = r"/([^/]+)$"

if "experiments" in original_json_data:
    for experiment in original_json_data["experiments"]:
        url = experiment.get("url")
        if url:
            match = re.search(regex_pattern, url)
            if match:
                modified_url = "https://zkitefly.github.io/minecraft-experiments/" + match.group(1).replace(".zip", ".json")
                experiment["url"] = modified_url

# 将修改后的 JSON 数据写回文件
with open(local_json_file, "w") as json_file:
    json.dump(original_json_data, json_file, indent=4)

print("已完成所有操作。")
