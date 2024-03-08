import os
import json
import requests
import concurrent.futures
import re
import shutil

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义下载目录
download_folder = os.path.join(script_dir, "minecraft-old-snapshots")

# 如果下载目录不存在，则创建它
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 下载 JSON 文件
json_url = "https://github.com/PrismLauncher/meta/raw/main/static/mojang/minecraft-old-snapshots.json"
local_json_path = os.path.join(script_dir, "minecraft-old-snapshots.json")  # 本地保存路径

response = requests.get(json_url)

if response.status_code == 200:
    # 保存JSON文件到本地
    with open(local_json_path, "wb") as json_file:
        json_file.write(response.content)

    # 解析 JSON 数据
    data = json.loads(response.text)
    snapshots = data.get("old_snapshots", [])  # 获取"old_snapshots"列表

    def download_snapshot(entry):
        id_value = entry["id"]
        url_value = entry["url"]
        jar_url_value = entry["jar"]  # 获取"jar"键的值

        # 创建子文件夹以存储每个版本的文件
        version_folder = os.path.join(download_folder, id_value)
        if not os.path.exists(version_folder):
            os.makedirs(version_folder)

        # 构建文件下载路径（对于url键和jar键）
        json_file_name = f"{id_value}.json"  # JSON文件名以{id}.json方式命名
        download_path = os.path.join(version_folder, json_file_name)

        # 下载url键对应的文件
        if not os.path.exists(download_path):
            print(f"正在下载 {id_value} 版本的JSON文件...")
            # 尝试在链接前加上 "https://cfp.zkitefly.eu.org/"
            response = requests.get("https://cfp.zkitefly.eu.org/" + url_value)
            if response.status_code != 200:
                print("尝试使用前缀失败，将尝试直接下载...")
                response = requests.get(url_value)

            if response.status_code == 200:
                with open(download_path, "wb") as file:
                    file.write(response.content)
                print(f"{id_value} 版本的JSON文件下载完成.")
            else:
                print(f"无法下载 {id_value} 版本的JSON文件.")
        else:
            print(f"{id_value} 版本的JSON文件已存在，跳过下载.")

        # 构建jar文件的下载路径
        jar_file_name = f"{id_value}.jar"
        jar_download_path = os.path.join(version_folder, jar_file_name)

        # 下载jar键对应的文件
        if not os.path.exists(jar_download_path):
            print(f"正在下载 {id_value} 版本的JAR文件...")
            # 尝试在链接前加上 "https://cfp.zkitefly.eu.org/"
            response = requests.get("https://cfp.zkitefly.eu.org/" + jar_url_value)
            if response.status_code != 200:
                print("尝试使用前缀失败，将尝试直接下载...")
                response = requests.get(jar_url_value)

            if response.status_code == 200:
                with open(jar_download_path, "wb") as jar_file:
                    jar_file.write(response.content)
                print(f"{id_value} 版本的JAR文件下载完成.")
            else:
                print(f"无法下载 {id_value} 版本的JAR文件.")
        else:
            print(f"{id_value} 版本的JAR文件已存在，跳过下载.")

    # 使用多线程下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_snapshot, snapshots)

    # 复制一份 minecraft-old-snapshots.json 并修改内容
    copied_json_path = os.path.join(script_dir, "!minecraft-old-snapshots.json")
    shutil.copy(local_json_path, copied_json_path)


    # 替换JSON文件的内容
    json_content = json.dumps(data, indent=4)
    for entry in snapshots:
        id_value = entry["id"]
        json_content = re.sub(
            rf"https://archive\.org/download/assets\.minecraft\.net-2013-11-13/assets\.minecraft\.net/{id_value}",
            f"https://zkitefly.github.io/minecraft-old-snapshots/{id_value}/{id_value}",
            json_content,
        )
        json_content = re.sub(
            rf"https://archive\.org/download/Minecraft-JSONs/{id_value}\.json",
            f"https://zkitefly.github.io/minecraft-old-snapshots/{id_value}/{id_value}.json",
            json_content,
        )

    with open(local_json_path, "w") as json_file:
        json_file.write(json_content)

    print("JSON文件内容替换完成.")
else:
    print("无法下载 JSON 文件.")
