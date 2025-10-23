import os
import pdf2image
import numpy as np
import easyocr
from markitdown import MarkItDown
from .preprocess import image_preprocess
from .utils import detect_type
from refiner.clean import clean_text

poppler_path = r'D:\Release-25.07.0-0\poppler-25.07.0\Library\bin'

def convert_text_pdf(pdf_file, output_folder):
    try:
        md = MarkItDown()
        result = md.convert(pdf_file)

        md_filename = os.path.basename(pdf_file).replace('.pdf', '.md')
        output_path = os.path.join(output_folder, md_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"Converted {pdf_file} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_file}: {e}")
        return False

def convert_image_pdf(pdf_file, output_folder):
    try:
        pages = pdf2image.convert_from_path(pdf_file, dpi=300, poppler_path = poppler_path)

        pdf_name = os.path.basename(pdf_file)
        all_text = f"# {pdf_name}\n\n"
        reader = easyocr.Reader(['vi'])

        for i, page in enumerate(pages):
            page = image_preprocess(page)
            page = np.array(page)
            text = reader.readtext(page, detail = 0)
            text = '\n'.join(text)
            text = clean_text(text)

            if text.strip():
                all_text += f'## {i+1}\n\n{text}\n\n'

        md_filename = os.path.basename(pdf_file).replace('.pdf', '.md')
        output_path = os.path.join(output_folder, md_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(all_text)
        
        print(f"Converted {pdf_file} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_file}: {e}")
        return False
    
def smart_convert_pdf(pdf_file, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_type = detect_type(pdf_file)
    print(f"Detected PDF type: {pdf_type}")
    
    if pdf_type == "text":
        return convert_text_pdf(pdf_file, output_folder)
    else:
        return convert_image_pdf(pdf_file, output_folder)
