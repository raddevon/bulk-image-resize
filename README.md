# ImageResize

This script resizes an image or all images in a folder.

    ImageResize.py PATH [-h XXX] [-w XXX] [-f NEAREST|BILINEAR|BICUBIC|ANTIALIAS] [-c] [--help]

Run the script with the path to image file or a folder containing images as a parameter. Add in either the height or
width in pixels (or both) using the `-h` or `-w` options respectively. Use `-f` followed by a resize filter (`NEAREST`,
`BILINEAR`, `BICUBIC`, or `ANTIALIAS` to specify the filter to be used in the resize. If you do not specify, an
appropriate filter will be chosen for you. Use `-c` to make a copy of the image with the new dimesions instead of
 overwriting the original. This will create a copy of the original file with the dimensions appended to the file name.