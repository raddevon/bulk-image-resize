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
	if new_height not new_width:
		ratio = new_height / current_height
		new_width = current_width * ratio
	if width not height:
		ratio = new_width / current_width
		new_height = current_height * ratio

	# Set filter to ANTIALIAS if the image is getting smaller on both dimensions. Use BICUBIC for high-quality upscaling otherwise.
	if user_filter in filters:
		resize_filter = filters[user_filter]
	elif new_width < current_width and new_height < current_height:
		resize_filter = Image.ANTIALIAS

	user_image.resize((new_width, new_height), resize_filter)
	user_image.save(filename)

def main():
	'''
	Determines if the argument is a file or a directory. If file, runs resize. If directory, runs resize on each file in directory.
	'''
	if os.path.isfile(args[0]):
		resize(args, user_width, user_height, user_filter)
	elif os.path.isdir(args[0]):
		for f in os.listdir(args[0]):
			if os.path.isfile(f):
				resize(args, user_width, user_height, user_filter)

if __name__=="__main__":
	main()
