一个可以批量爬取指定搜狗问问问题链接，下载并转换为.md格式的python脚本。

（一个关于你青春黑历史的备份）

特点：

1、可识别 `wenwen.sogou.com/question/XXX`的内容

2、可抓取提问、回答的图片，并将官网屏蔽不显示的图片展示出来（详见 `sougouwenwen_fetch_tool`的 `wapm-注释`）

注：
1、本项目仅用于个人搜狗问问的个人提问、回答内容的备份

使用：

1. 在 `base_url.txt`文件内填入需要备份的链接，`wenwen.sogou.com/question/XXX`或 `wenwen.sogou.com/z/XXX`格式，且一行只能有一个地址。以下仅为示意参考：

```
https://wenwen.sogou.com/z/q1713280989.htm?ch=ww.sy.wwzl
https://wenwen.sogou.com/question/q1227625514349824078.htm?ch=ww.sy.tj&pid=ww.sy.tj
```

2. 在项目当前目录运行 `py multi_sougouwenwen_spy.py`即可将结果下载并处理为.md格式，并保存到 `Download`文件夹
   注意：本脚本设置了间隔1秒钟再备份下一个地址（防止封IP）
   可以修改以下代码的time.sleep(1)的数字，或者直接注释掉 `time.sleep(10)`该行

```
for url in base_url:
    print(f'命令：py "tieba_fetch_tool.py" {url}')
    command = f'py {tool_path} "{url}"'
    subprocess.run(command)
    time.sleep(10)  # 在每次循环后等待N秒，防止封IP
```

可选功能：

1. 批量获取[问问个人中心](https://wenwen.sogou.com/user/center/)的各个提问/回答页面的base_url地址
   * 手动复制个人中心提问/回答列表，用 `Typora`打开在base_url.md，然后粘贴在该文件当中，会自动转换成markdown的格式
   * 运行 `py base_url_extract.py`，通过 `base_url_extract.py`获取并导出链接到 `base_url.txt`。
2. 批量添加frontmatter（配合vuepress使用，可将处理后的.md作为vuepress的页面展示）
   运行 `py ADDfrontmatter.py`，即可将添加好frontmatter内容的文件添加到 `Download2`文件夹
3. 批量将多个.md文件合并为一个.md文件
   运行 `PY mergeMD.py`，即可将多个.md文件合并为merge.md，并添加到 `Download2`文件夹
4. 下载markdown文件内所有 `![](xxx.jpg)`的图片
   运行 `PY mdPicDownload.py`，即可批量下载图片到 `PicDownload`文件夹。（需要在 `mdPicDownload.py`内设置需要读取的markdown文件路径。
