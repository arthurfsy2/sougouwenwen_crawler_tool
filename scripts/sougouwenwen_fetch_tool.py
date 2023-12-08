import http.client
http.client._MAXHEADERS = 1000
import requests
import argparse
import re
from bs4 import BeautifulSoup
import html2text
import json
import os

with open("scripts/config.json", "r") as file:
    data = json.load(file)

questionUrl = data["questionUrl"]
questionPageNum = data["questionPageNum"]
answerUrl = data["answerUrl"]
answerPageNum = data["answerPageNum"]
Cookie = data["Cookie"]
nickname = data["nickname"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
    "Cookie":Cookie
}

def createListMD(pageNum,type,url,headers):
    id_all = []
    content_all=""
    count = 0
    while count < pageNum:
        num = (count)*20
        pattern = f"start=(.*?)&"
        match = re.search(pattern, url)
        if match:
            init_num = match.group(1)  
        url_new = url.replace(f"start={init_num}",f"start={num}")
        print(f"已抓取{type}列表{count+1}/{pageNum}")
        pageContent = getList(type,url_new,headers)
        content_all += pageContent
        count += 1
    if type =="question":
        mdtitle = "提问"
    else: 
        mdtitle = "回答"
    with open("./template/list_template.md","r",encoding="utf-8") as f:
        data = f.read()
        data = data.replace("$nickname",nickname)
        data = data.replace("$mdtitle",mdtitle)
        data = data.replace("$list_content",content_all)
    with open(f"./output/list_{type}.md","w",encoding="utf-8") as f:
        f.write(data)
    print(f"已生成./output/list_{type}.md")
    print(f"——————————————————")
    


def getList(type,url,headers):
    
    response = requests.get(url=url,headers=headers).json()["questions"]
    list_content=""
    
    for item in response:
        id = item["id"]
        title_init = item["title"]
        baseurl = f"https://wenwen.sogou.com/question/q{id}.htm"
        createTimeStr = item["createTimeStr"]
        score = item["score"]
        pv = item["pv"]
        answerNum = item["answerNum"]
        tag =  item["tags"][0]["tagName"]
        tagIds = item["tags"][0]["tagId"]
        
        if type == "question":
            title = f"- [🏅{score} {title_init}]({baseurl}?ch=ww.grzx.wdtwques) {createTimeStr}发布 `{pv}人看过` [``{tag}``](https://wenwen.sogou.com/cate/tag?tagId={tagIds})\n\n> {answerNum}个回答 [`查看处理`]({baseurl}?ch=ww.grzx.ckcl)\n\n"
        elif type == "answer":
            createTimeStr = item["myAnswer"]["createTimeStr"]
            
            isAdopted = item["myAnswer"]["daren"]
            if isAdopted == False:
                isAdopted = "🕓等待采纳"
            else:
                isAdopted = "🏅最佳答案"
            title = f"- [ {title_init}]({baseurl}?ch=ww.grzx.wdtwques) {createTimeStr}发布 [``{tag}``](https://wenwen.sogou.com/cate/tag?tagId={tagIds}) {isAdopted}\n\n"
        list_content+=title
    return list_content
    
def getListContent(type,url,headers):
    
    response = requests.get(url=url,headers=headers).json()["questions"]
    id_list = []
    list_content=""
    
    for item in response:
        id = item["id"]
        id_list.append(id)
        title_init = item["title"]
        baseurl = f"https://wenwen.sogou.com/question/q{id}.htm"
        createTimeStr = item["createTimeStr"]
        score = item["score"]
        pv = item["pv"]
        answerNum = item["answerNum"]
        tag =  item["tags"][0]["tagName"]
        tagIds = item["tags"][0]["tagId"]
        content = parseContent(type,baseurl,title_init,createTimeStr,score,pv)
        list_content+=content
    return list_content

