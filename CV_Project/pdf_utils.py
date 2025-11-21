import streamlit as st
import pdfkit
from webUI import generar_css

@st.cache_data
def exportar_pdf(html_content):
    # HTML completo con DOCTYPE + estilos inline + centrado
    html_final = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        background: #f0f0f0;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        margin: 0;
    }}

    .cv-wrapper {{
        width: 800px;
        display: flex;
        justify-content: center;
    }}

    /* Tus estilos originales */
    {generar_css()}
</style>
</head>

<body>
    <div class="cv-wrapper">
        {html_content}
    </div>
</body>
</html>
"""
    # Retornar bytes directamente
    return pdfkit.from_string(html_final, False)
