import os
import shutil
from datetime import datetime
import fitz  # PyMuPDF para PDFs
import docx  # python-docx para DOCX

# Ruta base relativa del módulo BIC3
BASE_DIR = os.path.join(os.path.dirname(__file__), "bic3_module")

def save_uploaded_file(uploaded_file, context_type="general", empresa_id=None):
    """
    Guarda el archivo en la carpeta correspondiente según el tipo de contexto.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}__{uploaded_file.name}"

    if context_type == "general":
        save_path = os.path.join(BASE_DIR, "general_context", filename)
    elif context_type == "empresa" and empresa_id:
        save_path = os.path.join(BASE_DIR, "user_data", empresa_id, filename)
    else:
        raise ValueError("Debe especificar un tipo de contexto válido.")

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path

def extract_text_from_pdf(file_path):
    """
    Extrae texto desde un archivo PDF.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_docx(file_path):
    """
    Extrae texto desde un archivo DOCX.
    """
    text = ""
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()

def analyze_file(file_path):
    """
    Realiza el análisis del archivo: guarda copia en processed, extrae texto y crea un resumen.
    """
    processed_dir = os.path.join(BASE_DIR, "processed")
    outputs_dir = os.path.join(BASE_DIR, "outputs")

    # Copiar archivo original a carpeta processed
    shutil.copy(file_path, processed_dir)

    # Extraer texto según tipo de archivo
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        extracted_text = "⚠️ Tipo de archivo no soportado para lectura avanzada."

    # Crear archivo de salida
    output_filename = os.path.basename(file_path).replace(ext, "") + "_output.txt"
    output_path = os.path.join(outputs_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("📊 Resultado del análisis BIC3\n")
        f.write(f"Archivo: {os.path.basename(file_path)}\n\n")
        f.write("📄 Contenido extraído:\n")
        f.write(extracted_text if extracted_text else "⚠️ No se pudo extraer texto.")

    return output_path
