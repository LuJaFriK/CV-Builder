# Generador de CV Profesional

Este proyecto es una aplicación web construida con [Streamlit](https://streamlit.io/) que permite a los usuarios crear, visualizar y exportar su Currículum Vitae (CV) de manera profesional y sencilla.

## Características

- **Ingreso de Datos Personales**: Nombre, título, contacto, perfil profesional, etc.
- **Gestión de Experiencia Laboral**: Permite agregar múltiples experiencias laborales con cargo, empresa, fecha y descripción.
- **Habilidades (Skills)**: Agrega y elimina habilidades de forma dinámica.
- **Educación e Idiomas**: Secciones dedicadas para formación académica y nivel de inglés.
- **Vista Previa en Tiempo Real**: Visualiza cómo quedará tu CV mientras editas los datos.
- **Exportación a PDF**: Descarga tu CV listo para enviar en formato PDF.
- **Guardar y Cargar Progreso**: Guarda tus datos en un archivo JSON y retoma la edición más tarde.

## Requisitos

Para ejecutar este proyecto necesitas tener instalado Python y las siguientes librerías:

- `streamlit`
- `pdfkit`

Además, `pdfkit` requiere que tengas instalado **wkhtmltopdf** en tu sistema para la generación de PDFs.

### Instalación de dependencias de Python

```bash
pip install streamlit pdfkit
```

### Instalación de wkhtmltopdf

- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install wkhtmltopdf
  ```
- **Windows/Mac**: Descarga el instalador desde [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).

## Uso

1. Clona este repositorio o descarga los archivos.
2. Navega al directorio del proyecto:
   ```bash
   cd CV_Project
   ```
3. Ejecuta la aplicación de Streamlit:
   ```bash
   streamlit run CV.py
   ```
4. La aplicación se abrirá automáticamente en tu navegador.

## Estructura del Proyecto

- `CV.py`: Archivo principal de la aplicación. Contiene la lógica de la interfaz de usuario y el flujo de datos.
- `web_interface.py`: Módulo auxiliar que maneja la generación de estilos CSS y la estructura HTML del CV.
- `profiles/`: Directorio para almacenar perfiles (si aplica).
