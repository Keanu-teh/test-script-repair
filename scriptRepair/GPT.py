import openai
import getGPTResult
import re

openai.api_key = ''

# 只需要在第一次使用GPT进行判断时加上few-shot learning的信息，后面就不需要了
gpt_first = False
# 是否存在下一个测试动作
next_action_flag = False

# 将findWidgetInfo.py中的source_version_widget_html变量传入
with open('source_widget_xml_encoding.html', 'r', encoding='utf-8') as file:
    source_widget_encoding = file.read()

# 获得target version xml的html表示(字符串)
with open('target_version_xml_encoding.html', 'r', encoding='utf-8') as file:
    target_UI_encoding = file.read()

target_UI_encoding = target_UI_encoding.replace('\n', '').replace('\r', '').replace(' ', '')


# 下一个测试动作的自然语言描述
next_action_desc = 'The action clicks on a widget whose text attribute is "inbox"'


# 定义prompt及相关参数
few_shot_learning = '''
I am a UI test script fixer, and I need you to do the same job I did, to make it easier for you to understand I will encode the xml information into html information according to my rules. When I start to repair the UI test script, I'll firstly try to compare the resource-id, content-desc, and text values(if present in the xml file) of all the widgets on the page to the values of the source widget, that is correspondingly, the value of the class and alt attributes in the HTML element and the text information sandwiched in the html elements to find out if they are the same or semantically similar to the ones of source widget. Of course, it is not necessary that the three attributes correspond to each other to compare, if the text value and the content-desc value (which can be any combination of the three attributes) are the same or semantically similar, I also think it is possible that the two widgets correspond to each other.Then I will try to compare the relative position and image similarity of the widget icons to discover if they are identical or similar in location and vision. Specifically speaking, in the HTML representation of the xml there are divs and their id values related to positional relationships and title attributes(if present) related to image similarity. If the test action that went wrong in the test script is followed by a test action I also include the widget that the next test action is going to manipulate next in the judgment and the first widget is what causes the test script to fail. There are five scenarios in script repair work and there will be different treatment methods for different repair scenarios. Here's my process for fixing the five scenarios.
Here is the first scenario. The following is the source widget encoding: <div id="3"><img id="3_3" class="id/nav_controls_compass_container" alt="Compass" /></div>. The following is the target UI encoding: <html><body><div id="1"><img id="1_1" alt="Open navigation drawer" title="0.34" /><button id="1_2" class="id/toolbar_search"> Search </button><button id="1_3" class="id/toolbar_feed"> Voyager </button><button id="1_4" class="id/toolbar_feeling_lucky"> I'm Feeling Lucky </button><button id="1_5" class="id/toolbar_measure"> Measure </button><img id="1_6" alt="More options" title="0.41"/></div><div id="2"><img id="2_1" class="id/google_status_logo" title="0.26"/></div><div id = 3><img id=3_1 class="id/nav_controls_my_location" alt="Location permissions disabled" title="0.52" /><img id=3_2 class="id/nav_controls_pegman" alt="Street View" title="0.47" /><img id=3_3 class="id/nav_controls_compass" alt="Compass"title="0.90" /></div></body></html>. According to the fixing process I mentioned at the beginning, I found that the class value of the widget with id "3_3" on the target UI screen is semantically similar to that of the source widget, and both alt values are "Compass", and the title value of "3_3" is 0.90, so I think id "3_3" is the target widget, and output [id = "3_3"].
Here is the second scenario. The following is the source widget encoding: <div id=3><img id=3_4 class="id/mq" /></div>. The following is the target UI encoding: <html><body><div id="1"><button id="1_1"> "YouTube & Library" </button></div><div id = "2"><button id="2_1"> All Videos </button><button id="2_2"> Folders </button></div><div id="3"><button id="3_1" class="id/xb"> 0 video </button><img id="3_2" class="id/na" title="0.98" /><img id="3_3" class="id/a1q" title="0.56" /><img id="3_4" class="id/n6" title="0.37" /></div><div id="4"><img id="4_1" class = "id/me" title  = "0.07" /></div><div id="5"><img id="5_1" alt="Music" title="0.41" /><img id="5_2" alt="Video" title="0.45" /><img id="5_3" alt="Trending" title="0.32" /><img id="5_4" alt="Me" title="0.35" /></div></body></html>. Following the repair process I described at the beginning, I found that none of the three attribute values of all the widgets on the target UI screen were the same or semantically similar to the source widget's attribute values, but since the title value of id "3_2" is 0.98 which means "3_2" is most visually similar to source widget because its title value is the largest, so I think id "3_2" is the target widget, but since I am judging based on the position and similarity information rather than class, alt and text values so I have to output [possibly id = "3_2"].
Here is the third scenario. The following is the source widget encoding: <div id="2"><button id="2_5"> Folders </button></div>. The following is the target UI encoding: <html><body><div id="1"><button id="1_1"> "YouTube & Library" </button></div><div id="2" style="display:flex"><button id="2_1"> Songs </button><button id="2_2"> Playlists </button><button id="2_3"> Albums </button><button id="2_4"> Artists </button></div><div id="3"><button id="3_1" class="id/xb"> Play all </button><img id="3_2" class="id/us" /><img id="3_3" class="id/o9k" /></div><div id="4"><button id="4_1" class="id/me"> DISCOVER MORE </button></div></body></html>. According to the fixing process I mentioned at the beginning, I found that the attribute values of the source widget are not identical or semantically similar to the ones of all the widgets in the target UI and the id value of the div to which the source widget belongs is the same as the id value of a div in the target UI screen, and the id value of the source widget can be the next id in the div with id "2" in the target UI, and the display mode of the div with id "2" is flex, so I think the direction to swipe the screen should be to the left. Moreover I think what causes the script to fail is the UI display size change, so output [swipe left on <div id="2">].
Here is the fourth scenario. The following is the source widget encoding: <div id="2_1"><button id="2_1_1"> genders </button></div>. The following is the target UI encoding: <html><body><div id="1"><div id="1_1"><button id="1_1_1"> Data backup </button><img id="1_1_2" /><img id="1_1_3" /></div><img id="1_2" class="id/fresh" /></div><div id="2"><button id="2_1"> practice settings </button><button id="2_2"> general settings </button><button id="2_3"> voice selection(TTS) </button><button id="2_4"> language choice </button></div><div id="3"><button id="3_1"> practice </button><button id="3_2"> discovery </button><button id="3_3"> report </button><button id="3_4"> setting </button></div></body></html>. According to the fixing process I mentioned at the beginning, I found that none of the widgets on the target UI have the same class and alt values as the source widget or have similar semantics, but the widget with id "2_1" has text value "practice settings", which is semantically similar to the text value "genders" of the source widget, because "practice settings" can include "genders", so output [click id = "2_1"].
Here is the fifth scenario. The following is the source widget encoding: <div id="3"><button id="3_1"> tools </button></div>.The following is the natural language description of the next action: 'The action clicks on a widget whose text attribute is "translate"'. The following is the target UI encoding: <html><body><div id="1"><div id="1_1"><button id="1_1_1"> user </button><img id="1_1_2" class="id/more" /></div><button id="1_2"> following </button></div><div id="2"><button id="2_1"> Profile </button><button id="2_2"> Premium </button><button id="2_3"> Bookmarks </button><button id="2_4"> Lists </button><button id="2_5"> translate </button></div><div id="3"><button id="3_1"> tools </button><button id="3_2"> setup & support </button></div></body></html>. According to the fixing process I mentioned at the beginning, I found that there are two source widgets, that means the test script has two test actions which are clicked in sequence and the test script execution failed on the first source widget. The text value of the first source widget is the same as the text value of id "3_1" in the target UI, and the text value of the second source widget is the same as the text value of id "2_5" in the target UI. However, there already exists a widget with id "2_5" in the target UI with the same value as the widget to be clicked by the second test action, so I think I should merge the two test actions of the test script into a single one, so I output [only id = "2_5"].
Here is the sixth scenario. The following is the source widget encoding: <div id="4"><button id="4_1"> Sound </button></div>. The following is the natural language description of the next action: The action clicks on a widget whose text attribute is "up". The following is the target UI encoding: <html><body><div id="1"><div id="1_1"><button id="1_1_1"> light </button><img id="1_1_2" class="id/light" /></div><button id="1_2"> dark </button></div><div id="2"><button id="2_1"> location </button><button id="2_2"> map </button><button id="2_3"> privacy </button></div></body></html>. According to the fixing process I mentioned at the beginning, I found that none of the source widgets had the same or similar property information as the target widget, so I assumed that the source widget that did the job might have been removed. Therefore the output [function deleted].
'''


