import json
import os
import requests
import shutil

# 删除已存在的 versionlist 文件夹
if os.path.exists("versionlist"):
    shutil.rmtree("versionlist")

# 下载 versionList.json 文件
url = "https://bmclapi2.bangbang93.com/optifine/versionList"
response = requests.get(url)
response.raise_for_status()  # 检查请求是否成功
version_list = response.json()

# 保存 versionList.json 文件
with open("versionlist.json", "w") as file:
    json.dump(version_list, file)

# 创建文件夹 versionlist
os.makedirs("versionlist", exist_ok=True)  # 使用 os.makedirs 递归创建文件夹

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
        forge_response.raise_for_status()  # 检查请求是否成功
        forge_list = forge_response.json()
        for forge_entry in forge_list:
            forge_build = str(forge_entry.get("build"))
            if forge_build and forge_build.split(".")[-1] == forge_value.split("#")[-1]:
                helpforge = f"Forge {forge_entry.get('version')}"
                break
    else:
        helpforge = forge_value

    # 读取 versionList.json 的 mcversion、type、patch 值
    mcversion_value = version_entry.get("mcversion")
    type_value = version_entry.get("type")
    patch_value = version_entry.get("patch")
    filename = version_entry.get("filename")

    if helpforge != 'nohelp':
        forged = helpforge.replace('Forge ', '')

    # 创建并写入文本文件
    file_name = f"{mcversion_value}-{type_value}_{patch_value}.md"
    file_path = os.path.join("versionlist", file_name)
    with open(file_path, "w") as file:
        if helpforge == "nohelp":
            file.write(f"# Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 不支持**任何** Forge 版本\n\n")
            file.write("## 你可以前往 [→此处←](./all.md) 查看全部支持情况，找一个相邻的版本进行调整。\n\n")
            file.write("### HMCL\n\n")
            file.write("#### 你需要在 HMCL 的 `版本设置` -> `自动安装` 中调整 Optifine 版本或（/和） Forge 版本，或将 Optifine 或 Forge 卸载。\n\n![hmcl](hmcl.gif)\n\n")
            file.write("### 其他启动器\n\n")
            file.write("#### 重新安装 Optifine 或 Forge 选其中一个。\n\n")
            file.write(f"##### [→点此处下载该版本 Optifine←](https://optifine.cn/download/{filename})\n\n")
        else:
            file.write(f"# Minecraft `{mcversion_value}` OptiFine `{type_value}_{patch_value}` 支持 `{helpforge}` 版本\n\n")
            file.write("### HMCL\n\n")
            file.write("#### 你需要在 HMCL 的 `版本设置` -> `自动安装` 中调整 Optifine 版本或（/和） Forge 版本。\n\n![hmcl](hmcl.gif)\n\n")
            file.write("### 其他启动器\n\n")
            file.write("#### 重新安装 Optifine 和 Forge，安装时请留意版本！\n\n")
            file.write(f"##### [→点此处下载该版本 Optifine←](https://optifine.cn/download/{filename}) | [→点击此处下载该版本所支持的 Forge 安装器←](https://maven.minecraftforge.net/net/minecraftforge/forge/{mcversion_value}-{forged}/forge-{mcversion_value}-{forged}-installer.jar)\n\n")