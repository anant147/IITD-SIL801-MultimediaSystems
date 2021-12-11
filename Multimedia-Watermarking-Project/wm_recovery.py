from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import time
import numpy as np
import functools
import sys
import os
import re
import cv2
import time
import pywt

###########################################################################################################################################
######################## method 1 ################################333
#################################################################################################


###########################################################################################################################################
######################## method 2 ################################333
#################################################################################################

def get_Content_str( content):
    
    contStr = ""
    
    for c in content:
        contStr = contStr + str(c)
        
    return contStr

def get_frag_inv_watermark_msg( watermarked_image_path):
    
    endcheck = '#$$#'
    length = len(endcheck)
    lastchar = endcheck[length-1]
    
    zlen = 16
    
    watermark_image = Image.open( watermarked_image_path)
    wmarkArr = np.array( watermark_image)
    
    rows = wmarkArr.shape[0]
    cols = wmarkArr.shape[1]
    channels = wmarkArr.shape[2]
    
    message = ""
    
    content = []
    
    ctr = 0
    
    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                ctr = ctr + 1
                val = wmarkArr[i][j][k]%2
                content.append(val)
                
                if ctr % zlen == 0:

                    # getting each character of the message
                    contStr = get_Content_str( content)
                    val1 = int(contStr, 2)
                    cur_char = chr( val1)
                    message = message + cur_char
#                     print(message)
                    
                    if cur_char == '#' and message[(-4):] == '#$$#':
                        return message[:(-4)]
                    content = []

    # if the terminatinng conditions are not met
    # it can be assumed that there is no watermark message
    # or image is altered                
    return 'cannot get any watermark message'



def getArgumentForFragileInvisibleWatermarkRecov():

	print(' for fragile invisible watermark Recovery , enter the arguments :- ')

	watermarked_image_path = input('Enter the path of watermarked image :- ')
	watermark_message = get_frag_inv_watermark_msg( watermarked_image_path)
	print('the watermark message :- ', watermark_message)

###########################################################################################################################################
######################## method 3 ################################333
#################################################################################################

def get_image_after_idct2(img, val1, val2, val3):

    # doing 3-d inverse haar wavelet transform of image with given parameters.
    pr3 = (img, val3)
    img = pywt.idwt2(pr3, 'haar', mode = 'reflect')
    
    pr2 = (img, val2)
    img = pywt.idwt2(pr2, 'haar', mode = 'reflect')
    
    pr1 = (img, val1)
    img = pywt.idwt2(pr1, 'haar', mode = 'reflect')
    
    return img


def get_discrete_Wavelet_Value( mainImage, wmarkImage):

    # doing 3-d wavelet haar transform of given image
    mainval1 = pywt.dwt2(mainImage, 'haar', mode='reflect')
    mainval2 = pywt.dwt2(mainval1[0], 'haar', mode='reflect')
    mainval3 = pywt.dwt2(mainval2[0], 'haar', mode='reflect')

    # doing 3-d wavelet haar tranform of watermarked image
    wmarkval1 = pywt.dwt2(wmarkImage, 'haar', mode='reflect')
    wmarkval2 = pywt.dwt2(wmarkval1[0], 'haar', mode='reflect')
    wmarkval3 = pywt.dwt2(wmarkval2[0], 'haar', mode='reflect')
    
    return mainval1, mainval2, mainval3, wmarkval3


def get_from_channel( mainImage, wmarkedImage, main_image_factor, watermark_factor):
    
    mainval1, mainval2, mainval3, wmarkval3 = get_discrete_Wavelet_Value( mainImage, wmarkedImage)

    # recovering watermark image from the main image and watermarked image 
    # by doing reverse oof done during adding watermark in the watermarked imagee
    out_watermark_image = cv2.divide( cv2.subtract( wmarkval3[0], cv2.multiply( main_image_factor, mainval3[0])), watermark_factor)
    
    out_watermark_image = get_image_after_idct2( out_watermark_image, (None, None, None), ( None, None, None), ( None, None, None))
    
    return out_watermark_image


def robust_invisible_watermark_recovery(watermarked_image_path, main_image_path, out_watermark_image_path, main_image_factor, watermark_factor):
    
    watermarkedImage = cv2.imread( watermarked_image_path)
    mainImage = cv2.imread(main_image_path)
    
    mainImgSize = mainImage.shape
    
    watermarkedImage = cv2.resize( watermarkedImage, (mainImgSize[1], mainImgSize[0]))
    
    main_r, main_g, main_b = cv2.split(mainImage)
    wmarked_r, wmarked_g, wmarked_b = cv2.split( watermarkedImage)
    
    out_wmark_r = get_from_channel( main_r, wmarked_r, main_image_factor, watermark_factor)
    out_wmark_g = get_from_channel( main_g, wmarked_g, main_image_factor, watermark_factor)
    out_wmark_b = get_from_channel( main_b, wmarked_b, main_image_factor, watermark_factor)
    
    out_wmark = cv2.merge([ out_wmark_r, out_wmark_g, out_wmark_b])
    
    cv2.imwrite( out_watermark_image_path, out_wmark)

    outImage = Image.open(out_watermark_image_path)

    outImage.show()


def getArgumentForRobustInvisibleWatermarkRec():

	print(' for fragile robust watermark Recovery , enter the arguments :- ')

	watermarked_image_path = input('Enter the path of watermarked image :- ')
	main_image_path = input('Enter the path of main image :- ')
	out_watermark_image_path = input('Enter the path of image which will contain watermark message :- ')
	main_image_factor = float(input('Enter the value of scaling factor for main image rate :- '))
	watermark_factor = float(input('Enter the value of scaling factor for watermark :- '))

	robust_invisible_watermark_recovery(watermarked_image_path, main_image_path, out_watermark_image_path, main_image_factor, watermark_factor)
	print(' done successfully')


###########################################################################################################################################
######################## caller function  ################################333
#################################################################################################


if __name__ == '__main__':
    print('Watermarking Recovery Schemes \n')
    
    # print('Enter 1 for getting original image from watermarked image for visible watermarking ')
    print('Enterr 1 for getting watermark message from watermarked image for Fragile invisible watermarking ')
    print('Enter 2 for getting watermark message from watermarked image for Robust Invisible watermarking ')
    
    val = input('Enter the value :- ')
    val = int(val)
    
    if val == 1:
        print('method 1 \n')
        getArgumentForFragileInvisibleWatermarkRecov()
    elif val == 2:
        print('method 2 \n')
        getArgumentForRobustInvisibleWatermarkRec()
    else:
        print('wrong command \n')