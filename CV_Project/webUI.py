#Las funciones que se encargan de generar el CSS y el HTML
import base64
import os
from jinja2 import Environment, FileSystemLoader

def construir_html(foto, nombre, titulo, email, telefono, linkedin, perfil,
                    experiencia_laboral,
                    universidad, carrera, fecha_edu, skills_input, certificaciones, nivel_ingles):

    # Procesar foto si existe
    foto_url = ""
    if foto:
        try:
            # Convertir a base64
            b64_img = base64.b64encode(foto.getvalue()).decode('utf-8')
            mime_type = foto.type
            foto_url = f"data:{mime_type};base64,{b64_img}"
        except Exception as e:
            print(f"Error procesando imagen: {e}")

    # Configurar Jinja2
    # Asumimos que el template está en el mismo directorio que este script
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('cv_template.html')

    # Renderizar el template
    html_content = template.render(
        foto_url=foto_url,
        nombre=nombre,
        titulo=titulo,
        email=email,
        telefono=telefono,
        linkedin=linkedin,
        perfil=perfil,
        experiencia_laboral=experiencia_laboral,
        universidad=universidad,
        carrera=carrera,
        fecha_edu=fecha_edu,
        skills_input=skills_input,
        certificaciones=certificaciones,
        nivel_ingles=nivel_ingles
    )

    return html_content