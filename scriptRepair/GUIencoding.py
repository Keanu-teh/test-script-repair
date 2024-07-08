import xml.etree.ElementTree as ET
import iconSimilarity
from collections import deque


'''
                                    将xml文件编码成html的形式(对于旧版本新版本的xml编码不一样，因为新版本需要将title编码进去)
'''

# XML文件和UI截图路径(代码完成时需要从其他.py文件中获得变量来替代以下变量)
old_div_flag = {}
new_div_flag = {}
new_xml_id = {}
old_xml_id = {}
image_file_path = ''
img_flag = False
old_root_flag = False
new_root_flag = False


class TreeNode:
    def __init__(self, label, text=None, resourceid=None, description=None, bounds=None, scrollable=None, width=None, height=None, id=None):
        self.label = label
        self.text = text
        self.resourceid = resourceid
        self.description = description
        self.bounds = bounds
        self.scrollable = scrollable
        self.width = width
        self.height = height
        self.id = id
        self.children = []
        self.number = None  # 用于存储标号的属性


def parse_xml_tree_new(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return build_tree_new(root)


def parse_xml_tree_old(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return build_tree_old(root)


def build_tree_new(xml_element):
    if xml_element.tag == 'hierarchy':
        node = TreeNode(xml_element.tag, id=xml_element.get('id'))
    else:
        node = TreeNode(xml_element.tag, text=xml_element.get('text'), resourceid=xml_element.get('resource-id'),
                        description=xml_element.get('content-desc'), bounds=xml_element.get('bounds'), id=xml_element.get('id'))
    new_xml_id[f'{xml_element.get("id")}'] = xml_element.get('id')
    for child in xml_element:
        node.children.append(build_tree_new(child))

    return node


def build_tree_old(xml_element):
    if xml_element.tag == 'hierarchy':
        node = TreeNode(xml_element.tag, id=xml_element.get('id'))
    else:
        node = TreeNode(xml_element.tag, text=xml_element.get('text'), resourceid=xml_element.get('resource-id'),
                        description=xml_element.get('content-desc'), bounds=xml_element.get('bounds'), id=xml_element.get('id'))
    old_xml_id[f'{xml_element.get("id")}'] = xml_element.get('id')
    for child in xml_element:
        node.children.append(build_tree_old(child))

    return node


def change_xml_new(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element in root.iter():
        if element.get('id') != new_xml_id[f'{element.get("id")}']:
            new_value = new_xml_id[f'{element.get("id")}']
            element.set('id', f'{new_value}')

    tree.write('target_version_xml.xml')


def change_xml_old(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element in root.iter():
        if element.get('id') != old_xml_id[f'{element.get("id")}']:
            new_value = old_xml_id[f'{element.get("id")}']
            element.set('id', f'{new_value}')

    tree.write('source_version_xml.xml')


def find_parent_node_by_id(root, target_id):
    # 检查当前节点的子节点是否包含目标节点
    for child in root.children:
        if child.id == target_id:
            return root

    # 递归搜索子节点
    for child in root.children:
        parent = find_parent_node_by_id(child, target_id)
        if parent:
            return parent

    # 如果没有找到目标节点，返回None
    return None


# xml tree编码
def xml_to_html_target_version(node):
    tree = node
    # 递归地将XML元素转换为HTML代码
    html = depth_traverse_output_html_target_version(tree, node, indent_level=0)

    return html


def xml_to_html_source_version(node):
    tree = node
    # 递归地将XML元素转换为HTML代码
    html = depth_traverse_output_html_source_version(tree, node, indent_level=0)

    return html


def breadth_first_traversal_target_version(root):
    global new_root_flag
    queue = deque([(root, "")])

    while queue:
        node, parent_number = queue.popleft()
        has_children = len(node.children) > 0

        if node.label == 'hierarchy':
            new_root_flag = True

        # 将当前节点的子节点添加到队列，并传递当前节点的标号作为父节点的标号
        if new_root_flag:
            if len(node.children) > 1:
                for i, child in enumerate(node.children):
                    child_number = f"{i+1}"
                    queue.append((child, child_number))
                new_root_flag = False
            else:
                for i, child in enumerate(node.children):
                    child_number = ' '
                    queue.append((child, child_number))
        elif has_children:
            if len(node.children) > 1:
                node.number = parent_number
                for i, child in enumerate(node.children):
                    child_number = f"{node.number}_{i+1}"
                    queue.append((child, child_number))
            else:
                for i, child in enumerate(node.children):
                    child_number = parent_number
                    queue.append((child, child_number))

        if has_children:
            if len(node.children) > 1 and node.bounds != node.children[0].bounds:
                node.number = parent_number if parent_number else "None"
                new_xml_id[node.id] = node.number
            elif ('TextView' in node.label or ('Button' in node.label and node.text != '')) and len(node.children) != 1:
                node.number = parent_number if parent_number else "None"
                new_xml_id[node.id] = node.number
            elif ('ImageView' in node.label or 'Button' in node.label) and len(node.children) != 1:
                node.number = parent_number if parent_number else "None"
                new_xml_id[node.id] = node.number
        else:
            if 'TextView' in node.label or ('Button' in node.label and node.text != ''):
                node.number = parent_number if parent_number else "None"
                new_xml_id[node.id] = node.number
            elif 'ImageView' in node.label or 'Button' in node.label:
                node.number = parent_number if parent_number else "None"
                new_xml_id[node.id] = node.number


def breadth_first_traversal_source_version(root):
    global old_root_flag
    queue = deque([(root, "")])

    while queue:
        node, parent_number = queue.popleft()
        has_children = len(node.children) > 0

        if node.label == 'hierarchy':
            old_root_flag = True

        # 将当前节点的子节点添加到队列，并传递当前节点的标号作为父节点的标号
        if old_root_flag:
            if len(node.children) > 1:
                for i, child in enumerate(node.children):
                    child_number = f"{i+1}"
                    queue.append((child, child_number))
                old_root_flag = False
            else:
                for i, child in enumerate(node.children):
                    child_number = ' '
                    queue.append((child, child_number))
        elif has_children:
            if len(node.children) > 1:
                node.number = parent_number
                for i, child in enumerate(node.children):
                    child_number = f"{node.number}_{i+1}"
                    queue.append((child, child_number))
            else:
                for i, child in enumerate(node.children):
                    child_number = parent_number
                    queue.append((child, child_number))

        if has_children:
            if len(node.children) > 1 and node.bounds != node.children[0].bounds:
                node.number = parent_number if parent_number else "None"
                old_xml_id[node.id] = node.number
            elif ('TextView' in node.label or ('Button' in node.label and node.text != '')) and len(node.children) != 1:
                node.number = parent_number if parent_number else "None"
                old_xml_id[node.id] = node.number
            elif ('ImageView' in node.label or 'Button' in node.label) and len(node.children) != 1:
                node.number = parent_number if parent_number else "None"
                old_xml_id[node.id] = node.number
        else:
            if 'TextView' in node.label or ('Button' in node.label and node.text != ''):
                node.number = parent_number if parent_number else "None"
                old_xml_id[node.id] = node.number
            elif 'ImageView' in node.label or 'Button' in node.label:
                node.number = parent_number if parent_number else "None"
                old_xml_id[node.id] = node.number


# new version
def depth_traverse_output_html_target_version(tree, node, indent_level):
    global new_div_flag
    img_resourceid_flag = True
    img_description_flag = True
    img_text_flag = True
    # 处理元素标签
    html = ''
    # 检查是否有子元素
    has_children = len(node.children) > 0
    div_symbol = False

    if node.label == 'hierarchy':
        indent = " " * indent_level * 2
        html += f'{indent}<html>\n<body>\n'
        indent_level += 1
    elif node.number is not None:
        if has_children:
            if node.bounds != node.children[0].bounds and len(node.children) > 1:
                first_child = node.children[0]
                last_child = node.children[len(node.children) - 1]
                first_child_bottom = first_child.bounds.strip('[]').split('][')[-1]
                last_child_bottom = last_child.bounds.strip('[]').split('][')[-1]
                last_child_top = last_child.bounds.strip('[]').split('][')[0]
                last_child_top_y = int(last_child_top.split(',')[-1])
                first_child_bottom_y = int(first_child_bottom.split(',')[-1])
                last_child_bottom_y = int(last_child_bottom.split(',')[-1])
                indent = " " * indent_level * 2
                div_symbol = True
                if (last_child_bottom_y - first_child_bottom_y) < (last_child_bottom_y - last_child_top_y):
                    html += f'{indent}<div id="{node.number}" style="display:flex">\n'
                else:
                    html += f'{indent}<div id="{node.number}">\n'
                new_div_flag[f'{node.label}_{node.number}'] = True
                indent_level += 1
        else:
            if 'TextView' in node.label or ('Button' in node.label and node.text != ''):
                indent = " " * indent_level * 2
                html += f'{indent}<button id="{node.number}"'
                if node.resourceid is not None:
                    if ':id/' in node.resourceid:
                        split_text = node.resourceid.split(':')
                        word = split_text[1].strip()
                    else:
                        word = node.resourceid
                if node.resourceid is not None and node.resourceid != '':
                    html += f' class="{word}"'
                if node.description is not None and node.description != '':
                    html += f' alt="{node.description}"'
                html += f'> {node.text} </button>\n'
                indent_level += 1
            elif 'Image' in node.label or 'Button' in node.label:
                indent = " " * indent_level * 2
                html += f'{indent}<img id="{node.number}"'
                if node.resourceid is not None:
                    split_text = node.resourceid.split(':')
                    if len(split_text) > 1:
                        word = split_text[1].strip()
                    else:
                        word = split_text[0].strip()
                if node.resourceid is not None:
                    html += f' class="{word}"'
                    img_resourceid_flag = False
                if node.description is not None:
                    html += f' alt="{node.description}"'
                    img_description_flag = False
                if node.text is not None and node.text != '':
                    html += f' text="{node.text}"'
                    img_text_flag = False
                    if img_resourceid_flag and img_description_flag and img_text_flag:
                        parent_node = find_parent_node_by_id(tree, node.id)
                        if parent_node:
                            if parent_node.resourceid is not None:
                                split_text = node.resourceid.split(':')
                                if len(split_text) > 1:
                                    word = split_text[1].strip()
                                else:
                                    word = split_text[0].strip()
                            if parent_node.resourceid is not None and parent_node.resourceid != '':
                                html += f' class="{word}"'
                            if parent_node.description is not None and parent_node.description != '':
                                html += f' alt="{parent_node.description}"'
                            if parent_node.text is not None and parent_node.text != '':
                                html += f' text="{parent_node.text}"'
                if img_flag:
                    html += f' title="{iconSimilarity.get_title_value(node.bounds, image_file_path)}" />\n'
                else:
                    html += ' />\n'
                indent_level += 1

    if has_children:
        for child in node.children:
            html += depth_traverse_output_html_target_version(tree, child, indent_level)

    # 处理结束标签
    if has_children:
        if node.label == 'hierarchy':
            html += f'</body>\n{indent}</html>'
        elif f'{node.label}_{node.number}' in new_div_flag and new_div_flag[f'{node.label}_{node.number}'] and div_symbol:
            html += f'{indent}</div>\n'

    return html


# old version
def depth_traverse_output_html_source_version(tree, node, indent_level):
    global old_div_flag
    img_resourceid_flag = True
    img_description_flag = True
    img_text_flag = True
    # 处理元素标签
    html = ''
    # 检查是否有子元素
    has_children = len(node.children) > 0
    div_symbol = False

    if node.label == 'hierarchy':
        indent = " " * indent_level * 2
        html += f'{indent}<html>\n<body>\n'
        indent_level += 1
    elif node.number is not None:
        if has_children:
            if node.bounds != node.children[0].bounds and len(node.children) > 1:
                # 是否需要对View和ViewGroup类型的节点进行编码处理？
                first_child = node.children[0]
                last_child = node.children[len(node.children) - 1]
                first_child_bottom = first_child.bounds.strip('[]').split('][')[-1]
                last_child_bottom = last_child.bounds.strip('[]').split('][')[-1]
                last_child_top = last_child.bounds.strip('[]').split('][')[0]
                last_child_top_y = int(last_child_top.split(',')[-1])
                first_child_bottom_y = int(first_child_bottom.split(',')[-1])
                last_child_bottom_y = int(last_child_bottom.split(',')[-1])
                indent = " " * indent_level * 2
                div_symbol = True
                if (last_child_bottom_y - first_child_bottom_y) < (last_child_bottom_y - last_child_top_y):
                    html += f'{indent}<div id="{node.number}" style="display:flex">\n'
                else:
                    html += f'{indent}<div id="{node.number}">\n'
                old_div_flag[f'{node.label}_{node.number}'] = True
                indent_level += 1
        else:
            if 'TextView' in node.label or ('Button' in node.label and node.text != ''):
                indent = " " * indent_level * 2
                html += f'{indent}<button id="{node.number}"'
                if node.resourceid is not None:
                    if ':id/' in node.resourceid:
                        split_text = node.resourceid.split(':')
                        word = split_text[1].strip()
                    else:
                        word = node.resourceid
                if node.resourceid is not None:
                    html += f' class="{word}"'
                if node.description is not None:
                    html += f' alt="{node.description}"'
                html += f'> {node.text} </button>\n'
                indent_level += 1
            elif 'Image' in node.label or 'Button' in node.label:  # 未完善！！！！！！View & ViewGroup???
                indent = " " * indent_level * 2
                html += f'{indent}<img id="{node.number}"'
                if node.resourceid is not None:
                    split_text = node.resourceid.split(':')
                    word = split_text[1].strip()
                if node.resourceid is not None:
                    html += f' class="{word}"'
                    img_resourceid_flag = False
                if node.description is not None and node.description != '':
                    html += f' alt="{node.description}"'
                    img_description_flag = False
                if node.text is not None and node.text != '':
                    html += f' text="{node.text}"'
                    img_text_flag = False
                if img_resourceid_flag and img_description_flag and img_text_flag:
                    parent_node = find_parent_node_by_id(tree, node.id)
                    if parent_node:
                        if parent_node.resourceid is not None:
                            split_text = node.resourceid.split(':')
                            if len(split_text) > 1:
                                word = split_text[1].strip()
                            else:
                                word = split_text[0].strip()
                        if parent_node.resourceid is not None and parent_node != '':
                            html += f' class="{word}"'
                        if parent_node.description is not None and parent_node.description != '':
                            html += f' alt="{parent_node.description}"'
                        if parent_node.text is not None and parent_node.text != '':
                            html += f' text="{parent_node.text}"'
                html += ' />\n'
                indent_level += 1

    if has_children:
        for child in node.children:
            html += depth_traverse_output_html_source_version(tree, child, indent_level)

    # 处理结束标签
    if has_children:
        if node.label == 'hierarchy':
            html += f'</body>\n{indent}</html>'
        elif f'{node.label}_{node.number}' in old_div_flag and old_div_flag[f'{node.label}_{node.number}'] and div_symbol:
            html += f'{indent}</div>\n'

    return html


def source_version_final_result(xml_file_path):
    # 解析XML树结构
    tree_result = parse_xml_tree_old(xml_file_path)
    # 对XML树进行广度优先遍历并生成标号
    breadth_first_traversal_source_version(tree_result)
    source_version_html_result = xml_to_html_source_version(tree_result)
    change_xml_old(xml_file_path)
    with open('source_version_xml_encoding.html', 'w+', encoding='utf-8') as file:
        file.write(source_version_html_result)


def target_version_final_result(xml_file_path):
    # 解析XML树结构
    tree_result = parse_xml_tree_new(xml_file_path)
    # 对XML树进行广度优先遍历并生成标号
    breadth_first_traversal_target_version(tree_result)
    target_version_html_result = xml_to_html_target_version(tree_result)
    change_xml_new(xml_file_path)
    with open('target_version_xml_encoding.html', 'w+', encoding='utf-8') as file:
        file.write(target_version_html_result)


