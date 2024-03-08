import json
import re

def process_filename(filename, mcversion):
    # 处理文件名，剔除 OptiFine_ 和前面的字符，然后剔除 .jar，再剔除 {mcversion}_ 
    processed_name = re.sub(r'^.*OptiFine_', '', filename)
    processed_name = re.sub(r'\.jar$', '', processed_name)
    processed_name = re.sub(fr'{mcversion}_', '', processed_name)
    return processed_name

def add_property(module):
    # 如果模块缺少 name 属性，则添加
    if 'name' not in module:
        mcversion = module.get('mcversion', '')
        processed_name = process_filename(module['filename'], mcversion)
        module['name'] = processed_name
    # 如果模块缺少 time 属性，则添加
    if 'time' not in module:
        module['time'] = "0000-00-00"
    # 如果模块缺少 ispreview 属性，则添加
    if 'ispreview' not in module:
        module['ispreview'] = "pre" in module['filename'].lower()
    # 如果模块缺少 forge 属性，则添加
    if 'forge' not in module:
        module['forge'] = "Forge N/A"

# 读取 index.json 文件
with open('index.json', 'r') as file:
    data = json.load(file)

# 处理每个模块
for module in data['file']:
    add_property(module)

# 保存更新后的 index.json 文件
with open('index.json', 'w') as file:
    json.dump(data, file, indent=2)

print("处理完成！")
