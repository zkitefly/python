import requests
import re

def get_links_and_search(input_text):
    # 获取主链接的JSON数据
    main_url = "https://piston-meta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json"
    main_response = requests.get(main_url)
    
    if main_response.status_code == 200:
        # 使用正则表达式提取所有URL
        links = re.findall(r'"url": "(.*?)"', main_response.text)

        # 遍历链接并获取文本内容
        for link in links:
            print(link)
            link_response = requests.get(link)

            if link_response.status_code == 200:
                # 获取文本内容
                text_content = link_response.text

                # 在文本中搜索用户输入的字符
                if input_text in text_content:
                    print(f"在链接 {link} 中找到了匹配的内容")
    
    else:
        print(f"无法获取主链接的JSON数据。状态码：{main_response.status_code}")

if __name__ == "__main__":
    # 获取用户输入的搜索内容
    user_input = input("请输入搜索内容：")
    
    # 调用函数进行搜索
    get_links_and_search(user_input)
