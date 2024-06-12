import textract  # Using textract for simplicity


def extract_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        return f"Failed to extract text: {str(e)}"
