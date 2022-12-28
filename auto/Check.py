import cv2
import numpy as np


# 直方图比较图片相似度
# 主要用于判断当前所在的界面
def diffImage(img_1, img_2):
    # 转为灰度图
    gray_1 = cv2.cvtColor(np.asarray(img_1), cv2.COLOR_RGB2GRAY)
    gray_2 = cv2.cvtColor(np.asarray(img_2), cv2.COLOR_RGB2GRAY)
    # 获取直方图结果
    hist_1 = cv2.calcHist([gray_1], [0], None, [64], [0, 256])
    hist_2 = cv2.calcHist([gray_2], [0], None, [64], [0, 256])
    # 直方图归一化
    hist_1 = np.float32(hist_1/gray_1.size)
    hist_2 = np.float32(hist_2/gray_2.size)
    # 相关系数
    corr = cv2.compareHist(hist_1, hist_2, cv2.HISTCMP_CORREL)
    return corr


# 统一两张图片的分辨率
def _toSameSize(img_1, img_2, mode='small'):
    if mode not in ('big', 'small'):
        raise Exception("size mode err!")

    img_1_size = img_1.size
    img_2_size = img_2.size
    small_size = 1 if img_1_size[0]*img_1_size[1] < img_2_size[0]*img_2_size[0] else 2
    if mode == 'small':
        if small_size == 1:
            return img_1, img_2.resize(img_1_size)
        else:
            return img_1.resize(img_2_size), img_2
    else:
        if small_size == 1:
            return img_1.resize(img_2_size), img_2
        else:
            return img_1, img_2.resize(img_1_size)


# 一次只返回一个点，为tar_image所在的坐标中心 找不到就返回None
def checkInImage(tar_image, image, threshold=0.6) -> tuple:
    img_gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    template = cv2.cvtColor(np.asarray(tar_image), cv2.COLOR_RGB2GRAY)
    w, h = tar_image.size
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 规定和tar_image相似有threshold以上时则判断其是同一图片
    if max_val >= threshold:
        # 这部分可以看到匹配的结果，但是会阻塞程序
        # cv2.rectangle(img_gray, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 2)
        # cv2.namedWindow('img_rgb', 0)
        # cv2.imshow('img_rgb', np.asarray(img_gray))
        # cv2.waitKey(0)
        return max_loc[0]+w//2, max_loc[1]+h//2
    return None

