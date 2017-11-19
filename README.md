# compression-DCT

(for learning purposes to understand RLE encoding)

Basic implementation of image compression using DCT has been done. Note that JPEG compression exploits many other techniques to achieve 
higher compression. Here only Quantization (lossy step) & Run length encoding has been done.

The working can be simply explained as : 
1. image2RLE reads an image and performs DCT, applies quantization (Q-Matrix taken is standard JPEG matrix obtained from psycho-visual)
experiments) and encodes it using Run Length Encoding.
2. Encoded data is written onto a text file with name image.txt {this text file has lesser bytes than original image  = Compression}
3. RLE2image reads image.txt and decodes it into image again, writing a new compressed image onto disk. 

The compressed image has block-artifacts which can be seen easily.

One can read about DCT-image compression from : https://www.youtube.com/watch?v=sckLJpjH5p8 NPTEL IMAGE PROCESSING SERIES

credits : 
1. zigzag.py has been taken from : https://github.com/amzhang1/simple-JPEG-compression
2. https://github.com/abhishek-sehgal954/Lossy-and-lossless-image-compression-techniques



