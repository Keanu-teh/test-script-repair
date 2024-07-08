import searchWidget
import re
import getBounds

'''
                                    对于来自getGPTResult的调用进行处理
'''


def choose_add_function(result_str):
    result_str = result_str.strip('[]')
    words = result_str.split()
    if words[0] == 'swipe':
        return code_add_swipe(result_str)
    elif words[0] == 'click':
        return code_add_click(result_str)


def code_add_swipe(result_str):
    pattern = r'(\w+)\s+on\s+(.*)'
    widget_pattern = r'id="(.*?)"'
    matches = re.search(pattern, result_str)
    if matches:
        swipe_direction = matches.group(1)
        swipe_location = matches.group(2)   # div
    else:
        print('WRONG!!!')
    div_match = re.search(r'id="([^"]+)"', swipe_location)
    swipe_location = div_match.group(0)
    widget_id = re.search(widget_pattern, swipe_location).group(1)
    # 将swipe_location传入对应的py中获得要进行滑动的区域的bounds属性
    bounds = getBounds.find_node_bounds('source_version_xml.xml', swipe_location)
    # 根据两个变量值决定要加入的代码行
    bounds = bounds.strip('[]')
    left_top, right_bottom = bounds.split('][')
    left_top_x, left_top_y = map(int, left_top.split(','))
    right_bottom_x, right_bottom_y = map(int, right_bottom.split(','))
    x_average = int((left_top_x + right_bottom_x)/2)
    y_average = int((left_top_y + right_bottom_y)/2)
    if swipe_direction == 'left':   # 向左滑？
        swipe_result = f'driver.swipe({right_bottom_x}, {y_average}, {left_top_x}, {y_average}, 3000)  # GPT result = [swipe left on <div id="{widget_id}">]'
    elif swipe_direction == 'right':   # 向右滑？
        swipe_result = f'driver.swipe({left_top_x}, {y_average}, {right_bottom_x}, {y_average}, 3000)  # GPT result = [swipe right on <div id="{widget_id}">]'
    elif swipe_direction == 'up':   # 向上滑？
        swipe_result = f'driver.swipe({x_average}, {right_bottom_y}, {x_average}, {left_top_y}, 3000)  # GPT result = [swipe up on <div id="{widget_id}">]'
    elif swipe_direction == 'down':   # 向下滑？
        swipe_result = f'driver.swipe({x_average}, {left_top_y}, {x_average}, {right_bottom_y}, 3000)  # GPT result = [swipe down on <div id="{widget_id}">]'

    return swipe_result


def code_add_click(result_str):
    match = re.search(r'id = "(.*?)"', result_str)
    widget_value = match.group(0).replace(' ', '')
    pattern = r'id="(.*?)"'
    widget_id = re.search(pattern, widget_value).group(1)
    # 根据widget_value的值在xml文件中寻找唯一确定的点击方式(此功能由searchWidget.py完成)
    node = searchWidget.get_root()
    return_result = searchWidget.find_way_to_locate_widget(node, widget_value)
    click_mode = return_result.split('=')[0]
    click_info = return_result.split('=')[1]
    if click_mode == 'content-desc':
        click_result = f'''el = driver.find_element(MobileBy.ACCESSIBILITY, {click_info})  # GPT result = [click id = "{widget_id}"]'''
    elif click_mode == 'resource-id':
        click_result = f'''el = driver.find_element(MobileBy.ID, {click_info})  # GPT result = [click id = "{widget_id}"]'''
    elif click_mode == 'text':
        click_result = f'''el = driver.find_element(MobileBy.XPATH, "//*[contains(@text, {click_info})]")  # GPT result = [click id = "{widget_id}"]'''
    elif click_mode == 'class':
        click_info_class_name = click_info.split(',')[0].replace('"', '')
        click_info_index = click_info.split(',')[1].replace('"', '')
        click_result = f'''el = driver.find_elements(MobileBy.CLASS_NAME, "{click_info_class_name}")[{click_info_index}]  # GPT result = [click id = "{widget_id}"]'''

    return click_result




