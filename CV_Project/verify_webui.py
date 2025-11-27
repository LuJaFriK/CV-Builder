import sys
import os
sys.path.append('/home/lujafrik/Documentos/GitHub/CV-Builder/CV_Project')
from webUI import construir_html

# Dummy data
foto = None
nombre = "Juan Perez"
titulo = "Desarrollador"
email = "juan@example.com"
telefono = "1234567890"
linkedin = "linkedin.com/in/juan"
perfil = "Perfil de prueba"
experiencia_laboral = [{"cargo": "Dev", "empresa": "Tech", "fecha": "2020-2021", "descripcion": "Code"}]
universidad = "Uni"
carrera = "Ingenieria"
fecha_edu = "2015-2019"
skills_input = ["Python", "Jinja2"]
certificaciones = [{"nombre": "Cert1", "entidad": "Entidad1", "duracion": "10h", "folio": "123"}]
nivel_ingles = "B2"

try:
    html = construir_html(foto, nombre, titulo, email, telefono, linkedin, perfil,
                          experiencia_laboral,
                          universidad, carrera, fecha_edu, skills_input, certificaciones, nivel_ingles)
    print("HTML generated successfully")
    print(html[:100]) # Print first 100 chars
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
