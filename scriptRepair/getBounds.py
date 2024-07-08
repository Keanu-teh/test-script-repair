import xml.etree.ElementTree as ET

'''
                                    获取swipe函数所需要的bounds属性
'''

xml_file_path = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/xmlSimilarity/test.xml' # 对source version的xml文件进行编码后得到的source version xml文件


def find_node_bounds(xml_file, search_string):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    search_mode = search_string.split('=')[0].replace(' ', '')
    search_info = search_string.split('=')[1].replace('"', '')

    for node in root.iter():
        if search_mode in node.attrib and node.attrib[f'{search_mode}'] == search_info:
            if 'bounds' in node.attrib:
                bounds = node.attrib['bounds']
                return bounds

    return None


