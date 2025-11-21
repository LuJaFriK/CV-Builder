import streamlit as st
import streamlit.components.v1 as components
import pdfkit
import tempfile
import json
from web_interface import generar_css, construir_html

st.set_page_config(page_title="Generador de CV Profesional", layout="wide")

@st.cache_data
def exportar_pdf(html_content):
    import pdfkit

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






def main():
    # Inicializar session_state para todos los campos si no existen
    default_values = {
        "nombre": "Juan Pérez",
        "titulo": "Ingeniero de Software",
        "email": "juan@ejemplo.com",
        "telefono": "+52 55 1234 5678",
        "linkedin": "linkedin.com/in/juanperez",
        "perfil": "",
        "experiencia_laboral": [], # Lista de diccionarios
        "universidad": "",
        "carrera": "",
        "fecha_edu": "",
        "nivel_ingles": "B2 Intermedio",
        "skills_list": []
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.sidebar.header("📝 Ingresa tus Datos")

    # Sección de Guardar/Cargar Progreso
    with st.sidebar.expander("💾 Guardar / Cargar Progreso"):
        
        # CSS Hack para ocultar la zona de "Drag and drop" visualmente, dejar solo el botón y centrar todo
        st.markdown("""
            <style>
                /* Contenedor principal del uploader */
                [data-testid='stFileUploader'] {
                    width: 100% !important;
                }
                [data-testid='stFileUploader'] section {
                    padding: 0 !important;
                    min-height: 0 !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    width: 100% !important;
                    background-color: transparent !important;
                }
                /* El div interno que contiene el botón y el icono */
                [data-testid='stFileUploader'] section > div {
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: stretch !important; /* Estirar hijos para que ocupen todo el ancho */
                    justify-content: center !important;
                    width: 100% !important;
                    padding: 10px !important;
                    height: auto !important;
                }
                /* Ocultar textos default */
                [data-testid='stFileUploader'] section > div > div > span,
                [data-testid='stFileUploader'] section > div > div > small {
                    display: none !important;
                }
                /* Estilo para el nombre del archivo cargado */
                [data-testid='stFileUploader'] section > div > div {
                    text-align: center !important;
                    margin-top: 5px !important;
                }

                /* Botón "Browse files" */
                [data-testid='stFileUploader'] section button {
                    width: 100% !important; /* Ancho completo */
                    height: auto !important;
                    margin: 0 !important;
                    padding: 0.5rem 1rem !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                }
                /* Icono (SVG) - OCULTO */
                [data-testid='stFileUploader'] section svg {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # --- GUARDAR (Descargar JSON) ---
        cv_data = {key: st.session_state[key] for key in default_values.keys()}
        
        # Usar columnas para centrar el botón
        d_col1, d_col2, d_col3 = st.columns([1, 2, 1])
        with d_col2:
            st.download_button(
                label="⬇ Descargar Progreso (JSON)",
                data=json.dumps(cv_data, indent=4),
                file_name="cv_progress.json",
                mime="application/json"
            )

        st.write("---")

        # --- CARGAR (Subir JSON) ---
        # Callback para cargar datos
        def load_data():
            uploaded = st.session_state.uploaded_file
            if uploaded is not None:
                try:
                    data = json.load(uploaded)
                    for key, value in data.items():
                        if key in default_values:
                            st.session_state[key] = value
                    st.toast("¡Progreso cargado correctamente!")
                except Exception as e:
                    st.error(f"Error al cargar el archivo: {e}")

        # Usar columnas para centrar el uploader y alinearlo con el botón de descarga
        u_col1, u_col2, u_col3 = st.columns([1, 2, 1])
        with u_col2:
            st.file_uploader(
                "📂 Cargar Progreso (JSON)", 
                type=["json"], 
                key="uploaded_file", 
                on_change=load_data,
                label_visibility="visible"
            )

    with st.sidebar.form("cv_form"):
        st.subheader("Datos Personales")
        # Usamos key= para vincular con session_state
        st.text_input("Nombre Completo", key="nombre")
        st.text_input("Título Profesional", key="titulo")
        st.text_input("Email", key="email")
        st.text_input("Teléfono", key="telefono")
        st.text_input("LinkedIn/Web", key="linkedin")

        st.subheader("Perfil")
        st.text_area("Resumen Profesional", key="perfil")

        st.subheader("Educación")
        st.text_input("Institución", key="universidad")
        st.text_input("Carrera", key="carrera")
        st.text_input("Año de Graduación", key="fecha_edu")

        st.subheader("Nivel de Inglés")
        st.selectbox("Selecciona una opción", 
                     ["A1 Principiante", "A2 Básico", "B1 Intermedio", "B2 Intermedio", "C1 Avanzado", "C2 Nativo"],
                     key="nivel_ingles")

        submitted = st.form_submit_button("Actualizar Vista Previa")

    # --- EXPERIENCIA LABORAL (Múltiples entradas) ---
    st.sidebar.subheader("Experiencia Laboral")
    
    with st.sidebar.expander("➕ Agregar Experiencia"):
        with st.form("add_exp_form"):
            new_cargo = st.text_input("Cargo")
            new_empresa = st.text_input("Empresa")
            new_fecha = st.text_input("Fecha (Ej: 2020 - Presente)")
            new_desc = st.text_area("Descripción")
            
            add_exp_submitted = st.form_submit_button("Agregar")
            if add_exp_submitted:
                if new_cargo and new_empresa:
                    st.session_state.experiencia_laboral.append({
                        "cargo": new_cargo,
                        "empresa": new_empresa,
                        "fecha": new_fecha,
                        "descripcion": new_desc
                    })
                    st.rerun()
                else:
                    st.warning("Cargo y Empresa son obligatorios")

    # Listar experiencias agregadas
    if st.session_state.experiencia_laboral:
        st.sidebar.write("### Experiencias agregadas:")
        for i, exp in enumerate(st.session_state.experiencia_laboral):
            with st.sidebar.container():
                col_exp_text, col_exp_btn = st.columns([5, 1])
                with col_exp_text:
                    st.markdown(f"**{exp['cargo']}** en {exp['empresa']}")
                with col_exp_btn:
                    if st.button("🗑️", key=f"del_exp_{i}", help="Eliminar experiencia"):
                        st.session_state.experiencia_laboral.pop(i)
                        st.rerun()
                st.sidebar.divider()


    st.sidebar.subheader("Habilidades (una por una)")

    nueva_skill = st.sidebar.text_input("Nueva Skill")

    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button("➕ Agregar skill"):
            if nueva_skill.strip():
                st.session_state.skills_list.append(nueva_skill.strip())
                st.rerun()

    with col2:
        if st.button("🗑️ Borrar todas"):
            st.session_state.skills_list.clear()
            st.rerun()

    # CSS pequeño para ajustar la alineación y quitar viñetas
    st.sidebar.markdown(
        """
        <style>
        /* Evitar que aparezcan viñetas en markdown dentro del sidebar */
        .skill-text { list-style: none; padding: 8px 0; margin: 0; display: flex; align-items: center; }
        .skill-text p { margin: 0; padding-left: 6px; }
        /* Forzar un gap razonable entre texto y botón en dispositivos pequeños */
        .stButton button { min-width: 36px; height: 36px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.write("### Skills agregadas:")

    # CSS para alinear y estilizar
    st.sidebar.markdown("""
    <style>
    .skill-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 4px;
        background-color: rgba(255,255,255,0.05);
        border-radius: 6px;
        margin-bottom: 6px;
    }
    .skill-text {
        font-size: 15px;
        margin: 0;
    }
    .delete-btn > button {
        background: none !important;
        color: #ff4b4b !important;
        border: none !important;
        padding: 0 !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    .delete-btn > button:hover {
        color: #ff7777 !important;
        
    }
    </style>
    """, unsafe_allow_html=True)

    for i, skill in enumerate(st.session_state.skills_list):

        # Crear columnas ultra compactas
        col_text, col_btn = st.sidebar.columns([6, 1])

        with col_text:
            st.markdown(f"<div class='skill-text'>{skill}</div>", unsafe_allow_html=True)

        with col_btn:
            # botón nativo de streamlit, estilizado como "X"
            if st.button("×", key=f"del_{i}", help="Eliminar", type="secondary"):
                st.session_state.skills_list.pop(i)
                st.rerun()







    html_content = construir_html(
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

    # Renderizamos el HTML (escoge un height suficientemente grande; el script ajustará)
    
    # Renderizamos el HTML (escoge un height suficientemente grande; el script ajustará)
    
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
