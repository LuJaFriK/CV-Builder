import streamlit as st
import streamlit.components.v1 as components
from webUI import construir_html
from pdf_utils import exportar_pdf
from data_manager import init_session_state, render_save_load_section
from forms import render_personal_data_form, render_work_experience_section, render_skills_section

st.set_page_config(page_title="Generador de CV Profesional", layout="wide")

def main():
    # Inicializar session_state
    init_session_state()

    # Renderizar Sidebar
    render_save_load_section()
    render_personal_data_form()
    render_work_experience_section()
    render_skills_section()

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
        st.session_state.nivel_ingles
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
