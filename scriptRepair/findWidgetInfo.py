import sys
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from PIL import Image
import GUIencoding

'''
                                    通过分析输入的代码行，获得代码行中要点击的小部件的信息
'''
# 将代码行传给input_str变量，将路径传给两个file_path
xml_file_path = 'source_version_xml.xml'
xml_encoding_file_path = 'source_version_xml_encoding.html'
image_file_path = ''
image_save_path = 'source_version_widget_image.png'
class_number = 0
source_version_widget_html = ''
img_exist_flag = False
source_widget_file_path = 'source_widget_xml_encoding.html'


# 获得测试脚本代码行所要点击的小部件信息
def get_widget_info(code_str):
    founds = []
    global class_number
    global source_version_widget_html
    if 'CLASS_NAME' in code_str:
        class_matches = re.search(r'\[(\d+)\]$', code_str)
        class_number = int(class_matches.group(1))
        code_str = re.sub(r'\[\d+\]$', '', code_str)
        pattern_code = r"find_elements\((.+?),\s*\"(.+?)\"\)"
    else:
        pattern_code = r"find_element\((.+?),\s*\"(.+?)\"\)"
    pattern_xpath = r"\bcontains\(@text, '(.+?)'\)"
    matches_code = re.findall(pattern_code, code_str)
    if len(matches_code) > 0:
        extracted_code_str = matches_code[0]
        extracted_text = extracted_code_str[1].replace('"', '').strip()

        pattern_str = extracted_code_str[0]
        info_str = extracted_text
        if 'ID' in pattern_str and 'ACCESSIBILITY_ID' not in pattern_str:  # 需要修改，有的resourceid值的格式不是包名:id/值
            split_text = info_str.split(':')
            info_str = split_text[1].strip()
    else:
        print('Error happened')
        sys.exit()

    if 'ID' in pattern_str or 'CLASS_NAME' in pattern_str or 'ACCESSIBILITY_ID' in pattern_str:
        founds = search_string_in_html_file(xml_encoding_file_path, pattern_str, info_str)
    elif 'XPATH' in pattern_str:
        if 'text' in info_str:
            matches_xpath = re.search(pattern_xpath, info_str)
            if matches_xpath:
                text_info = matches_xpath.group(1)
                founds = search_string_in_html_file(xml_encoding_file_path, pattern_str, text_info)
            else:
                print("WRONG!!!")
                sys.exit()
        else:
            print('text WRONG!!!')
            sys.exit()

    if founds:
        found = founds[-1]
        tag, parent = found
        source_version_widget_html = parent
        with open(source_widget_file_path, 'w', encoding='utf-8') as file:
            file.write(str(source_version_widget_html))
    else:
        print("未找到符合条件的标签及其父节点")
        sys.exit()


# 在xml_encoding.html文件中搜索特定字符串
def search_string_in_html_file(html_file, pattern_string, search_string):
    global img_exist_flag
    global xml_file_path
    global image_file_path
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')  # 解析 HTML 文件

        img_tag = soup.find_all('img')
        button_tag = soup.find('button')
        # 查找所有符合条件的标签及其父节点
        mode_str = pattern_string.split('.')[-1]
        if mode_str == 'ID':
            tags = soup.select(f'[class*="{search_string}"]')
        elif mode_str == 'CLASS_NAME':
            if 'ImageView' in search_string and img_tag:
                tags = [img_tag[class_number]]
            elif 'TextView' in search_string and button_tag:
                tags = [button_tag[class_number]]  # 未完善！！！
        elif mode_str == 'ACCESSIBILITY_ID':
            tags = soup.select(f'[alt*="{search_string}"]')
        elif mode_str == 'XPATH':
            tags = soup.select(f':-soup-contains("{search_string}")')
        results = []

        for tag in tags:
            parent = tag.find_parent("div")  # 查找标签的父节点
            if parent:
                # 去除父节点的其他子节点，只保留匹配的标签及其内容
                parent.clear()
                parent.append(tag)
                # 将父节点和子节点添加到结果列表
                results.append((tag, parent))

        img_tag = tags[-1]
        if img_tag.name == 'img':
            img_exist_flag = True
        else:
            img_exist_flag = False
        GUIencoding.img_flag = img_exist_flag
        if img_exist_flag:
            search_widget_image_in_xml(xml_file_path, image_file_path, mode_str, search_string)
        return results


# 对xml文件进行编码时若所找寻的小部件是<img>则获取小部件的bounds属性从而获得小部件的图标图片
# 可以在对xml文件进行编码的同时对原xml文件进行修改，如果某节点被编码则加入被编码的id值，这样到时候找被点击的小部件时更高效方便
def search_widget_image_in_xml(xml_file, image_file, pattern_string, search_string):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    bounds_result = ''

    if pattern_string == 'ACCESSIBILITY_ID':
        for element in root.iter():
            if element.get('content-desc') is not None:
                if search_string in element.get('content-desc'):
                    bounds_result = element.get('bounds')
                    break
    elif pattern_string == 'ID':
        for element in root.iter():
            if element.get('resource-id') is not None:
                if search_string in element.get('resource-id'):
                    bounds_result = element.get('bounds')
                    break
    elif pattern_string == 'CLASS_NAME':
        for element in root.iter():
            if element.get('class') is not None:
                if search_string in element.get('class'):
                    bounds_result = element.get('bounds')
                    break
    elif pattern_string == 'XPATH':
        for element in root.iter():
            if element.get('text') is not None:
                if search_string in element.get('text'):
                    bounds_result = element.get('bounds')
                    break

    screenshot = Image.open(image_file)
    bounds = bounds_result.strip('[]')
    left_top, right_bottom = bounds.split('][')
    left, top = map(int, left_top.split(','))
    right, bottom = map(int, right_bottom.split(','))
    # 截取图像片段
    image_fragment = screenshot.crop((left, top, right, bottom))
    # 保存图像片段
    image_fragment.save(image_save_path)


