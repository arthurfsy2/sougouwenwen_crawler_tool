import re

# 手动复制个人中心提问/回答列表，用`Typora`打开在base_url.md，然后粘贴在该文件当中，会自动转换成markdown的格式

with open(r"./base_url.md", "r", encoding="utf-8") as file:
    content = file.read()

# 找到所有符合条件的链接
urls = re.findall(r"https://wenwen\.sogou\.com/question/\w+.htm", content)
# 对链接进行除重
urls = list(set(urls))

# Write the URLs to base_url.txt file
with open("./base_url.txt", "w", encoding="utf-8") as file:
    for url in urls:
        file.write(url + "\n")

print(f"已找到以下链接：\n{urls}\n")
print("已导出链接到base_url.txt")