if gpt_first:
    if next_action_flag:
        prompt = f'''
        {few_shot_learning}
        And now it is your turn to judge which widget on the target UI screen is most likely to correspond to the source widget? The following is the source widget encoding: {source_widget_encoding}. The following is the natural language description of the next action: {next_action_desc}. The following is the target UI encoding: {target_UI_encoding}. I want you to judge in strict order of the above five scenarios and if you think the scenario you are judging is the same or similar to one of the scenarios I showed you above, please output one answer strictly in the output format corresponding to each of the scenarios, that is: [id = "value"], [possibly id = "value"], [swipe left/right/up/down on <div id="value">], [click id = "value"], [only id = "value"] or [function deleted].
        '''
    else:
        prompt = f'''
        {few_shot_learning}
        And now it is your turn to judge which widget on the target UI screen is most likely to correspond to the source widget? The following is the source widget encoding: {source_widget_encoding}. The following is the target UI encoding: {target_UI_encoding}. I want you to judge in strict order of the above five scenarios and if you think the scenario you are judging is the same or similar to one of the scenarios I showed you above, please output one answer strictly in the output format corresponding to each of the scenarios, that is: [id = "value"], [possibly id = "value"], [swipe left/right/up/down on <div id="value">], [click id = "value"], [only id = "value"] or [function deleted].
        '''
