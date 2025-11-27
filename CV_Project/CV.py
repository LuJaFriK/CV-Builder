import streamlit as st
import streamlit.components.v1 as components
import os
from webUI import construir_html
from pdf_utils import exportar_pdf
from data_manager import init_session_state, render_save_load_section
from forms import render_personal_data_form, render_work_experience_section, render_skills_section, render_certifications_section

st.set_page_config(page_title="Generador de CV Profesional", layout="wide")

def main():
    # Inicializar session_state
    init_session_state()

    # Renderizar Sidebar
    render_save_load_section()
    render_personal_data_form()
    render_work_experience_section()
    render_certifications_section()
    render_skills_section()

    # Selector de Diseño
    st.sidebar.markdown("---")
    st.sidebar.header("Diseño del CV")
    
    # Detectar templates dinámicamente
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    # Listar archivos .html y quitar la extensión para el nombre
    available_templates = [f.replace('.html', '') for f in os.listdir(templates_dir) if f.endswith('.html')]
    # Ordenar alfabéticamente
    available_templates.sort()
    
    # Asegurar que 'classic' esté primero si existe, o usar el primero de la lista
    default_index = 0
    if 'classic' in available_templates:
        default_index = available_templates.index('classic')
        
    template_option = st.sidebar.selectbox(
        "Elige una plantilla",
        available_templates,
        index=default_index,
        format_func=lambda x: x.capitalize() # Mostrar nombres capitalizados (ej. classic -> Classic)
    )
    
    # El nombre del archivo es el mismo que la opción (en minúsculas)
    selected_template = template_option

    # Construir HTML para vista previa
    html_content = construir_html(
        st.session_state.foto,
        st.session_state.nombre, 
        st.session_state.titulo, 
        st.session_state.email, 
        st.session_state.telefono, 
        st.session_state.linkedin,
        st.session_state.perfil, 
        st.session_state.experiencia_laboral, 
        st.session_state.universidad, 
        st.session_state.carrera, 
        st.session_state.fecha_edu, 
        st.session_state.skills_list,
        st.session_state.certificaciones,
        st.session_state.nivel_ingles,
        template_name=selected_template
    )

    st.title("Vista Previa de tu CV")

    # Renderizamos el HTML
    components.html(html_content, height=1100, scrolling=True)

    # Generar PDF (cacheado)
    pdf_bytes = exportar_pdf(html_content)
    
    st.sidebar.download_button(
        label="📄 Descargar PDF",
        data=pdf_bytes,
        file_name="CV.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
