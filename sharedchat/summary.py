import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 用户输入JSON文件路径
json_file_path = input("请输入要整理的JSON文件路径：")

# 读取JSON文件
with open(json_file_path, 'r') as file:
    data = json.load(file)

# 创建一个空的DataFrame
df = pd.DataFrame(columns=["对象", "count"])

# 解析JSON数据并添加到DataFrame中
for key, value in data["account"].items():
    df = df.append({"对象": key, "count": value["count"]}, ignore_index=True)

# 生成表格并保存为CSV文件
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file_name = f"data_{timestamp}.csv"
df.to_csv(csv_file_name, index=False)

# 生成条形图
plt.bar(df["对象"], df["count"])
plt.xlabel("对象")
plt.ylabel("count")
plt.title("对象与count关系")
plt.xticks(rotation=45)
plt.tight_layout()

# 保存条形图为图片文件
image_file_name = f"bar_chart_{timestamp}.png"
plt.savefig(image_file_name)

# 显示条形图
plt.show()

print(f"表格已保存为: {csv_file_name}")
print(f"条形图已保存为: {image_file_name}")