else:
    if next_action_flag:
        prompt = f'''
        And now it is your turn to judge which widget on the target UI screen is most likely to correspond to the source widget? The following is the source widget encoding: {source_widget_encoding}. The following is the natural language description of the next action: {next_action_desc}. The following is the target UI encoding: {target_UI_encoding}. I want you to judge in strict order of the above five scenarios and if you think the scenario you are judging is the same or similar to one of the scenarios I showed you above, please output one answer strictly in the output format corresponding to each of the scenarios, that is: [id = "value"], [possibly id = "value"], [swipe left/right/up/down on <div id="value">], [click id = "value"], [only id = "value"] or [function deleted].
        '''
    else:
        prompt = f'''
        And now it is your turn to judge which widget on the target UI screen is most likely to correspond to the source widget? The following is the source widget encoding: {source_widget_encoding}. The following is the target UI encoding: {target_UI_encoding}. I want you to judge in strict order of the above five scenarios and if you think the scenario you are judging is the same or similar to one of the scenarios I showed you above, please output one answer strictly in the output format corresponding to each of the scenarios, that is: [id = "value"], [possibly id = "value"], [swipe left/right/up/down on <div id="value">], [click id = "value"], [only id = "value"] or [function deleted].
        '''

response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    max_tokens=100,
    temperature=0
)


result_text = response['choices'][0]['text']
result_pattern = r'\[(.*?)\]'
result_match = re.search(result_pattern, result_text)
if result_match:
    result_text = result_match.group()
    final_result = getGPTResult.get_result(result_text)
else:
    final_result = "OUTPUT WRONG"


'''
                                                输出修复结果
'''
# 正常使用
print("修复结果为：" + final_result)

