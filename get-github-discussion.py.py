import requests
import json

# 注：第一次使用需要安装 requests 库
# 在 cmd 或终端中输入并回车： pip install requests

# 设置GitHub API的访问令牌
access_token = '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'  # 请替换为你的GitHub访问令牌

# 要获取GitHub访问令牌（Access Token），请按照以下步骤操作：
# 
# 登录到你的GitHub帐号。
# 在右上角的头像下拉菜单中，选择"Settings"（设置）选项。
# 在左侧导航菜单中，选择"Developer settings"（开发者设置）。
# 在左侧导航菜单中，选择"Personal access tokens"（个人访问令牌）。
# 点击"Generate new token"（生成新令牌）按钮。
# 在"Note"（注释）字段中，为令牌起一个描述性的名称。
# 在"Select scopes"（选择范围）部分，选择你希望该访问令牌拥有的权限。对于访问GitHub Discussions的API，你至少需要选择public_repo（公开仓库）和read:discussion（读取讨论）权限。
# 滚动到页面底部，点击"Generate token"（生成令牌）按钮。
# 系统将生成一个访问令牌，并将其显示在屏幕上。请确保复制并保存好该令牌，因为在之后你将无法再次看到完整的令牌内容。
# 将复制的访问令牌粘贴到Python脚本中的access_token变量中。
# 请注意，访问令牌是与你的GitHub账户关联的敏感信息。务必妥善保存和保护好你的访问令牌，不要将其泄露给他人。

# 设置GraphQL API的请求头部信息
headers = {
    'Authorization': f'bearer {access_token}',
    'Accept': 'application/vnd.github.echo-preview+json'
}

# 设置GraphQL API的请求体 （此处示例为读取 https://github.com/zkitefly/zkitefly.github.io/discussions/7 ）
query = '''
query {
  repository(owner: "zkitefly", name: "zkitefly.github.io") {
    discussion(number: 7) {
      title
      body
    }
  }
}
'''

# 发起GraphQL API请求
response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
data = response.json()

# 提取讨论的标题和正文内容
title = data['data']['repository']['discussion']['title']
body = data['data']['repository']['discussion']['body']

# 将讨论内容写入文件
with open('index.md', 'w', encoding='utf-8') as file:
    file.write(f'Title: {title}\n')
    file.write(f'Body: {body}\n')

print('讨论内容已成功写入到index.md文件中。')
