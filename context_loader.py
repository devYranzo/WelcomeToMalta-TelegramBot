"""
context_loader.py
-----------------
Lee los archivos de la carpeta /knowledge_base y los combina como
contexto para Gemini.

FORMATOS SOPORTADOS:
  - PDF  (.pdf)  → Creado desde Word, Google Docs, etc.
  - Texto (.txt) → Archivo de texto plano

CÓMO CONTROLAR QUÉ SABE EL BOT:
  - Añadir info     → Sube un PDF o .txt a la carpeta knowledge_base/
  - Quitar info     → Borra el archivo o muévelo fuera de la carpeta
  - Editar info     → Reemplaza el archivo por la nueva versión
  - El bot recarga los archivos cada 50 mensajes sin necesidad de reiniciar
"""

import os
import re
from typing import Dict

try:
    import pdfplumber as _pdfplumber
    PDF_SUPPORT = True
except ImportError:
    _pdfplumber = None  # type: ignore
    PDF_SUPPORT = False

KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")


def _read_pdf(filepath: str) -> str:
    """Extrae el texto de un PDF usando pdfplumber."""
    if not PDF_SUPPORT:
        return "[PDF support not available — run: pip install pdfplumber]"
    try:
        text_parts = []
        with _pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text.strip())
        return "\n\n".join(text_parts)
    except Exception as e:
        return f"[Error reading PDF: {e}]"


def _read_txt(filepath: str) -> str:
    """Lee un archivo de texto plano."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Elimina las líneas de metadatos (# TOPIC:, # ENABLED:, etc.)
        content = re.sub(r"^#.*\n?", "", content, flags=re.MULTILINE)
        return content.strip()
    except Exception as e:
        return f"[Error reading file: {e}]"


def load_knowledge_base() -> str:
    """
    Carga todos los archivos soportados de knowledge_base/
    y devuelve el texto combinado como contexto.
    """
    if not os.path.exists(KB_DIR):
        return ""

    parts = []

    for filename in sorted(os.listdir(KB_DIR)):
        filepath = os.path.join(KB_DIR, filename)
        name = os.path.splitext(filename)[0]  # nombre sin extensión
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            content = _read_pdf(filepath)
        elif ext == ".txt":
            # Soporte para el flag ENABLED en .txt (opcional)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            enabled_match = re.search(r"#\s*ENABLED:\s*(true|false)", raw, re.IGNORECASE)
            if enabled_match and enabled_match.group(1).lower() == "false":
                continue
            content = _read_txt(filepath)
        else:
            continue  # Ignora otros formatos

        if content.strip():
            parts.append(f"=== {name.upper()} ===\n{content}")

    return "\n\n".join(parts)


def get_loaded_topics() -> Dict[str, str]:
    """
    Devuelve un dict {nombre_archivo: formato} de los archivos en el KB.
    Útil para el comando /status del bot.
    """
    topics = {}
    if not os.path.exists(KB_DIR):
        return topics

    for filename in sorted(os.listdir(KB_DIR)):
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0]
        if ext in (".pdf", ".txt"):
            topics[name] = ext.replace(".", "").upper()

    return topics
