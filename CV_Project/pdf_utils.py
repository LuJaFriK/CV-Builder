import streamlit as st
import pdfkit

@st.cache_data
def exportar_pdf(html_content):
    """
    Genera el PDF a partir del contenido HTML completo.
    html_content ya debe ser un documento HTML válido (<!DOCTYPE html>...).
    """
    # Opciones para wkhtmltopdf
    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }
    
    # Retornar bytes directamente
    return pdfkit.from_string(html_content, False, options=options)
