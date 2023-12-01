import os
import re
import requests

def download_images_from_md(md_file, save_dir):
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()
        image_urls = re.findall(r'!\[\]\((.*?)\)', content)
        print(image_urls)
        for url in image_urls:
            response = requests.get(url)
            
            if response.status_code == 200:
                image_name = url.replace('wapm-', '')
                if url.endswith('/0'):
                    image_name = url.replace('/0', '.jpg').split('/')[-1]
                else:
                    image_name = url.split('/')[-1]
                #print(f"image_name: {image_name}")
                save_path = os.path.join(save_dir, image_name)
                with open(save_path, 'wb') as image_file:
                    image_file.write(response.content)
                    print(f'已下载图片: {save_path}')

# 示例用法
merge_question = r'./output/merge_question.md'  # 替换为实际的.md文件路径
merge_answer = r'./output/merge_answer.md'  # 替换为实际的.md文件路径
save_dir = r'./PicDownload'  # 替换为实际的保存目录路径
download_images_from_md(merge_question, save_dir)
download_images_from_md(merge_answer, save_dir)
