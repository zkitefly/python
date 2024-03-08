import os
import json
import requests

# 获取版本列表并保存为versionlist.json
response = requests.get('https://bmclapi2.bangbang93.com/optifine/versionList')
version_list = response.json()
with open('versionlist.json', 'w') as file:
    json.dump(version_list, file)

# 如果存在all.md文件，则删除
if os.path.exists('all.md'):
    os.remove('all.md')

# 创建all.md文件并写入标题
with open('all.md', 'w') as file:
    file.write('# Optifine 所支持 Forge 版本的列表\n\n## ↑你可以点击上方蓝色链接前往搜索↑\n\n')

# 遍历 versionList.json 中的每个元素
for version_entry in version_list:
    # 读取 versionList.json 的 forge 值
    forge_value = version_entry.get("forge")
    helpforge = ""
    if forge_value is None or forge_value == "Forge N/A":
        helpforge = "nohelp"
    elif "#" in forge_value:
        mcversion_value = version_entry.get("mcversion")
        forge_url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{mcversion_value}"
        forge_response = requests.get(forge_url)
        forge_list = forge_response.json()
        for forge_entry in forge_list:
            forge_build = str(forge_entry.get("build"))
            if forge_build and forge_build.split(".")[-1] == forge_value.split("#")[-1]:
                helpforge = f"Forge {forge_entry.get('version')}"
                break
    else:
        helpforge = forge_value

    if helpforge != 'nohelp':
        forged = helpforge.replace('Forge ', '')

    # 读取其他信息并写入all.md文件
    mcversion_value = version_entry['mcversion']
    type_value = version_entry['type']
    patch_value = version_entry['patch']
    filename = version_entry['filename']

    with open('all.md', 'a') as file:
        if helpforge == 'nohelp':
            file.write(f'### Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 不支持**任何** Forge 版本，[下载该版本 Optifine](https://optifine.cn/download/{filename})\n\n')
        else:
            file.write(f'### Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 支持 `{helpforge}` 版本，[下载该版本 Optifine](https://optifine.cn/download/{filename}) | [下载该版本支持的 Forge 安装器](https://maven.minecraftforge.net/net/minecraftforge/forge/{mcversion_value}-{forged}/forge-{mcversion_value}-{forged}-installer.jar)\n\n')
