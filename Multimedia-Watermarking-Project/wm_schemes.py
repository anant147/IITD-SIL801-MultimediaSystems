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

def visible_Watermarking(main_image_path, Watermark_message, output_image_path, text_size, position):
    
    # opening image in main path 
    outImage = Image.open(main_image_path)
    tempImage = ImageDraw.Draw(outImage)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", text_size)
    tempImage.text(position , Watermark_message, fill= (0,0,0) , font = font)

    # showing output image
    outImage.show()
    outImage.save(output_image_path)

def getArgumentForVisibleWatermark():

	print(" for Visible watermarking , enter the arguments :- \n")

	main_image_path = input('Enter the path of main image :- ')
	Watermark_message = input('Enter the watermark message :- ')
	output_image_path = input('Enter the path of output watermarked image :- ')
	text_size = int(input(' Enter the size of watermark message :- '))

    # default postion , can be changed 
	position = (0,0)

	visible_Watermarking(main_image_path, Watermark_message, output_image_path, text_size, position)
	print("visible watermarking done successfully \n ")

##################################################################################################################################################
############################################ method 2 ######################################################################
##################################################################################################################################################

def get_inserting_content( watermark_message):
    
    endcheck = '#$$#'
    
    msg = watermark_message + endcheck
    
    content = []
    zlen = 16
    
    for c in msg:
        u = ord(c)
        v = bin(u)
        x = v[2:]
        y = x.zfill(zlen)
        for i in range(zlen):
            content.append(int(y[i]))
    
    return content


def fragile_invisible_Watermarking( main_image_path, watermark_message, output_image_path):
    
    mainImage = Image.open(main_image_path)
    mainArr = np.array(mainImage)
    
    # using function to get watermark message into appropriate form 
    insertingText = get_inserting_content( watermark_message)
    
    intextlen = len(insertingText)
    
    # parameters of array formed from image
    rows = mainArr.shape[0]
    cols = mainArr.shape[1]
    channels = mainArr.shape[2]
    
    ctr = 0
    
    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                if ctr < intextlen:
                    # inserting value into the array of image
                    mainArr[i][j][k] = 0
                    mainArr[i][j][k] = insertingText[ctr]
                    ctr += 1
                    
    
    newImage = Image.fromarray(mainArr)

    # showing new image
    newImage.show()
    newImage.save(output_image_path)


def getArgumentForFragileInvisibleWatermark():

	print(" for fragile invisible watermarking, enter the arguments :- \n ")

	main_image_path = input('Enter the path of main image :- ')
	watermark_message = input('Enter the watermark message :- ')
	output_image_path = input('Enter the path of output watermarked image :- ')

	fragile_invisible_Watermarking( main_image_path, watermark_message, output_image_path)
	print("fragile watermarking done successfully ")

##################################################################################################################################################
############################################ method 3 ######################################################################
##################################################################################################################################################

def get_discrete_Wavelet_Value( mainImage, wmarkImage):

    # doing 3-d wavelet haar transform of main image 
    mainval1 = pywt.dwt2(mainImage, 'haar', mode='reflect')
    mainval2 = pywt.dwt2(mainval1[0], 'haar', mode='reflect')
    mainval3 = pywt.dwt2(mainval2[0], 'haar', mode='reflect')

    # doing 3-d wavelet haar transform of water mark image
    wmarkval1 = pywt.dwt2(wmarkImage, 'haar', mode='reflect')
    wmarkval2 = pywt.dwt2(wmarkval1[0], 'haar', mode='reflect')
    wmarkval3 = pywt.dwt2(wmarkval2[0], 'haar', mode='reflect')

    # return required component of both images
    return mainval1, mainval2, mainval3, wmarkval3

def get_image_after_idct2(img, val1, val2, val3):

    # doing 3-d inverse wavelet haar transfrom of given image with given parameters
    # when parameters have no value
    # then default value is (None, None, None)
    pr3 = (img, val3)
    img = pywt.idwt2(pr3, 'haar', mode = 'reflect')
    
    pr2 = (img, val2)
    img = pywt.idwt2(pr2, 'haar', mode = 'reflect')
    
    pr1 = (img, val1)
    img = pywt.idwt2(pr1, 'haar', mode = 'reflect')
    
    return img