def createMergeMD(pageNum,type,url,headers):
    id_all = []
    content_all=""
    count = 0
    while count < pageNum:
        num = (count)*20
        pattern = f"start=(.*?)&"
        match = re.search(pattern, url)
        if match:
            init_num = match.group(1)  
        url_new = url.replace(f"start={init_num}",f"start={num}")
        print(f"已抓取{type}列表{count+1}/{pageNum}")
        pageContent = getListContent(type,url_new,headers)
        content_all += pageContent
        count += 1
    if type =="question":
        mdtitle = "提问"
    else: 
        mdtitle = "回答"
    with open("./template/merge_template.md","r",encoding="utf-8") as f:
        data = f.read()
        data = data.replace("$nickname",nickname)
        data = data.replace("$mdtitle",mdtitle)
        data = data.replace("$list_content",content_all)
    with open(f"./output/merge_{type}.md","w",encoding="utf-8") as f:
        f.write(data)
    print(f"已生成./output/merge_{type}.md")
    print(f"——————————————————")
    download_pic(data, type)


def download_pic(data, type):
    save_dir = r'./output/PicDownload'
    image_urls = re.findall(r'!\[\]\((.*?)\)', data)
    print(image_urls)
    for url in image_urls:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = url.replace('wapm-', '')
            if url.endswith('/0'):
                image_name = url.replace('/0', '.jpg').split('/')[-1]
                #print("image_name:\n",image_name) 
            else:
                image_name = url.split('/')[-1]
            #print(f"image_name: {image_name}")
            save_path = os.path.join(save_dir, image_name)
            with open(save_path, 'wb') as image_file:
                image_file.write(response.content)
                print(f'已下载图片: {save_path}')
            content = data.replace(f"{url}",f"{save_dir}/{image_name}")
            # print(f'已将: {url}换为{save_dir}/{image_name}')
            print('————————————————————')
    with open(f"./output/merge_{type}_local.md", 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'已生成本地图片版：merge_{type}_local.md')

def parseContent(type,url,title_init,createTimeStr,score,pv):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
        }
    
    response = requests.get(url=url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    title = title_init
    # createTimeStr = response_old[i]["createTimeStr"]
    # score = response_old[i]["score"]
    # pv = response_old[i]["pv"]
    file_name = re.sub(r'[<>:"/\\|?*\n]', ' ', title_init)

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
        #print(f"s_src_list：{s_src_list}")
        # 转换为Markdown格式的链接，图片链接加上“/0”即可显示
        markdown_links = [f"![]({s_src}/0)" for s_src in s_src_list]
        # 合并为一个输出，以\n分隔每个链接
        question_picUrl = "\n\n".join(markdown_links)
        
    else:
        question_picUrl = ""
    #print(f"问题图片链接:{question_picUrl}")


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
    # question_dates = f"{pv} 次浏览 | {createTimeStr}提问 🏅{score}"
    # answer_dates = f"{pv} 次浏览 | {createTimeStr}提问"
    
    #判断该日期是提问的日期还是回答的日期
    answer_dates=[]
    for date in dates:
        if "提问" in date.text:
            question_dates = date.text
        elif "回答" in date.text:
            answer_dates.append(date.text)
    title = re.sub(r'[\n]', ' ', title)

 
            
    sub_content =""
    for i in range(len(answer_dates)):
        content=f"---\n"\
                f"**{user_contents[i+1]}**\n{answer_dates[i]}\n> {answer_contents[i]}\n\n" 
                
        sub_content+=content
    content = f"### [{file_name}]({url})\n\n" \
            f"**{user_contents[0]}**\n{question_dates}\n> {question_content}\n\n{question_picUrl}\n\n" \
            f'{sub_content}' \
            f"---\n"
    
    output_path = f"./Download_{type}/{file_name}.md"  # 定义output.md的存放路径
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'****已完成"{file_name}"的备份***\n')
    return content


createListMD(questionPageNum,"question",questionUrl,headers)
createListMD(answerPageNum,"answer",answerUrl,headers)
createMergeMD(questionPageNum,"question",questionUrl,headers)
createMergeMD(answerPageNum,"answer",answerUrl,headers)