import os
import subprocess
import shutil
import json
import time

def download_file(url, filename):
    while True:
        try:
            subprocess.run(['wget', url, '-O', filename])
            break
        except:
            print("下载失败，重新尝试...")
            time.sleep(2)

# 步骤1: 使用wget下载versionList.json并保存为versionlist.json
download_file('https://bmclapi2.bangbang93.com/optifine/versionList', 'versionlist.json')

# 等待2秒
time.sleep(2)

# 步骤2: 如果存在game文件夹，则删除
if os.path.exists('game'):
    shutil.rmtree('game')

# 新增步骤: 如果存在forge文件夹，则删除
if os.path.exists('forge'):
    shutil.rmtree('forge')

# 步骤3: 创建game文件夹
os.mkdir('game')

# 新增步骤: 创建forge文件夹
os.mkdir('forge')

# 步骤4: 读取versionlist.json文件内容并赋值给version_list变量
with open('versionlist.json', 'r') as file:
    version_list = json.load(file)

# 步骤5: 遍历version_list中的每个元素
for version_entry in version_list:
    mcversion_value = version_entry.get('mcversion')
    type_value = version_entry.get('type')
    patch_value = version_entry.get('patch')
    filename = version_entry.get('filename')
    forge_value = version_entry.get('forge')
    helpforge = ""

    if forge_value is None or forge_value == "Forge N/A":
        helpforge = "nohelp"
    elif "#" in forge_value:
        mcversion_value = version_entry.get('mcversion')
        if mcversion_value == '1.8.0':
            mcversion_value = '1.8'
        if mcversion_value == '1.9.0':
            mcversion_value = '1.9'

        if os.path.exists(f'forge/{mcversion_value}.json') and os.stat(f'forge/{mcversion_value}.json').st_size > 5:
            with open(f'forge/{mcversion_value}.json', 'r') as forge_file:
                forge_list = json.load(forge_file)
        else:
            forge_url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{mcversion_value}"
            download_file(forge_url, f'forge/{mcversion_value}.json')
            time.sleep(2)

            if os.path.exists(f'forge/{mcversion_value}.json') and os.stat(f'forge/{mcversion_value}.json').st_size > 5:
                with open(f'forge/{mcversion_value}.json', 'r') as forge_file:
                    forge_list = json.load(forge_file)

        for forge_entry in forge_list:
            forge_build = str(forge_entry.get('build'))
            if forge_build and forge_build.split('.')[-1] == forge_value.split('#')[-1]:
                helpforge = f"Forge {forge_entry.get('version')}"
                break
    else:
        helpforge = forge_value

    if helpforge != 'nohelp':
        if '#' in helpforge:
            forged = helpforge
        else:
            forged = helpforge.replace('Forge ', '')

    # 写入md文件
    with open(f'game/{mcversion_value}.md', 'a') as file:
        if helpforge == 'nohelp':
            file.write(f'### Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 不支持**任何** Forge 版本，[下载该版本 Optifine](https://optifine.cn/download/{filename})\n\n\n\n')
        else:
            file.write(f'### Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 支持 `{helpforge}` 版本，[下载该版本 Optifine](https://optifine.cn/download/{filename}) | [下载该版本支持的 Forge 安装器](https://maven.minecraftforge.net/net/minecraftforge/forge/{mcversion_value}-{forged}/forge-{mcversion_value}-{forged}-installer.jar)\n\n\n\n')

# 删除临时文件
if os.path.exists('forge_info.json'):
    os.remove('forge_info.json')
