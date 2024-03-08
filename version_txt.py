# https://gist.github.com/zkitefly/9e789c934a8cc7847330674432babfd0
import json
import os
import requests

# 读取版本列表和版本清单文件的URL
# test url: https://cdn.crashmc.com/https://gist.github.com/zkitefly/9e789c934a8cc7847330674432babfd0/raw/66a580349159aa26a405eb02f1dcbf6a16efeb15/test-versions.txt
versions_txt_url = "https://raw.githubusercontent.com/HMCL-dev/HMCL/javafx/HMCLCore/src/main/resources/assets/game/versions.txt"
version_manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
local_versions_txt = "versions.txt"

# 下载文件并保存到本地
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"文件 {filename} 下载完成。")
    else:
        print(f"下载 {filename} 文件失败。")

# 读取版本清单文件中的版本id
def read_version_manifest():
    response = requests.get(version_manifest_url)
    if response.status_code == 200:
        manifest_data = json.loads(response.text)
        versions = [version['id'] for version in manifest_data['versions']]
        return versions
    else:
        print("无法读取版本清单文件。")
        return None

# 读取版本列表文件中的最后一行文本
def read_last_line_from_versions_txt(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                last_line = lines[-1].strip()
            else:
                last_line = None
        return last_line
    except FileNotFoundError:
        print(f"{filename} 文件不存在。")
        return None

# 检查是否有新的版本id，并更新版本列表文件
def check_and_update_versions(versions_txt, new_versions):
    last_version = read_last_line_from_versions_txt(versions_txt)
    if last_version is None:
        return

    if last_version not in new_versions:
        print(f"找不到id: {last_version}")
        return

    new_ids = []
    found_last_version = False
    for version in new_versions:
        if found_last_version:
            new_ids.append(version)
        if version == last_version:
            found_last_version = True

    if not new_ids:
        print("没有新的id。")
        return

    with open(versions_txt, 'a') as f:
        print("新增的id（已按照从下至上版本号大至小的排序）: \n\n")
        for new_id in new_ids:
            # f.write(f"\n{new_id}")
            print(f"{new_id}")
        print("\n")

    # print(f"版本列表已更新并保存到 {versions_txt}。")

# 删除版本列表文件中最后一行的换行符
def remove_last_line_break(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        with open(filename, 'w') as f:
            f.writelines(lines[:-1])
        print(f"{filename} 文件中最后一行的换行符已删除。")
    except FileNotFoundError:
        print(f"{filename} 文件不存在。")

# 主函数
def main():
    download_file(versions_txt_url, local_versions_txt)
    new_versions = read_version_manifest()
    if new_versions:
        new_versions.reverse()  # 将版本清单反转，确保从第一个开始读取
        # remove_last_line_break(local_versions_txt)
        check_and_update_versions(local_versions_txt, new_versions)

if __name__ == "__main__":
    main()
