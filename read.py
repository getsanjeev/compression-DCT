# Jpeg decoding

import cv2
import numpy as np
import math

# import zigzag functions
from zigzag import *

QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56 ],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
print(QUANTIZATION_MAT)

##################### step 5 #####################
# load h, w, block_size and padded_img from txt files

# load 'encoded.txt' into padded_img matrix.
# You should use np.loadtxt if you have already used np.savetxt to save them.
#padded_img = np.loadtxt('encoded.txt')

# defining block size
block_size = 8


with open('image.txt', 'r') as myfile:
    image=myfile.read()

print()
print()
details = image.split()
print(details)

h = int(''.join(filter(str.isdigit, details[0])))
w = int(''.join(filter(str.isdigit, details[1])))



print("read height & width",(h,w))
array = np.zeros(h*w).astype(int)
print("shape of array",array.shape)

k = 0
i = 2
x = 0
j = 0

print(len(details),"Length of deatils")

while k < array.shape[0]:
    if(details[i] == ';'):
        break
    #print(" I  KI VALUE",i)
    #print("value of k is : ",k)  
    print("details value",details[i])    
    if "-" not in details[i]:
        array[k] = int(''.join(filter(str.isdigit, details[i])))        
    else:
        array[k] = -1*int(''.join(filter(str.isdigit, details[i])))
        print("OCCURRED")

    #print("value at array : ",array[k])

    if(i+3 < len(details)):
        j = int(''.join(filter(str.isdigit, details[i+3])))

    if j == 0:
        k = k + 1
    else:
        #print("k prev ",k)
        print("value read for increment is : ",j)    
        k = k + j + 1
        #print("k fin", k)

    i = i + 2

    print("K value :",k)
    print()
    print()

print(array)


array = np.reshape(array,(h,w))
print("AFTER RESHAPING")
print(array)



i = 0
j = 0
k = 0

padded_img = np.zeros((h,w))

print("main image",padded_img.shape)

while i < h:
    j = 0
    while j < w:        
        temp_stream = array[i:i+8,j:j+8]
        print(temp_stream)                
        block = inverse_zigzag(temp_stream.flatten(), int(block_size),int(block_size))    
        print(block)
        print(block.shape)
        print(padded_img[i:i+8,j:j+8].shape)
        #print("Block IN LOOP : ",i,j)    
        de_quantized = np.multiply(block,QUANTIZATION_MAT)
        #print("de_QUANTIZED")
        print(de_quantized)
        padded_img[i:i+8,j:j+8] = cv2.idct(de_quantized)
        print(padded_img[i:i+8,j:j+8].astype(int))
        j = j + 8
        print()
        print()
    i = i + 8

print("COMPRESSED IMAGE")
print(np.uint8(padded_img))
padded_img[padded_img > 255] = 255
padded_img[padded_img < 0] = 0
cv2.imwrite("compressed_image.bmp",np.uint8(padded_img))



#reordered = inverse_zigzag(array, int(h), int(w))

# #print("This is from where IDCT will be calculated")

# #print(reordered.astype(int))

# # compute number of blocks by diving height and width of image by block size
# # copy from step 1
# # number of blocks in height

# nbh = math.ceil(h/block_size)##### your code #####
# nbh = np.int32(nbh)


# # number of blocks in width
# nbw = math.ceil(w/block_size)##### your code #####
# nbw = np.int32(nbw)


# ##################### step 7 #####################
# # start decoding:
# # divide encoded image into block size by block size (here: 8-by-8) blocks
# # reshape it to one dimensional array (here: 64)
# # use inverse zig-zag to reorder the array into a block
# # apply 2D inverse discrete cosine transform

# padded_img = reordered.copy()

# # iterate over blocks
# for i in range(nbh):

#         # Compute start row index of the block, same as encoder
#         row_ind_1 = i*int(block_size)##### your code #####

#         # Compute end row index of the block, same as encoder
#         row_ind_2 = row_ind_1+int(block_size)##### your code #####

#         for j in range(nbw):

#             # Compute start column index of the block, same as encoder
#             col_ind_1 = j*int(block_size)##### your code #####

#             # Compute end column index of the block, same as encoder
#             col_ind_2 = col_ind_1+int(block_size)##### your code #####

#             # select the current block we want to process using calculated indices
#             block = reordered[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2]

#             # reshape the 2D block (here: 8-by-8) to one dimensional array (here: 64)                       
#             #reshaped= np.reshape(block,(int(block_size)*int(block_size)))##### your code #####

#             # use inverse_zigzag function to scan and reorder the array into a block
#             # reordered = inverse_zigzag(reshaped, int(block_size), int(block_size))##### your code #####

#             #print("zig zag BOX")
#             #print(reshaped)

#             reordered_quantized = np.multiply(block,QUANTIZATION_MAT)
#             print("BLOCK",i,j)
#             print(reordered_quantized) 
#             # apply 2D inverse discrete cosine transform to the reordered matrix


#             IDCT = cv2.idct(reordered_quantized)

#             print("Inverse DCT BOX : ",i,j)
#             print(IDCT)

#             # copy IDCT matrix into padded_img on current block corresponding indices
#             padded_img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ] = IDCT


# padded_img = np.uint8(padded_img)
# print("Final IMAGE")
# print(padded_img)
# cv2.imshow('decoded padded image', padded_img)

# ##################### step 8 #####################
# # get the original size (h by w) image from padded_img

# decoded_img = padded_img[0:int(h),0:int(w)]##### your code #####

# cv2.imshow('decoded image', decoded_img)

##################################################

cv2.waitKey(0)
cv2.destroyAllWindows()
