from pycocotools.coco import COCO
import cv2
import os
import shutil
import json
import numpy as np

img_and_anno_root = 'C:/Users/62349/Downloads/chongqing1_round1_train1_20191223_split/'
img_path = img_and_anno_root + 'images/'
annFile = img_and_anno_root + 'annotations.json'
annFile1 = img_and_anno_root + 'annotations1.json'

# 原有json有问题，先做修改
with open(annFile) as f:
    dataset = json.load(f)
for id, ann in enumerate(dataset['annotations']):
    ann['id'] = id
with open(annFile1, 'w') as f:
    json.dump(dataset, f)


annFile2 = img_and_anno_root + 'annotations2.json'
shutil.copyfile(annFile1, annFile2)  # 如果旧的存在，会覆盖
img_path2 = os.path.join(img_and_anno_root, 'images2')
if not os.path.exists(img_path2):
    os.makedirs(img_path2)

# 初始化标注数据的 COCO api
dataset0 = COCO(annFile1)
dataset1 = COCO(annFile1)
dataset2 = COCO(annFile2)

# display COCO categories and supercategories
cats = dataset1.loadCats(dataset1.getCatIds())
cats = sorted(cats, key = lambda e:e.get('id'),reverse = False) # clw note：这里并不完全是COCO格式，只能算是类COCO格式，因此
                                                                #           比如这里的categories就不是排序的，因此需要手动排序
img_list = os.listdir(img_path)

# 查看所有图片
count_box1 = 0
count_box2 = 0
count_img1 = 0
count_img2 = 0
for imgId in range(1, len(img_list)+1):
    img = dataset0.loadImgs(imgId)[0]
    image_name = img['file_name']
    print('clw: already read %d images' % (imgId))
    # print(img)

    # clw note:读取image_id对应标注信息的两种方法：
    anns = dataset0.imgToAnns[imgId]
    # print(anns)

    #img = cv2.imread(os.path.join(img_path, image_name))


    for j, ann in enumerate(anns):
        # 1、处理json，
        # # （1）如果cats[anns[j]['category_id']] in [6,7,8]，即瓶盖类，则移除dataset1中的内容，
        # if cats[anns[j]['category_id']]['id'] in [6,7,8]:  # clw note：TODO，但是还有11张酒瓶样本是只含有category_id=0也就是背景，
        if dataset0.imgs[anns[j]['image_id']]['width'] == 4096: # 因此改为如果宽度是4096，即瓶盖类，则移除dataset1中的内容，
            print('clw: count_box1 =', count_box1)
            count_box1 += 1
            # 删除 dataset1.anns
            for key in list(
                    dataset1.anns):  # 字典在遍历时不能进行修改，建议转成列表或集合处理。 https://blog.csdn.net/zhihaoma/article/details/51265168
                if dataset1.anns[key+count_img2]['image_id'] == imgId:
                    del dataset1.anns[key+count_img2]
                else:
                    break  # 因为是顺序，可以遍历，然后没有该imgId对应的anns就跳出

            # 删除 dataset1.imgs的信息
            for key in list(dataset1.imgs):
                a = list(dataset1.imgs)
                b = dataset1.imgs[key+count_img2]
                if dataset1.imgs[key+count_img2]['id'] == imgId:
                #if key + count_img2 == imgId:
                    del dataset1.imgs[int(key)+count_img2]
                else:
                    break  # 因为是顺序，可以遍历，然后没有该imgId对应的anns就跳出

            # 同时拷贝图片到img_path2
            if j == len(anns) - 1:  # 如果该图片所有anns处理完
                shutil.move(os.path.join(img_path, image_name), os.path.join(img_path2, image_name))
                count_img1 += 1
        #
        # # （2）否则，移除dataset2中的内容
        else:
            print('clw: count_box2 =', count_box2)
            count_box2 += 1
            # 删除 dataset2.anns
            for key in list(dataset2.anns):  # 字典在遍历时不能进行修改，建议转成列表或集合处理。 https://blog.csdn.net/zhihaoma/article/details/51265168
                if dataset2.anns[key+count_img1]['image_id'] == imgId:
                    del dataset2.anns[key+count_img1]
                else:
                    break  # 因为是顺序，可以遍历，然后没有该imgId对应的anns就跳出

            # 删除 dataset2.imgs的信息
            for key in list(dataset2.imgs):
                if dataset2.imgs[key+count_img1]['id'] == imgId:
                    del dataset2.imgs[key+count_img1]
                else:
                    break  # 因为是顺序，可以遍历，然后没有该imgId对应的anns就跳出

            if j == len(anns) - 1:  # 如果该图片所有anns处理完
                count_img2 += 1


    # 3、调整 dataset1.anns dataset1.imgs的索引序号，和之前一致，dataset2同理；注意二者的category不用管，都按照10个类来，
    #    便于输出索引的统一，不用再后处理；


print('end!!')



