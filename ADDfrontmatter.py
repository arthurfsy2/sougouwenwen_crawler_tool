import os

input_path = "./Download_我的提问"  # 替换为实际的源目录路径
output_path = "./我的提问"  # 替换为实际的目标目录路径

for filename in os.listdir(input_path):
    if filename.endswith(".md"):
        file_input_path = os.path.join(input_path, filename)
        file_output_path = os.path.join(output_path, filename)
        title = os.path.splitext(filename)[0]  # 获取文件名并去除扩展名
        with open(file_input_path, "r",encoding='utf-8') as fileA:
            content = fileA.read()
            new_content = f'---\ntitle: {title}\nicon: "pencil"\ncategory:\n  - Arthur\ntag:\n  - 搜狗问问\n---\n\n{content}'
        with open(file_output_path, "w",encoding='utf-8') as fileB:
            fileB.write(new_content)