def inserting_in_channel( mainImage , wmarkImage, main_image_factor, watermark_factor ):

    # getting 3-d discrete wavelet tranform of the both images.
    mainval1, mainval2, mainval3, wmarkval3 = get_discrete_Wavelet_Value( mainImage, wmarkImage)

    # adding the component of main image and watermark image after multiplying with their respective scaling factors
    outImage = cv2.add(cv2.multiply(main_image_factor, mainval3[0]), cv2.multiply( watermark_factor, wmarkval3[0]))

    # getting output image by doing reconstruction process on above image with the components of main image
    outImage = get_image_after_idct2(outImage, mainval1[1], mainval2[1], mainval3[1])
    
    np.clip( outImage, 0, 255, out = outImage)
    outImage = outImage.astype('uint8')
    
    return outImage

def inserting_Watermark( mainImage, wmarkImage, main_image_factor, watermark_factor):
    
    mainImgSize = mainImage.shape
    wmarkImage = cv2.resize( wmarkImage,( mainImgSize[1], mainImgSize[0]))
    
    main_r, main_g, main_b = cv2.split(mainImage)
    wmark_r, wmark_g, wmark_b = cv2.split( wmarkImage)

    # inserting watermark image channel in each channel of main image
    out_r = inserting_in_channel( main_r, wmark_r, main_image_factor, watermark_factor)
    out_g = inserting_in_channel( main_g, wmark_g, main_image_factor, watermark_factor)
    out_b = inserting_in_channel( main_b, wmark_b, main_image_factor, watermark_factor)
    
    outImage = cv2.merge([ out_r, out_g, out_b])
    
    return outImage


def make_image_from_watermark_msg( watermark_message):

    # making image from given message
    tempImage = Image.new("RGB", (512, 512), (255, 255, 255))
    fnt = ImageFont.truetype("Pillow/Tests/fonts/Roboto-Bold.ttf",100)
    drawing = ImageDraw.Draw(tempImage)
    drawing.text((10,10), watermark_message, font=fnt, fill=(0, 0, 0))
    
    temp_Watermark_image_path = 'Watermark_method3.png'
    
    tempImage.save(temp_Watermark_image_path)
    
    return cv2.imread(temp_Watermark_image_path)


def robust_invisible_Watermarking( main_image_path, watermark_message, output_image_path, main_image_factor, watermark_factor):
    
    mainImage = cv2.imread( main_image_path)
    
    wmarkImage = make_image_from_watermark_msg( watermark_message)
    
    output_image = inserting_Watermark( mainImage, wmarkImage, main_image_factor, watermark_factor)
    
    cv2.imwrite( output_image_path, output_image)

    outImage = Image.open(output_image_path)

    outImage.show()
    


def getArgumentForRobustInvisibleWatermark():

	print(" for robust invisible watermarking, enter the arguments :- \n ")

	main_image_path = input('Enter the path of main image :- ')
	watermark_message = input('Enter the watermark message :- ')
	output_image_path = input('Enter the path of the output watermarked image :- ')
	main_image_factor = float(input('Enter the value of scaling factor for main image rate :- '))
	watermark_factor = float(input('Enter the value of scaling factor for watermark :- '))

	robust_invisible_Watermarking( main_image_path, watermark_message, output_image_path, main_image_factor, watermark_factor)
	print(" robust watermarking done successfully ")

##################################################################################################################################################
############################################ caller  ######################################################################
##################################################################################################################################################

if __name__ == '__main__':
    print('Watermarking Schemes \n')
    
    print('Enter 1 for Visible Watermarking')
    print('Enterr 2 for Fragile invisible watermarking ')
    print('Enter 3 for Robust Invisible watermarking ')
    
    val = input('Enter the value :-')
    val = int(val)
    
    if val == 1:
        print('method 1 \n')
        getArgumentForVisibleWatermark()

    elif val == 2:
        print('method 2 \n')
        getArgumentForFragileInvisibleWatermark()

    elif val == 3:
        print('method 3 \n')
        getArgumentForRobustInvisibleWatermark()
    else:
        print('wrong command \n')