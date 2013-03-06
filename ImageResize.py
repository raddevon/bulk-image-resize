import Image

def resize(filename, width = None, height = None):
	'''
	Function for resizing an image. Takes the filname and optional width and height arguments.
	'''

	# Open the file
	user_image = Image.open(filename)

	# Grab current image width and height
	current_width = user_image.size[0]
	current_height = user_image.size[1]
	
	# to-do Test for neither image nor height dimension

	# If values are not provided for either height or width, resize on the other dimension to maintain aspect ratio
	if height not width:
		ratio = height / current_height
		width = current_width * ratio
	if width not height:
		ratio = width / current_width
		height = current_height * ratio

	# Set filter to ANTIALIAS if the image is getting smaller on both dimensions. Use BICUBIC for high-quality upscaling otherwise.
	if width < current_width and height < current_height:
		resize_filter = Image.ANTIALIAS
	else:
		resize_filter = Image.BICUBIC

	user_image.resize((width, height), resize_filter)
	user_image.save(filename)

