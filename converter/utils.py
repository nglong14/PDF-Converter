from markitdown import MarkItDown 

def detect_type(pdf_file):
    try:
        md = MarkItDown()
        result = md.convert(pdf_file)

        if len(result.text_content.strip()) < 50:
            return "image"
        else:
            return "text"
    except Exception as e:
        print(f"Error dectecting PDF type: {e}")
        return "image"