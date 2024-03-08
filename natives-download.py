import requests
import os
import re

# 定义下载文件的函数
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"已下载文件到 {save_path}")
    else:
        print(f"下载失败：{url}")

# 下载 natives.json 文件
natives_json_url = "https://github.com/huanghongxun/HMCL/raw/javafx/HMCL/src/main/resources/assets/natives.json"
natives_json_path = "natives.json"

response = requests.get(natives_json_url)
if response.status_code == 200:
    with open(natives_json_path, 'wb') as file:
        file.write(response.content)
else:
    print(f"下载 natives.json 文件失败：{natives_json_url}")
    exit()

# 读取 natives.json 文件内容
with open(natives_json_path, 'r') as file:
    json_data = file.read()

# 使用正则表达式匹配 URL
pattern = r"https://repo1.maven.org/maven2/[^\"']+"  # 匹配以"https://repo1.maven.org/maven2/"开头的URL
urls = re.findall(pattern, json_data)

# 下载匹配到的文件
for url in urls:
    # 去掉 "https://repo1.maven.org/maven2/" 后的路径
    file_path = url.replace("https://repo1.maven.org/maven2/", "")
    # 创建本地保存路径
    local_path = os.path.join(os.getcwd(), file_path)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # 下载文件
    download_file(url, local_path)
