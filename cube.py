import cv2
import numpy as np

# 读取图像
orig = cv2.imread('10mw-20ms-mid-c.tif')

# 生成全局增强图
dst = cv2.applyColorMap(orig, cv2.COLORMAP_AUTUMN)
# 归一化灰度化
img = np.mean(orig,axis=2)
img = (img/np.max(img) *255).astype('uint8')
# 去噪
blur = cv2.GaussianBlur(img, (5,5), 0, 0, cv2.BORDER_DEFAULT)
# 二值化
im5 = np.where(blur[...] < 80, 0, 255)
im5 = im5.astype('uint8')
# 腐蚀
kernel = np.ones((5,5),np.uint8)
im5 = cv2.erode(im5,kernel,iterations = 1)
# cv2.imshow('result',im5.astype('uint8'))
# cv2.waitKey(0)
# 去除外围影响
w,h = im5.shape
for i in range(w):
    if(np.sum(im5[i,:])<(h/3)*255):
        im5[0:i,:] = np.zeros_like(im5[0:i,:]) *255
        break
for i in range(w-1,0,-1):
    if(np.sum(im5[i,:])<(h/3)*255):
        im5[i:w,:] = np.zeros_like(im5[i:w,:]) *255
        break
for i in range(h):
    if(np.sum(im5[:,i])<(w/3)*255):
        im5[:,0:i] = np.zeros_like(im5[:,0:i]) *255
        break
for i in range(h-1,0,-1):
    if(np.sum(im5[:,i])<(w/3)*255):
        im5[:,i:h] = np.zeros_like(im5[:,i:h]) *255
        break
# 腐蚀
kernel = np.ones((5,5),np.uint8)
im5 = cv2.erode(im5,kernel,iterations = 3)
# 膨胀
element = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
dilation_img = cv2.dilate(im5, element, iterations=5)
# 伪彩色增强
for i in range(w):
    for j in range(h):
        if(dilation_img[i,j]==255):
            orig[i,j,:] = dst[i,j,:]

# 轮廓提取
# contours, hierarchy = cv2.findContours(dilation_img.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("result", orig)
cv2.waitKey(0)