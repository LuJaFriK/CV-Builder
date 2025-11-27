import streamlit as st
from utils import inject_focus_js, focus_input_by_label

def render_personal_data_form():
    inject_focus_js()
    st.sidebar.header("📝 Ingresa tus Datos")

    with st.sidebar.expander("📸 Foto de Perfil"):
        st.file_uploader("Subir foto (Opcional)", type=['png', 'jpg', 'jpeg'], key="foto")

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

        st.form_submit_button("Actualizar Vista Previa")

    st.sidebar.subheader("Nivel de Inglés")
    st.sidebar.selectbox("Selecciona una opción", 
                    ["Ninguno", "A1 Principiante", "A2 Básico", "B1 Intermedio", "B2 Intermedio", "C1 Avanzado", "C2 Nativo"],
                    key="nivel_ingles")

def render_work_experience_section():
    st.sidebar.subheader("Experiencia Laboral")
    
    with st.sidebar.expander("➕ Agregar Experiencia"):
        with st.form("add_exp_form", clear_on_submit=True):
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
                    # st.rerun()  <-- Eliminado para evitar recarga completa
                    focus_input_by_label("Cargo")
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

def render_skills_section():
    st.sidebar.subheader("Habilidades (una por una)")

    # Callback para agregar skill
    def add_skill_callback():
        # Obtenemos el valor del input desde session_state
        skill_val = st.session_state.new_skill_input
        if skill_val and skill_val.strip():
            st.session_state.skills_list.append(skill_val.strip())
            # Limpiamos el input
            st.session_state.new_skill_input = ""

    with st.sidebar.expander("➕ Agregar Habilidad"):
        # Input con callback (se ejecuta al dar Enter)
        st.text_input("Nueva Skill", key="new_skill_input", on_change=add_skill_callback)

        col1, col2 = st.columns([1, 1])
        with col1:
            # Botón con callback (se ejecuta al hacer click)
            st.button("➕ Agregar skill", on_click=add_skill_callback)

        with col2:
            if st.button("🗑️ Borrar todas"):
                st.session_state.skills_list.clear()
                # No necesitamos rerun explícito si usamos callbacks para lo anterior, 
                # pero para este botón simple sí, o podríamos usar callback también.
                # Dejamos rerun por simplicidad aquí.
                st.rerun()

    # CSS pequeño para ajustar la alineación y quitar viñetas
    # Cargar estilos desde archivo externo
    from utils import load_file_content
    css_content = load_file_content("styles.css")
    st.sidebar.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    if st.session_state.skills_list:
        st.sidebar.write("### Skills agregadas:")

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

def render_certifications_section():
    st.sidebar.subheader("Certificaciones y Diplomados")
    
    with st.sidebar.expander("➕ Agregar Certificación"):
        with st.form("add_cert_form", clear_on_submit=True):
            new_cert = st.text_input("Nombre del Certificado")
            new_entidad = st.text_input("Entidad Emisora / Plataforma")
            new_duracion = st.text_input("Duración (Ej: 40 horas, 3 meses)")
            new_folio = st.text_input("Folio o ID (Opcional)")
            
            add_cert_submitted = st.form_submit_button("Agregar")
            if add_cert_submitted:
                if new_cert and new_entidad:
                    st.session_state.certificaciones.append({
                        "nombre": new_cert,
                        "entidad": new_entidad,
                        "duracion": new_duracion,
                        "folio": new_folio
                    })
                    focus_input_by_label("Nombre del Certificado")
                else:
                    st.warning("Nombre y Entidad son obligatorios")

    # Listar certificaciones agregadas
    if st.session_state.certificaciones:
        st.sidebar.write("### Certificaciones agregadas:")
        for i, cert in enumerate(st.session_state.certificaciones):
            with st.sidebar.container():
                col_cert_text, col_cert_btn = st.columns([5, 1])
                with col_cert_text:
                    st.markdown(f"**{cert['nombre']}** - {cert['entidad']}")
                with col_cert_btn:
                    if st.button("🗑️", key=f"del_cert_{i}", help="Eliminar certificación"):
                        st.session_state.certificaciones.pop(i)
                        st.rerun()
                st.sidebar.divider()
