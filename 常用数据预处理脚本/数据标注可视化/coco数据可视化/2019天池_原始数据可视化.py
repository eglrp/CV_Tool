#!/usr/bin/env python
# coding=UTF-8
'''
@Description:
@Author: HuangQinJian
@LastEditors: HuangQinJian
@Date: 2019-04-23 13:43:24
@LastEditTime: 2019-04-30 21:29:26
'''
##### clw note:注意，带label的图片保存在当前路径下的一个名为anno_image_coco的文件夹内，这里取了大概7张图片；


from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
#import pylab
import cv2
import os
from skimage.io import imsave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
#pylab.rcParams['figure.figsize'] = (8.0, 10.0)

#img_and_anno_root = '/mfs/home/fangyong/data/guangdong/round1/train/'
#img_and_anno_root ='K:/deep_learning/dataset/2019tianchi/train/'
img_and_anno_root = '/mfs/home/fangyong/data/guangdong/round2/train_clw/'
img_path = img_and_anno_root + 'defect_Images/'
annFile = img_and_anno_root + 'Annotations/train.json'
img_save_path = img_and_anno_root + 'visualized_image'
VISUALIZE_SINGLE = False
NEED_SAVE = False

if NEED_SAVE:
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)

def draw_rectangle(boxes, labels, image):

    for box, label in zip(boxes, labels):
        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[0]) + int(box[2]), int(box[1]) +int(box[3])), (0, 255, 0), 2)   # xywh，需要转成左上角坐标, 右下角坐标

        # clw note:主要用于输出中文的label
        cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)  # 图片上打印
        #font = ImageFont.truetype('/media/clwclw/data/fonts/simsun.ttf', 20, encoding="utf-8")
        font = ImageFont.truetype('./simsun.ttf', 36, encoding="utf-8")
        #font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 36, encoding="utf-8")

        left = float(box[0])
        top = float(box[1])
        right = float(box[0]) + float(box[2])
        down = float(box[1]) + float(box[3])

        draw.text(((left + right) / 2.0, (top + down) / 2.0), label, (255, 0, 0), font=font) # clw note：在中心位置输出标签

        image = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

    return image


# 初始化标注数据的 COCO api
coco = COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
# print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
# print('COCO supercategories: \n{}'.format(' '.join(nms)))

img_list = os.listdir(img_path)

# 查看某张图片
if VISUALIZE_SINGLE:
    for i in range(len(img_list)):
    # for i in range(5): # clw note：随机查看几张
        imgIds = i+1
        img = coco.loadImgs(imgIds)[0]
        image_name = img['file_name']
        if image_name != '7e7e6359d8fb8e9c1332319214.jpg':
            continue
        else:
            # catIds=[] 说明展示所有类别的box，也可以指定类别
            annIds = coco.getAnnIds(imgIds=img['id'], catIds=[], iscrowd=None)
            anns = coco.loadAnns(annIds)
            # print(anns)
            coordinates = []
            labels = []
            img_raw = cv2.imread(os.path.join(img_path, image_name))
            for j in range(len(anns)):
                # 1、求坐标
                coordinate = []
                coordinate.append(anns[j]['bbox'][0])
                coordinate.append(anns[j]['bbox'][1])
                coordinate.append(anns[j]['bbox'][2])
                coordinate.append(anns[j]['bbox'][3])
                coordinates.append(coordinate)

                # 2、找到对应的标签

                labels.append(cats[anns[j]['category_id']]['name'])

            image = draw_rectangle(coordinates, labels, img_raw)
            cv2.namedWindow(image_name, 0);
            cv2.resizeWindow(image_name, 1280, 1024);
            cv2.imshow(image_name, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if NEED_SAVE:
                imsave(img_save_path, image)

else:
    # 查看所有图片
    for imgId in range(0, len(img_list)):
    #for i in range(3000, len(img_list)):  # look up from xxxx
    # for i in range(5): # clw note：随机查看几张
        img = coco.loadImgs(imgId)[0]
        image_name = img['file_name']
        print('clw: already read %d images' % (imgId))
        # print(img)

        # 加载并显示图片
        # I = io.imread('%s/%s' % (img_path, img['file_name']))
        # plt.axis('off')
        # plt.imshow(I)
        # plt.show()

        # catIds=[] 说明展示所有类别的box，也可以指定类别
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=[], iscrowd=None)
        anns = coco.loadAnns(annIds)
        # print(anns)


        coordinates = []
        labels = []
        img_raw = cv2.imread(os.path.join(img_path, image_name))

        special_class_num = 0  # clw note: only see some special class
        for j, ann in enumerate(anns):
            if ann['category_id'] != 4:  # clw note: only see some special class
                continue
            special_class_num += 1
            # 1、求坐标
            coordinate = []
            # coordinate.append(anns[j]['bbox'][0])
            # coordinate.append(anns[j]['bbox'][1]+anns[j]['bbox'][3])
            # coordinate.append(anns[j]['bbox'][0]+anns[j]['bbox'][2])
            # coordinate.append(anns[j]['bbox'][1])
            coordinate.append(anns[j]['bbox'][0])
            coordinate.append(anns[j]['bbox'][1])
            coordinate.append(anns[j]['bbox'][2])
            coordinate.append(anns[j]['bbox'][3])
            # print(coordinate)
            coordinates.append(coordinate)

            # 2、找到对应的标签
            labels.append(cats[anns[j]['category_id'] - 1 ]['name']) # clw note: the reason to -1 is that the first is 1 but the index should be 0

        if special_class_num == 0:
            continue
        else:
            image = draw_rectangle(coordinates, labels, img_raw)
            cv2.namedWindow(image_name, 0);
            cv2.resizeWindow(image_name, 1600, 1200);
            cv2.moveWindow(image_name, 0, 0);
            cv2.imshow(image_name, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if NEED_SAVE:
                imsave(img_save_path, image)