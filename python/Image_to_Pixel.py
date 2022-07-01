import numpy as np
from PIL import Image
import itertools
from scipy import ndimage
import scipy.spatial as sp
import cv2
import os

import pandas as pd

from tqdm import tqdm
from math import sqrt
from time import time
from joblib import delayed, Parallel

r = list(range(0,256,17))	
g = list(range(0,256,17))
b = list(range(0,256,17))

rgb_ref = list(itertools.product(r,g,b))

def nearest_colour(rgb_list):
	r, g, b = rgb_list
	distances = []
	for color in rgb_ref:
		r_ref, g_ref, b_ref = color
		dist = sqrt((r - r_ref)**2 + (g - g_ref)**2 + (b - b_ref)**2)
		distances.append((dist, color))
	return min(distances)[1]

def block_mean(ar, fact):
    assert isinstance(fact, int), type(fact)
    sx, sy = ar.shape
    X, Y = np.ogrid[0:sx, 0:sy]
    regions = sy/fact * (X/fact) + Y/fact
    res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
    res.shape = (sx/fact, sy/fact)
    return res


direct = os.listdir("./Image/fnemo")

print(len(direct))

fnemo_images = pd.DataFrame()

for img in tqdm(direct):

	img_a = Image.open("./Image/fnemo/"+str(img))
	img_a = np.asarray(img_a)
	img_a = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(img_a)))
	
	h,w,bpp = np.shape(img_a)
	
	for py in range(0,h):
	    for px in range(0,w):
	      ########################
	      #Used this part to find nearest color 
	      #reference : https://stackoverflow.com/a/22478139/9799700
	      input_color = (img_a[py][px][0],img_a[py][px][1],img_a[py][px][2])
	      tree = sp.cKDTree(rgb_ref) 
	      ditsance, result = tree.query(input_color) 
	      nearest_color = rgb_ref[result]
	      ###################
	      
	      img_a[py][px][0]=nearest_color[0]
	      img_a[py][px][1]=nearest_color[1]
	      img_a[py][px][2]=nearest_color[2]
	
	img_a = img_a.reshape(14400,3)

	img_p = pd.DataFrame(img_a, columns = ['R','G','B'])

	img_p["RGB"] = "("+img_p["R"].astype(str)+", "+img_p["G"].astype(str)+", "+img_p["B"].astype(str)+")"

	img_p = img_p.drop(["R","G","B"], axis=1)	

	img_p["Name"] = str(img)

	fnemo_images = fnemo_images.append(img_p)	
	
fnemo_images.to_csv("fnemo.csv", sep=';', encoding='utf-8', index =False)

