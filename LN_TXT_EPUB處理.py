import re

# 讀取文件內容
with open('我是星際國家的惡德領主！ 5.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # Prepare for content.xhtml
    pattern = "CONTENTS\n(.*)\n序章"
    match = re.search(r"CONTENTS\n(.*?)\n\n", content, re.DOTALL)
    if match:
        specific_text = match.group(1)
        lines = specific_text.split("\n")
        contents_length = len(lines)
        html_lines = ["<p class='mulu'><a class='no-d' href='../Text/Section0.xhtml'>" + line + "</p>" for line in
                      lines]
        html_content = "\n".join(html_lines)

        # 寫入 .xhtml 文件
        with open(f'contents.xhtml', 'w', encoding='utf-8') as f:
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
            f.write("  <div class='bold illus1' style='margin: 2em 0 0 2em;'>\n")
            f.write(f"    <p class='contents title em12'><b>CONTENTS</b></p>\n")

            # write the contents of the chapter
            f.write(f'{html_content}')

            f.write("  </div>\n")
            f.write("</body>\n")
            f.write("</html>\n")

    # 內文處理
    # 使用正則表達式解析文件內容
    chapters = re.findall(r'(序章|第.話.*?\n|終章|特別篇.*?\n)(.*?)(?=序章|第.話|終章|特別篇|後記)', content, re.DOTALL)
    extra_chapter_1 = re.findall(r'(後記)(.*?)(?=『新人騎士』特典小冊子)', content, re.DOTALL)
    extra_chapter_2 = re.findall(r'(『新人騎士』特典小冊子)(.*?)(?=結束)', content, re.DOTALL)
    chapters.extend(extra_chapter_1)
    chapters.extend(extra_chapter_2)

    iteration = 0
    clear_blank_files = 0
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
            if iteration == contents_length and clear_blank_files == 0:
                iteration = 0
                clear_blank_files = 1 # 因為contents_length比實際上輸出的file數量小，所以覆蓋過一次空白檔案後設if為否避免後面的檔案輸出不了
