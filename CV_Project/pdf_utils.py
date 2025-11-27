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
        'enable-local-file-access': None,
        'disable-smart-shrinking': None,
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm'
    }
    
    # Retornar bytes directamente
    return pdfkit.from_string(html_content, False, options=options)
