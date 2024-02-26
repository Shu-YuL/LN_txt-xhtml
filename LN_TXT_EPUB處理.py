import re

# 讀取文件內容
with open('不時輕聲地以俄語遮羞的鄰座艾莉同學 6\不時輕聲地以俄語遮羞的鄰座艾莉同學 6.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # Prepare for content.xhtml
    pattern = "CONTENTS\n(.*)\n第.話"
    match = re.search(r"CONTENTS\n(.*?)\n\n", content, re.DOTALL)
    if match:
        specific_text = match.group(1)
        lines = specific_text.split("\n")
        contents_length = len(lines)
        html_lines = ["<p class='mulu'><a class='no-d' href='../Text/Section{}.xhtml'><span class='co0'>{}</span></a></p>".format(x, line) for x, line in enumerate(lines)]
        html_content = "\n".join(html_lines)

        # 寫入 .xhtml 文件
        with open(f'contents.xhtml', 'w', encoding='utf-8') as f:
            # 寫入 .xhtml 檔案內容
            f.write("<?xml version='1.0' encoding='utf-8' standalone='no'?>\n")
            f.write("<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\n")
            f.write("  'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n")
            f.write("\n")
            f.write(
                "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='zh-TW' xmlns:epub='http://www.idpf.org/2007/ops' xmlns:xml='http://www.w3.org/XML/1998/namespace'>\n")
            f.write("<head>\n")
            f.write("  <link href='../Styles/style.css' rel='stylesheet' type='text/css' />\n")
            f.write("\n")
            f.write("  <title></title>\n")
            f.write("</head>\n")
            f.write("\n")
            f.write("<body>\n")
            f.write("  <div class='bold illus1' style='margin: 2em 0 0 2em;'>\n")
            f.write(f"    <p class='contents title em12'><b>CONTENTS</b></p>\n")

            # write the contents of the chapter
            f.write(f'{html_content}')

            f.write("  </div>\n")
            f.write("</body>\n")
            f.write("</html>\n")

    # 內文處理
    # 使用正則表達式解析文件內容
    # 注意: (?! ...) 用處在於添加 negative lookahead assertion。結果only match if it's not followed by (...)
    chapters = re.findall(r'(序章.*?\n|第.{1,3}話.*?\n|第.{1,3}章　.*?\n|epilogue.*?\n|番外篇.*?\n|終章.*?\n|單行本特典.*?\n|特別篇.*?\n)(?!序章|第.{1,3}話|第.{1,3}章|終章|特別篇|epilogue|單行本特典|番外篇　|後記)(.*?)(?=序章|第.{1,3}話|第.{1,3}章|終章|特別篇|epilogue|單行本特典|番外篇　|後記)', content, re.DOTALL)
    # 由於第一個item依然是多餘的，Remove the first item and shift all succeeding items up by one index
    chapters = chapters[1:]
    extra_chapter_1 = re.findall(r'(後記\n)(?!後記的後記SS)(.*?)(?=後記的後記SS　百合會拯救世界)', content, re.DOTALL)
    extra_chapter_2 = re.findall(r'(後記的後記SS　百合會拯救世界)(?!.*?序章)(.*?)(?=結束END)', content, re.DOTALL)
    chapters.extend(extra_chapter_1)
    chapters.extend(extra_chapter_2)

    iteration = 0
    # 將每個章節轉換為 .xhtml 文件
    for chapter in chapters:
        chapter_name, chapter_content = chapter[0], chapter[1]
        lines = chapter_content.split("\n")
        html_lines = ["<p>" + line + "</p>" for line in lines]
        html_content = "\n".join(html_lines)
        html_content = re.sub(r'<p></p>', '<p><br/></p>', html_content)
        html_content = re.sub(r'<p>（插圖(.*?)）</p>',
                              r'<div class="illus duokan-image-single"><img alt="\1" src="../Images/\1.jpg"/></div><p><br/></p>',
                              html_content)
        # 寫入 .xhtml 文件
        with open(f'Section{iteration}.xhtml', 'w', encoding='utf-8') as f:
            # 寫入 .xhtml 檔案內容
            f.write("<?xml version='1.0' encoding='utf-8' standalone='no'?>\n")
            f.write("<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\n")
            f.write("  'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n")
            f.write("\n")
            f.write(
                "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='zh-CN' xmlns:epub='http://www.idpf.org/2007/ops' xmlns:xml='http://www.w3.org/XML/1998/namespace'>\n")
            f.write("<head>\n")
            f.write("  <link href='../Styles/style.css' rel='stylesheet' type='text/css' />\n")
            f.write("\n")
            f.write("  <title></title>\n")
            f.write("</head>\n")
            f.write("\n")
            f.write("<body>\n")
            f.write("  <div>\n")
            f.write(f"    <p class='pius1'>{chapter_name}</p>\n")

            # write the contents of the chapter
            f.write(f'{html_content}')

            f.write("  </div>\n")
            f.write("</body>\n")
            f.write("</html>\n")

            iteration += 1
            # 由於上述更改，已經不需要覆蓋空白檔案了，chapters皆為有效chapter
