import os
from wand.image import Image

########## Twikeables ####################

path_files ='/certificates/files'
pdf_to_image_res = 300

for file in os.listdir(path_files):
	file_path = os.path.join(path_files, file)
	file_name, file_extension = os.path.splitext(file)

	if file.endswith((".pdf")):
		try:
			file_name, file_extension = os.path.splitext(file_path)
		
			with Image(filename=file_path, resolution=pdf_to_image_res) as img:
				print('pages = ', len(img.sequence))
			 
				with img.convert('jpg') as converted:
					converted.save(filename=file_name+'page.jpg')
		except IOError:
			print 'cannot convert', arg
		