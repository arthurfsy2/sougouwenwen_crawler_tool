import requests
import argparse
import re
from bs4 import BeautifulSoup
import html2text

parser = argparse.ArgumentParser()
parser.add_argument("base_url", help="输入帖子地址")
    
options = parser.parse_args()
    
url = options.base_url


#url = "https://wenwen.sogou.com/question/q276428073.htm?ch=ww.grzx.wdhdques"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
}

response = requests.get(url, headers=headers)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")

# 检查是否找到了标题标签
title_tag = soup.title
if title_tag:
    title = title_tag.text
else:
    title = ""

# 如果标题超过30个字符，则截取前50个字符并添加"..."作为文件名
if len(title) > 30:
    file_name = title[:30] + "..."
else: file_name = title


# 提取用户信息
user_info_tags = soup.find_all("div", class_="user-name-box")
user_contents = [user_info.find("a", class_="user-name").text if user_info.find("a", class_="user-name") else "匿名用户" for user_info in user_info_tags]





# 提取问题内容
question_tag = soup.find("pre", class_="detail-tit-info")
question_content = ""
if question_tag:
    html = str(question_tag)
    #print(f"question_content_html:{html}--end\n\n\n\n")
    markdown = html2text.html2text(html)
    #print(f"question_tag_markdown:{markdown}--end\n\n\n\n")
    markdown = re.sub('\r|\n| ', '', markdown)
    markdown = re.sub('!\[\]\((.*?)\)', r'\n![](\1)\n', markdown)
    question_content=markdown
else:
# 如果问题详情为空，则取标题描述作为问题内容
    question_content = title


# 判断问题是否存在图片标签
question_image_tag = soup.find("div", id="question_images")
if question_image_tag:
    # 提取所有符合条件的s-src链接
    s_src_list = re.findall(r's-src="(.*?)"', str(question_image_tag))
    #带有"wapm-"参数的图片会在网页上隐藏，去掉后即可显示图片
    s_src_list = [s_src.replace("wapm-", "") for s_src in s_src_list]
    print(f"s_src_list：{s_src_list}")
    # 转换为Markdown格式的链接，图片链接加上“/0”即可显示
    markdown_links = [f"![]({s_src}/0)" for s_src in s_src_list]
    # 合并为一个输出，以\n分隔每个链接
    question_picUrl = "\n\n".join(markdown_links)
    

else:
    question_picUrl = ""
print(f"问题图片链接:{question_picUrl}")



answer_tags = soup.find_all("pre", class_="replay-info-txt answer_con")
answer_contents = []
for answer in answer_tags:
    html = str(answer)
    markdown = html2text.html2text(html)
    #print(f"markdown:{markdown}--end\n\n\n\n")
    markdown = re.sub('\r|\n| ', '', markdown)
    markdown = re.sub('!\[\]\((.*?)\)', r'\n![](\1)\n', markdown)
    answer_contents.append(markdown)


# 提取回答内容和日期
dates = soup.find_all("div", class_="user-txt")

question_dates = []
answer_dates = []

#判断该日期是提问的日期还是回答的日期
for date in dates:
    if "提问" in date.text:
        question_dates = date.text
    elif "回答" in date.text:
        answer_dates.append(date.text)
        
# 替换文件名中无效字符和换行符为空格
file_name = re.sub(r'[<>:"/\\|?*\n]', ' ', file_name)

# 替换原标题的换行符为空格
title = re.sub(r'[\n]', ' ', title)

output_path = f"./Download/{file_name}.md"  # 定义output.md的存放路径
# 将提取的内容保存为.md文件
with open(output_path, 'w', encoding='utf-8') as file:

    print(f"title:{title}--结束")
    file.write(f"## [{file_name}]({url})\n\n")
    file.write(f"**{user_contents[0]}**\n{question_dates}\n> {question_content}\n\n{question_picUrl}\n\n")
    i=0
    for i in range(len(answer_dates)):
        file.write(f"---\n")
        file.write(f"**{user_contents[i+1]}**\n{answer_dates[i]}\n> {answer_contents[i]}\n\n")

    file.write(f"---\n")

print(f'****已完成"{file_name}"的备份***\n')

