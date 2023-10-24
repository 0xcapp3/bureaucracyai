# Requires Python 3.6 or higher due to f-strings

# Import libraries
import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def ocr_process():

	BAI_DIR = Path(__file__).expanduser().parent.parent.parent
	ROOT_DIR = Path(__file__).expanduser().parent.parent
	DOCS_DIR = ROOT_DIR / Path("docs/")
	OCR_DIR = ROOT_DIR / Path("ocr/")
	IMG_DIR = ROOT_DIR / Path("img/")

	img_is_empty = not any(IMG_DIR.iterdir())
	ocr_is_empty = not any(OCR_DIR.iterdir())
	docs_is_empty = not any(DOCS_DIR.iterdir())

	print(f"[custom_llm] docs dir is empty: {docs_is_empty}")
	print(f"[custom_llm] ocr dir is empty: {ocr_is_empty}")
	print(f"[custom_llm] img dir is empty: {img_is_empty}")

	# print("[custom_llm] ROOT_DIR:" + str(ROOT_DIR))
	# print("[custom_llm] BAI_DIR:" + str(BAI_DIR))

	# Path of the Input pdf
	# PDF_file = Path(r"d.pdf")
	# print("[custom_llm] pdf_file:" + str(PDF_file))

	# Store all the pages of the PDF in a variable
	# text_file = OCR_DIR / Path("ocr_text.txt")
	# print("[custom_llm] text_file:" + str(text_file))

	# -------------------------------------------------

	if not docs_is_empty:
		docs = [str(item) for item in DOCS_DIR.iterdir()
				if item.is_file()
				and item.name.endswith('.pdf')]
		
		for pdf in docs:
			# print(pdf)

			image_file_list = []

			tokens = pdf.split("/")
			f = tokens[-1]
			txt = f.replace(".pdf", ".txt")

			tt = f.split(".")
			n = tt[0]
			# print(n)

			TEXT_FILE_PATH = OCR_DIR / Path(txt)
			# print(TEXT_FILE_PATH)

			''' Main execution point of the program'''
			with TemporaryDirectory() as tempdir:
				# Create a temporary directory to hold our temporary images.
				"""
				Part #1 : Converting PDF to images
				"""

				if img_is_empty:
					# Read in the PDF file at 500 DPI
					pdf_pages = convert_from_path(pdf, poppler_path="", dpi=500) # handle value error

					# print("[custom_llm] pdf pages")
					# print(pdf_pages)

					# Iterate through all the pages stored above
					for page_enumeration, page in enumerate(pdf_pages, start=1):
						# enumerate() "counts" the pages for us.

						# Create a file name to store the image
						# filename = Path(f"{tempdir}/{n}_page_{page_enumeration:03}.jpg"
						filename = IMG_DIR / Path(f"{n}_page_{page_enumeration:03}.jpg")
						# print("[custom_llm] filename:" + str(filename))

						# Declaring filename for each page of PDF as JPG
						# For each page, filename will be:
						# PDF page 1 -> page_001.jpg
						# PDF page 2 -> page_002.jpg
						# PDF page 3 -> page_003.jpg
						# ....
						# PDF page n -> page_00n.jpg

						# Save the image of the page in system
						page.save(filename, "JPEG")
						image_file_list.append(filename)
					
					# print("[custom_llm] image list")
					# print(image_file_list)
					
					"""
					Part #2 - Recognizing text from the images using OCR
					"""
					if ocr_is_empty:
						with open(TEXT_FILE_PATH, "a") as output_file:
							# Open the file in append mode so that
							# All contents of all images are added to the same file

							# Iterate from 1 to total number of pages
							for image_file in image_file_list:

								# Set filename to recognize text from
								# Again, these files will be:
								# page_1.jpg
								# page_2.jpg
								# ....
								# page_n.jpg
				
								# Recognize the text as string in image using pytesserct
								text = str(((pytesseract.image_to_string(Image.open(image_file)))))

								# The recognized text is stored in variable text
								# Any string processing may be applied on text
								# Here, basic formatting has been done:
								# In many PDFs, at line ending, if a word can't
								# be written fully, a 'hyphen' is added.
								# The rest of the word is written in the next line
								# Eg: This is a sample text this word here GeeksF-
								# orGeeks is half on first line, remaining on next.
								# To remove this, we replace every '-\n' to ''.
								text = text.replace("-\n", "")

								# Finally, write the processed text to the file.
								output_file.write(text)
		

					print(f"[custom llm] ocr folder already filled with generated txts from images for {pdf}")


				print(f"[custom llm] docs already trasformed into images for {pdf}")

	else:
		print("[custom_llm] no docs found")