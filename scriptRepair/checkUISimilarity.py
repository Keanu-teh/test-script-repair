import xml.etree.ElementTree as ET


'''
                                    oracle：通过寻找新旧两个版本的UI中的叶子节点对，计算叶子节点对的占比来判断是否是两个一样的页面
                                    具体来说，每个app有不同的临界值，临界值的计算则是通过在脚本运行的过程中计算遍历过的UI的叶子节点对占比的平均值获得的
'''

xml_file_path1 = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/xmls/deepl/deepl4_old/deepl4_xml_1.xml'
xml_file_path2 = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/xmls/deepl/deepl4_new/deepl4_xml_1.xml'


class TreeNode:
    def __init__(self, name, resourceid=None, description=None, text=None):
        self.name = name
        self.resourceid = resourceid
        self.description = description
        self.text = text
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def get_leaf_nodes(self):
        nodes = []
        if self.is_leaf():
            nodes.append(self)
        else:
            for child in self.children:
                nodes.extend(child.get_leaf_nodes())
        return nodes


def parse_xml_to_tree(xml_file):
    tree = ET.parse(xml_file)
    root_element = tree.getroot()
    return build_tree(root_element)


def build_tree(xml_element):
    node = TreeNode(xml_element.tag, xml_element.attrib.get('resource-id'), xml_element.attrib.get('content-desc'), xml_element.attrib.get('text'))
    for child_element in xml_element:
        child_node = build_tree(child_element)
        node.add_child(child_node)
    return node


# 将 XML 文件解析为自定义的树结构
root_node1 = parse_xml_to_tree(xml_file_path1)
root_node2 = parse_xml_to_tree(xml_file_path2)

# 获取所有叶子节点
leaf_nodes1 = root_node1.get_leaf_nodes()
leaf_nodes2 = root_node2.get_leaf_nodes()


def get_node_pair(nodes1, nodes2):
    count = 0
    node_attribute = []
    test_nodes1 = nodes1[:]
    test_nodes2 = nodes2[:]
    for node1 in test_nodes1:
        flag = False
        if node1.resourceid is not None and node1.resourceid != '':
            node_attribute.append(node1.resourceid)
        if node1.description is not None and node1.description != '':
            node_attribute.append(node1.description)
        if node1.text is not None and node1.text != '':
            node_attribute.append(node1.text)
        if len(node_attribute) != 0:
            for node2 in test_nodes2:
                for attrib in node_attribute:
                    if node2.resourceid is not None and attrib.lower() == node2.resourceid.lower():
                        count += 1
                        test_nodes1.remove(node1)
                        test_nodes2.remove(node2)
                        node_attribute.clear()
                        flag = True
                        break
                    elif node2.description is not None and attrib.lower() == node2.description.lower():
                        count += 1
                        test_nodes1.remove(node1)
                        test_nodes2.remove(node2)
                        node_attribute.clear()
                        flag = True
                        break
                    elif node2.text is not None and attrib.lower() == node2.text.lower():
                        count += 1
                        test_nodes1.remove(node1)
                        test_nodes2.remove(node2)
                        node_attribute.clear()
                        flag = True
                        break

                if flag:
                    break

    leaf_nodes1_rate = "{:.1f}%".format(round(count/len(nodes1), 3) * 100)
    leaf_nodes2_rate = "{:.1f}%".format(round(count/len(nodes2), 3) * 100)
    if leaf_nodes1_rate > leaf_nodes2_rate:
        print(leaf_nodes2_rate)
    else:
        print(leaf_nodes1_rate)


get_node_pair(leaf_nodes1, leaf_nodes2)

