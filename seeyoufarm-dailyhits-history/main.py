import json
import requests
import os
from datetime import datetime

badge = "https://hits.seeyoufarm.com/api/count/incr/badge.svg?count_bg=%230D1117&title_bg=%230D1117&icon=github.svg&icon_color=%23E7E7E7&title=zkitefly%2Fseeyoufarm-dailyhits-history&url="

dailyhits = "https://hits.seeyoufarm.com/api/count/graph/dailyhits.svg?url="

# 读取url.json文件
with open('url.json', 'r') as file:
    data = json.load(file)

# 确保badgesvg文件夹存在
if not os.path.exists('badgesvg'):
    os.makedirs('badgesvg')

# 确保dailyhitssvg文件夹存在
if not os.path.exists('dailyhitssvg'):
    os.makedirs('dailyhitssvg')

# 确保history文件夹存在
if not os.path.exists('history'):
    os.makedirs('history')

# 遍历json数据中的每个对象
for item in data:
    name = item['name']
    url = item['url']

    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')

    # 创建文件名
    badgefilename = f'badgesvg/{name}_{current_time}.svg'
    dailyhitfilename = f'dailyhitssvg/{name}_{current_time}.svg'

    # 使用requests库下载.svg文件
    badgesvg = requests.get(badge + url)
    dailyhitssvg = requests.get(dailyhits + url)

    # 将下载的文件保存到指定的文件名
    with open(badgefilename, 'wb') as file:
        file.write(badgesvg.content)
    with open(dailyhitfilename, 'wb') as file:
        file.write(dailyhitssvg.content)

    # 检查是否存在名为"name.md"的文件，如果不存在，则创建该文件
    history_file = f'history/{name}.md'
    if not os.path.exists(history_file):
        with open(history_file, 'w') as file:
            pass

    # 在文件的顶部写入一行，内容为"# 名称_时间.svg}"
    # 在下一行写入"![名称_时间](/badgesvg/名称_时间)"
    # 在下一行写入"![名称_时间](/dailyhitssvg/名称_时间)"
    with open(history_file, 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(f"# {name}_{current_time}\n")
        file.write(f"![{name}_{current_time}](/badgesvg/{name}_{current_time}.svg)\n\n")
        file.write(f"![{name}_{current_time}](/dailyhitssvg/{name}_{current_time}.svg)\n")
        file.write(content)