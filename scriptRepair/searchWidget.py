import xml.etree.ElementTree as ET

'''
                                    根据传入的信息在xml文件中确定点击该小部件的唯一方法
'''

xml_file_path = 'target_version_xml.xml'
search_str = ''''''
final_path = ''
final_way = ''
final_flag = True
attribute_dict = {}
path_flag = True


def get_root():
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    return root


def find_way_to_locate_widget(node, search_string):
    global final_path
    global final_way
    global final_flag
    global attribute_dict
    global path_flag
    attribute_flag = True
    # 处理search_string
    search_mode = search_string.split('=')[0].strip()
    search_info = search_string.split('=')[1].replace('"', '').strip()

    if path_flag:
        target_node = node.findall(f'.//*[@{search_string}]')
        if target_node:
            tag_name = target_node[0].get('class')
            # 查找与目标节点同名的节点
            matching_tags = node.findall(f'.//{tag_name}')
            tag_index = matching_tags.index(target_node[0])
            final_path = f'class="{tag_name},{tag_index}"'
        path_flag = False

    # 检查当前节点是否符合目标属性和值
    if target_node:
        if target_node[0].get('resource-id') is not None and target_node[0].get('resource-id') != '':
            attribute_dict['resource-id'] = target_node[0].get('resource-id')
        if target_node[0].get('content-desc') is not None and target_node[0].get('content-desc') != '':
            attribute_dict['content-desc'] = target_node[0].get('content-desc')
        if target_node[0].get('text') is not None and target_node[0].get('text') != '':
            attribute_dict['text'] = target_node[0].get('text')

        if attribute_dict:
            for key, value in attribute_dict.items():
                target_nodes = node.findall(f".//*")
                filtered_nodes = [node for node in target_nodes if node.get(key) == value]
                if len(filtered_nodes) == 1:
                    final_way = f'{key}="{value}"'
                    final_flag = True
                    attribute_flag = False
                    break
                else:
                    continue

            if attribute_flag:
                final_flag = False
        else:
            final_flag = False

    if final_flag:
        return final_way
    else:
        return final_path


