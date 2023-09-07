import re

# Read the .md file
with open(r"D:\web\Blog\src\Arthur\搜狗问问\我的提问.md", "r", encoding="utf-8") as file:
    content = file.read()

# Find all the URLs matching the pattern
urls = re.findall(r"https://wenwen\.sogou\.com/question/\w+.htm", content)

# Write the URLs to base_url.txt file
with open("./base_url_提问.txt", "w", encoding="utf-8") as file:
    for url in urls:
        file.write(url + "\n")
