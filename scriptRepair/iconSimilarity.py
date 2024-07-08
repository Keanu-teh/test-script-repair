from PIL import Image
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity


'''
                        通过神经网络获取图标图片特征向量并进行相似度对比获得title属性的值并填写到编码后的html中
'''


# 代码完成时需要从其他.py文件中获得变量来替代以下变量
number = 1
save_path = f'C:/Users/17720/Desktop/Workplace/PyCharmFolders/xmlSimilarity/source_image{number}.png'

# mobileNetV2加载预训练的轻量级CNN模型
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')


def get_title_value(bounds, file_path):
    global number
    screenshot = Image.open(file_path)
    bounds = bounds.strip('[]')
    left_top, right_bottom = bounds.split('][')
    left, top = map(int, left_top.split(','))
    right, bottom = map(int, right_bottom.split(','))
    # 截取图像片段
    image_fragment = screenshot.crop((left, top, right, bottom))
    # 保存图像片段
    image_fragment.save(save_path)
    number += 1
    # 加载图标图片
    image1 = cv2.imread('source_version_widget_image.png')
    image2 = cv2.imread(save_path)

    # 调整图标图片的尺寸
    image1 = cv2.resize(image1, (224, 224))
    image2 = cv2.resize(image2, (224, 224))

    # 预处理图标图片
    image1 = preprocess_input(image1)
    image2 = preprocess_input(image2)

    # 提取图标图片的特征向量
    vector1 = model.predict(np.expand_dims(image1, axis=0))
    vector2 = model.predict(np.expand_dims(image2, axis=0))

    # 将特征向量展平
    vector1 = np.ravel(vector1)
    vector2 = np.ravel(vector2)

    # 计算图标图片的相似度（例如余弦相似度）
    similarity = cosine_similarity([vector1], [vector2])
    similarity = round(similarity.item(), 2)

    return similarity



