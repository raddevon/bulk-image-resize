#!/usr/bin/env python

import Image, argparse, os

parser = argparse.ArgumentParser(description='Resizes an image or several images to the desired size.', add_help=False)
parser.add_argument('filepath',
    help='Provide the path of the file or directory for image resizing.')
parser.add_argument('-c', '--copy',
    help='(Optional) Store a copy of the resized image rather than overwriting the original. The copy will have its \
         dimensions appended to the file name.',
    dest='copy', action='store_true', default=False)
parser.add_argument('-f', '--filter',
    help='(Optional) Specify a filter for resizing. Options are NEAREST, BILINEAR, BICUBIC, or ANTIALIAS.',
    dest='user_filter', action='store', metavar='filter', default=None,
    choices=['NEAREST', 'BILINEAR', 'BICUBIC', 'ANTIALIAS'])
parser.add_argument('-w', '--width',
    help='(Optional) Specify a width for the new image in pixels.',
    dest='user_width', action='store', type=int, default=0, metavar='width')
parser.add_argument('-h', '--height',
    help='(Optional) Specify a height for the new image in pixels.',
    dest='user_height', action='store', type=int, default=0, metavar='height')

args = parser.parse_args()

filters = {'NEAREST': Image.NEAREST, 'BILINEAR': Image.BILINEAR, 'BICUBIC': Image.BICUBIC, 'ANTIALIAS': Image.ANTIALIAS}

def resize(filename, new_width=None, new_height=None, resize_filter=None, copy=False):
    '''
    Function for resizing an image. Takes the filename and optional width and height arguments.
    '''

    # Open the file
    user_image = Image.open(filename)

    # Grab current image width and height
    current_width = user_image.size[0]
    current_height = user_image.size[1]

    # If values are not provided for either height or width, resize on the other dimension to maintain aspect ratio
    if new_height and not new_width:
        ratio = new_height / current_height
        new_width = current_width * ratio
    elif new_width and not new_height:
        ratio = new_width / current_width
        new_height = current_height * ratio
    elif not new_height and not new_width:
        print 'Please specify a new height, a new width, or both'

    # Set filter to ANTIALIAS if the image is getting smaller on both dimensions. Use BICUBIC for high-quality upscaling otherwise.
    if new_width < current_width and new_height < current_height and not resize_filter:
        resize_filter = Image.ANTIALIAS
    elif not resize_filter:
        resize_filter = Image.BICUBIC

    if copy:
        # Build a new filename
        file_and_path, extension = os.path.splitext(filename)
        filename = '%s-%ix%i%s' % (file_and_path, new_width, new_height, extension)

    user_image.resize((new_width, new_height), resize_filter)
    user_image.save(filename)

def main():
    """
    Determines if the argument is a file or a directory. If file, runs resize. If directory, runs resize on each file in directory.
    """
    if not args.filepath:
        print('Please supply a file or directory path.')
        return
    if os.path.isfile(args.filepath):
        resize(args.filepath, args.user_width, args.user_height, args.user_filter, args.copy)
    elif os.path.isdir(args.filepath):
        for f in os.listdir(args.filepath):
            filepath = os.path.join(args.filepath, f)
            if os.path.isfile(filepath):
                     resize(filepath, args.user_width, args.user_height, args.user_filter, args.copy)

if __name__=="__main__":
    main()
