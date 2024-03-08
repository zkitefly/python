import json
import requests
from concurrent.futures import ThreadPoolExecutor

def check_bmclapi_link():
    bmclapi_url = "https://bmclapi2.bangbang93.com/optifine/versionList"
    try:
        response = requests.get(bmclapi_url)
        if response.status_code == 200:
            print("成功获取到 BMCLAPI 版本列表，继续运行。")
            return True
        else:
            print(f"无法获取 BMCLAPI 版本列表，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"连接 BMCLAPI 版本列表出错: {e}")
        return False

def check_link(module):
    filename = module['filename']
    url = f"https://of-302v.zkitefly.eu.org/file/{filename}"
    try:
        response = requests.head(url, proxies=None)
        if response.status_code == 404:
            print(f"链接 {url} 返回 404，删除模块 {filename}")
            delete_module(module)
        elif response.status_code != 200:
            print(f"链接 {url} 返回状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"连接 {url} 出错: {e}")

def delete_module(module):
    # 根据需要执行删除模块的操作
    # 这里只是简单打印一条消息
    print(f"模块 {module['filename']} 已删除")
    # 删除模块
    index_data['file'].remove(module)

def check_links():
    # 检测 OptiFine 版本列表链接
    if not check_bmclapi_link():
        print("无法继续执行脚本，BMCLAPI 无法连接。")
        return
    
    # 读取 index.json 文件
    with open('index.json', 'r') as f:
        global index_data
        index_data = json.load(f)
    
    # 使用线程池并发检测链接
    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = [executor.submit(check_link, module) for module in index_data['file']]
        for future in futures:
            future.result()

    # 保存更新后的 JSON 数据
    with open('index.json', 'w') as f:
        json.dump(index_data, f, indent=4)

if __name__ == "__main__":
    check_links()
