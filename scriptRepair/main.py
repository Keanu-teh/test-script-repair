import xmlPreprocessing
import findWidgetInfo
import GUIencoding


'''
                                                输入相关信息，并对xml文件进行预处理
'''
code_need_to_repair = '''# el = driver.find_element(MobileBy.XPATH, "//*[contains(@text, 'To')]")'''
source_version_xml_file_path = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/xmls/maxim/maxim1_old/maxim1_xml_2.xml'
source_version_image_file_path = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/screenshots/maxim/maxim1_old/maxim1_screenshot_2.png'
target_version_xml_file_path = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/xmls/maxim/maxim1_new/maxim1_xml_2.xml'
target_version_image_file_path = 'C:/Users/17720/Desktop/Workplace/PyCharmFolders/Data/screenshots/maxim/maxim1_new/maxim1_screenshot_2.png'


# 对source version xml文件进行相应的预处理操作
xmlPreprocessing.source_version_xml_preprocess(source_version_xml_file_path, 100)


# 对target version xml文件进行预处理
xmlPreprocessing.target_version_xml_preprocess(target_version_xml_file_path, 100)


# 调用GUIencoding.py对source version进行encoding
GUIencoding.image_file_path = source_version_xml_file_path
GUIencoding.source_version_final_result('source_version_xml.xml')
# 调用findWidgetInfo.py找到source_widget_encoding表示
findWidgetInfo.image_file_path = source_version_image_file_path
findWidgetInfo.get_widget_info(code_need_to_repair)

# 将target version的UI截图传入GUIencoding.py中
GUIencoding.image_file_path = target_version_image_file_path
# 对target version xml文件进行encoding
GUIencoding.target_version_final_result('target_version_xml.xml')



