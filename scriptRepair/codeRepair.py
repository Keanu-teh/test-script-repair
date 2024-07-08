import searchWidget


'''
                                    对于来自getGPTResult的调用进行处理
'''


def choose_repair_function(result_str):
    result_str = result_str.strip('[]')
    words = result_str.split()
    if words[0] == 'possibly':
        return code_repair_possibly(result_str)
    elif words[0] == 'id':
        return code_repair_id(result_str)
    elif words[0] == 'only':
        return code_repair_only(result_str)


def code_repair_possibly(result_str):
    result_str = result_str.replace('possibly', '').strip()
    # 将result传入searchWidget.py中获取唯一的定位方式
    node = searchWidget.get_root()
    return_result = searchWidget.find_way_to_locate_widget(node, result_str)
    possibly_mode = return_result.split('=')[0]
    possibly_info = return_result.split('=')[1]
    if possibly_mode == 'content-desc':
        possibly_result = f'''el = driver.find_element(MobileBy.ACCESSIBILITY_ID, {possibly_info})  # possibly, GPT result = [possibly id = "{possibly_info}"]'''
    elif possibly_mode == 'resource-id':
        possibly_result = f'''el = driver.find_element(MobileBy.ID, {possibly_info})  # possibly, GPT result = [possibly id = "{possibly_info}"]'''
    elif possibly_mode == 'text':
        possibly_result = f'''el = driver.find_element(MobileBy.XPATH, "//*[contains(@text, {possibly_info})]")  # possibly, GPT result = [possibly id = "{possibly_info}"]'''
    elif possibly_mode == 'class':
        possibly_id_info_class_name = possibly_info.split(',')[0].replace('"', '')
        possibly_id_info_index = possibly_info.split(',')[1].replace('"', '')
        possibly_result = f'''el = driver.find_elements(MobileBy.CLASS_NAME, "{possibly_id_info_class_name}")[{possibly_id_info_index}]  # possibly, GPT result = [possibly {result_str}]'''

    return possibly_result


def code_repair_id(result_str):
    # 将result_str传入searchWidget.py中获取唯一的定位方式
    node = searchWidget.get_root()
    return_result = searchWidget.find_way_to_locate_widget(node, result_str)
    id_mode = return_result.split('=')[0]
    id_info = return_result.split('=')[1]
    if id_mode == 'content-desc':
        id_result = f'''el = driver.find_element(MobileBy.ACCESSIBILITY_ID, {id_info})  # GPT result = [id = "{id_info}"]'''
    elif id_mode == 'resource-id':
        id_result = f'''el = driver.find_element(MobileBy.ID, {id_info})  # GPT result = [id = "{id_info}"]\nel.click()'''
    elif id_mode == 'text':
        id_result = f'''el = driver.find_element(MobileBy.XPATH, "//*[contains(@text, {id_info})]")  # GPT result = [id = "{id_info}"]'''
    elif id_mode == 'class':
        id_info_class_name = id_info.split(',')[0].replace('"', '')
        id_info_index = id_info.split(',')[1].replace('"', '')
        id_result = f'''el = driver.find_elements(MobileBy.CLASS_NAME, "{id_info_class_name}")[{id_info_index}]  # GPT result = [id = "{id_info}"]'''

    return id_result


def code_repair_only(result_str):
    result_str = result_str.replace('only', '').strip()
    # 将result_str传入searchWidget.py中获取唯一的定位方式
    node = searchWidget.get_root()
    return_result = searchWidget.find_way_to_locate_widget(node, result_str)
    only_mode = return_result.split('=')[0]
    only_info = return_result.split('=')[1]
    if only_mode == 'content-desc':
        only_result = f'''el = driver.find_element(MobileBy.ACCESSIBILITY_ID, "{only_info}")  # only need one test action, GPT result = [id = "{only_info}"]'''
    elif only_mode == 'resource-id':
        only_result = f'''el = driver.find_element(MobileBy.ID, {only_info})  # only need one test action, GPT result = [id = "{only_info}"]'''
    elif only_mode == 'text':
        only_result = f'''el = driver.find_element(MobileBy.XPATH, "//*[contains(@text, {only_info})]")  # only need one test action, GPT result = [id = "{only_info}"]'''
    elif only_mode == 'class':
        only_info_class_name = only_info.split(',')[0].replace('"', '')
        only_info_index = only_info.split(',')[1].replace('"', '')
        only_result = f'''el = driver.find_elements(MobileBy.CLASS_NAME, "{only_info_class_name}")[{only_info_index}]  # only need one test action, GPT result = [id = "{only_info}"]'''

    return only_result


