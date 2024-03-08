import os
import json
import requests

# 检查并创建下载目录和changelog目录
download_dir = 'downloads'
changelog_dir = 'changelog'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
if not os.path.exists(changelog_dir):
    os.makedirs(changelog_dir)

# 读取本地optifine.json文件
with open('optifine.json', 'r') as json_file:
    data = json_file.read()
    # 解析JSON数据，假设JSON结构是一个包含多个字典项的列表
    optifine_data_list = json.loads(data)

# 循环处理每个字典项
for optifine_data in optifine_data_list:
    filename = optifine_data.get('filename')

    if filename:
        # 构建下载链接
        download_url = f'https://optifine.net/downloadx?f={filename}&x=a68358a538a9d227f24b4d98c5718baf'
        changelog_url = f'https://optifine.net/changelog?f={filename}'

        # 下载Optifine文件
        with open(os.path.join(download_dir, filename), 'wb') as file:
            response = requests.get(download_url)
            file.write(response.content)

        # 下载changelog文件并保存到changelog目录中
        changelog_filename = f'{filename}'
        changelog_filename1 = f'{filename}.txt'
        with open(os.path.join(changelog_dir, changelog_filename), 'wb') as changelog_file:
            response = requests.get(changelog_url)
            changelog_file.write(response.content)
        with open(os.path.join(changelog_dir, changelog_filename1), 'wb') as changelog_file:
            response = requests.get(changelog_url)
            changelog_file.write(response.content)

        print(f'{filename} 下载完成！')
    else:
        print("找不到filename值，请检查 optifine.json 文件的内容。")
