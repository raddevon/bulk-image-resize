#!/usr/bin/env python

from __future__ import division
import Image, argparse, os

parser = argparse.ArgumentParser(description='Resizes an image or several images to the desired size.', add_help=False)
parser.add_argument('filepath',
    help='Provide the path of the file or directory for image resizing.', metavar='PATH')
parser.add_argument('-c', '--copy',
    help='(Optional) Store a copy of the resized image rather than overwriting the original. The copy will have its \
         dimensions appended to the file name.',
    dest='copy', action='store_true', default=False)
parser.add_argument('-f', '--filter',
    help='(Optional) Specify a filter for resizing. Options are NEAREST, BILINEAR, BICUBIC, or ANTIALIAS.',
    dest='user_filter', action='store', metavar='FILTER', default=None,
    choices=['NEAREST', 'BILINEAR', 'BICUBIC', 'ANTIALIAS'])
parser.add_argument('-w', '--width',
    help='(Optional) Specify a width for the new image in pixels.',
    dest='user_width', action='store', type=int, default=0, metavar='XXX')
parser.add_argument('-h', '--height',
    help='(Optional) Specify a height for the new image in pixels.',
    dest='user_height', action='store', type=int, default=0, metavar='XXX')
parser.add_argument('--help', help='Displays the help message', action='help')

args = parser.parse_args()

def calculate_dimensions(current_width, current_height,width=None, height=None):
    """
    If values are not provided for either height or width, resize on the other dimension to maintain aspect ratio
        current_width: Width of the image
        current_height: Height of the image
        width: New width of the resized image
        height: New height of the resized image
    """
    if height and not width:
        ratio = height / current_height
        width = current_width * ratio
        width = int(width)
    elif width and not height:
        ratio = width / current_width
        height = current_height * ratio
        height = int(height)
    elif not height and not width:
        print 'Please specify a new height, a new width, or both.'

    return width, height

def set_filter(current_width, current_height, new_width, new_height, resize_filter=None):
    """
    Set resize_filter to ANTIALIAS if the image is getting smaller on both dimensions. Use BICUBIC for high-quality
    upscaling otherwise. Override defaults with the user specified filter if it is provided.
    """
    filters = {'NEAREST': Image.NEAREST, 'BILINEAR': Image.BILINEAR, 'BICUBIC': Image.BICUBIC,
               'ANTIALIAS': Image.ANTIALIAS}

    if new_width < current_width and new_height < current_height and not resize_filter:
        return Image.ANTIALIAS
    elif not resize_filter:
        return Image.BICUBIC

    return filters[resize_filter]

def resize(filename, width=None, height=None, resize_filter=None, copy=False):
    '''
    Function for resizing an image. Takes the filename and optional width and height arguments.
    '''

    # Open the file
    user_image = Image.open(filename)

    # Grab the original filename
    original_filename = filename

    # Grab current image width and height
    current_width = user_image.size[0]
    current_height = user_image.size[1]

    width, height = calculate_dimensions(current_width, current_height, width, height)
    resize_filter = set_filter(current_width, current_height, width, height, resize_filter)

    if copy:
        # Build a new filename
        file_and_path, extension = os.path.splitext(filename)
        filename = '%s-%ix%i%s' % (file_and_path, width, height, extension)

    if width == current_width and height == current_height:
        print 'Image dimensions did not change for %s' % original_filename
    else:
        user_image = user_image.resize((width, height), resize_filter)
        user_image.save(filename)

def main():
    """
    Determines if the argument is a file or a directory. If file, runs resize. If directory, runs resize on each file in
    directory.
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