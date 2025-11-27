import streamlit as st
import pickle

DEFAULT_VALUES = {
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
    "skills_list": [],
    "certificaciones": []
}

def init_session_state():
    """Inicializa las variables de estado si no existen."""
    for key, value in DEFAULT_VALUES.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_save_load_section():
    """Renderiza la sección de guardar y cargar progreso en el sidebar."""
    with st.sidebar.expander("💾 Guardar / Cargar Progreso"):
        
        # CSS Hack para ocultar la zona de "Drag and drop" visualmente
        # Cargar estilos desde archivo externo
        from utils import load_file_content
        css_content = load_file_content("styles.css")
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

        # --- GUARDAR (Descargar Binario) ---
        cv_data = {key: st.session_state[key] for key in DEFAULT_VALUES.keys()}
        
        # Usar columnas para centrar el botón
        d_col1, d_col2, d_col3 = st.columns([1, 2, 1])
        with d_col2:
            st.download_button(
                label="⬇ Descargar Progreso",
                data=pickle.dumps(cv_data),
                file_name="cv_progress.cvbd",
                mime="application/octet-stream"
            )

        st.write("---")

        # --- CARGAR (Subir Binario) ---
        # Callback para cargar datos
        def load_data():
            uploaded = st.session_state.uploaded_file
            if uploaded is not None:
                try:
                    data = pickle.load(uploaded)
                    for key, value in data.items():
                        if key in DEFAULT_VALUES:
                            st.session_state[key] = value
                    st.toast("¡Progreso cargado correctamente!")
                except Exception as e:
                    st.error(f"Error al cargar el archivo: {e}")

        # Usar columnas para centrar el uploader y alinearlo con el botón de descarga
        u_col1, u_col2, u_col3 = st.columns([1, 2, 1])
        with u_col2:
            st.file_uploader(
                "📂 Cargar Progreso", 
                type=["cvbd"], 
                key="uploaded_file", 
                on_change=load_data,
                label_visibility="visible"
            )
