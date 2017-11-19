# Jpeg encoding

import cv2
import numpy as np
import math

# import zigzag functions
from zigzag import *


def get_run_length_encoding(image):
    i = 0
    skip = 0
    stream = []    
    bitstream = ""
    image = image.astype(int)
    while i < image.shape[0]:
        if image[i] != 0:            
            stream.append((image[i],skip))
            bitstream = bitstream + str(image[i])+ " " +str(skip)+ " "
            skip = 0
        else:
            skip = skip + 1
        i = i + 1

    return bitstream

# defining block size
block_size = 8

# Quantization Matrix
QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56 ],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
print(QUANTIZATION_MAT)

# reading image in grayscale
img = cv2.imread('emma.png', cv2.IMREAD_GRAYSCALE)
#img = np.array([[255,255,227,204,204,203,192,217],[215,189,167,166,160,135,167,244],[169,115,99,99,99,82,127,220],[146,90,86,88,84,63,195,189],[255,255,231,239,240,182,251,232],[255,255,21,245,226,169,229,247],[255,255,222,251,174,209,174,163],[255,255,221,184,205,248,249,220]])

print("Image read : ")
print(img)

# get size of the image
[h , w] = img.shape


##################### step 1 #####################
# compute number of blocks by diving height and width of image by block size

# you need to convert h and w to float to get the right number
height = h
width = w
h = np.float32(h) ##### your code #####
w = np.float32(w) ##### your code #####

# to cover the whole image the number of blocks should be ceiling of the division of image size by block size
# at the end convert it to int

# number of blocks in height
nbh = math.ceil(h/block_size)##### your code #####
nbh = np.int32(nbh)

# number of blocks in width
nbw = math.ceil(w/block_size)##### your code #####
nbw = np.int32(nbw)

##################### step 2 #####################

# Pad the image, because sometime image size is not dividable to block size
# get the size of padded image by multiplying block size by number of blocks in height/width

# height of padded image
H =  block_size * nbh##### your code #####

# width of padded image
W =  block_size * nbw##### your code #####

# create a numpy zero matrix with size of H,W
padded_img = np.zeros((H,W))

# copy the values of img  into padded_img[0:h,0:w]
for i in range(height):
        for j in range(width):
                pixel = img[i,j]
                padded_img[i,j] = pixel ##### your code #####

# or this other way here
#padded_img[0:h,0:w] = img[0:h,0:w]

print("Padded images :")
print(padded_img.astype(int))
cv2.imwrite('uncompressed.bmp', np.uint8(padded_img))

#cv2.imshow('input padded image', np.uint8(padded_img).astype(int))


# start encoding:
# divide image into block size by block size (here: 8-by-8) blocks
# To each block apply 2D discrete cosine transform
# reorder DCT coefficients in zig-zag order
# reshaped it back to block size by block size (here: 8-by-8)


# iterate over blocks
for i in range(nbh):
    
        # Compute start row index of the block
        row_ind_1 = i*block_size
        
        # Compute end row index of the block
        row_ind_2 = row_ind_1+block_size
        
        for j in range(nbw):
            
            # Compute start column index of the block
            col_ind_1 = j*block_size
            
            # Compute end column index of the block
            col_ind_2 = col_ind_1+block_size
            
            # select the current block we want to process using calculated indices
            block = padded_img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ]
                       
            # apply 2D discrete cosine transform to the selected block
            # you should use opencv dct function
            print("BLOCK : ",i,j)
            print(block)
            DCT = cv2.dct(block)

            print("Box : DCT",i,j)
            print(DCT.astype(int))

            DCT_normalized = np.divide(DCT,QUANTIZATION_MAT).astype(int)
            print("AFTER QUantization")
            print(DCT_normalized)
            
            # reorder DCT coefficients in zig zag order by calling zigzag function
            # it will give you a one dimentional array
            reordered = zigzag(DCT_normalized)                      
            # reshape the reorderd array back to (block size by block size) (here: 8-by-8)
            reshaped= np.reshape(reordered, (block_size, block_size)) 
            
            # copy reshaped matrix into padded_img on current block corresponding indices
            padded_img[row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2] = reshaped
            print()
            print()

cv2.imshow('encoded image', np.uint8(padded_img))

print("DCT matrix FINAL")
print(padded_img.astype(int))
arranged = padded_img.flatten()
#arranged = np.reshape(padded_img.astype(int),(1,padded_img.size))
print(arranged.astype(int))
print()
bitstream = get_run_length_encoding(arranged)
bitstream = str(padded_img.shape[0]) + " " + str(padded_img.shape[1]) + " " + bitstream + ";"

print("Bitstream : ")
print(bitstream)

##################### step 4 #####################
# write h, w, block_size and padded_img into txt files at the end of encoding

# write padded_img into 'encoded.txt' file. You can use np.savetxt function.
#np.savetxt('encoded.txt',bitstream)##### your code #####

# write [h, w, block_size] into size.txt. You can use np.savetxt function.
#np.savetxt('size.txt',[h, w, block_size])##### your code #####
file1 = open("image.txt","w")
file1.write(bitstream)
file1.close()

##################################################

cv2.waitKey(0)
cv2.destroyAllWindows()




