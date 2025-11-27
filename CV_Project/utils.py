import streamlit.components.v1 as components
import os

def load_file_content(filename):
    """Lee el contenido de un archivo."""
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        return f.read()

def inject_focus_js():
    """
    Inyecta JavaScript para manejar la navegación con Enter en los formularios.
    Lee el código desde focus_utils.js.
    """
    js_content = load_file_content("focus_utils.js")
    js_code = f"""
    <script>
    {js_content}
    </script>
    """
    components.html(js_code, height=0, width=0)

def focus_input_by_label(label_text):
    """
    Inyecta JS para poner el foco en un input que tenga cierto aria-label.
    Lee el código base de focus_utils.js y llama a la función focusInputByLabel.
    """
    js_content = load_file_content("focus_utils.js")
    js_code = f"""
    <script>
    {js_content}
    focusInputByLabel("{label_text}");
    </script>
    """
    components.html(js_code, height=0, width=0)
