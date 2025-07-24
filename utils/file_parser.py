import docx2txt
import fitz  # PyMuPDF

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        text = ""
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text

    elif file_type in ["docx", "doc"]:
        return docx2txt.process(uploaded_file)

    else:
        return "Unsupported file type."
