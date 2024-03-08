import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 用户输入JSON路径
json_path = input("请输入JSON文件路径：")

# 读取JSON文件
with open(json_path, 'r') as json_file:
    data = json.load(json_file)

# 转换JSON数据为DataFrame
df = pd.DataFrame(data['account']).T
df.index.name = '对象'
df.reset_index(inplace=True)

# 生成当前时间的字符串形式，用于文件名
current_time = datetime.now().strftime("%Y%m%d%H%M%S")

# 生成表格并保存
table_filename = f"table_{current_time}.csv"
df.to_csv(table_filename, index=False)

# 生成条形图
plt.figure(figsize=(10, 6))
plt.bar(df['对象'], df['count'])
plt.xlabel('对象')
plt.ylabel('count')
plt.title('对象与count关系的条形图')
plt.xticks(rotation=45)
plt.tight_layout()

# 保存条形图
chart_filename = f"chart_{current_time}.png"
plt.savefig(chart_filename)

print(f"表格已保存为 {table_filename}")
print(f"条形图已保存为 {chart_filename}")
