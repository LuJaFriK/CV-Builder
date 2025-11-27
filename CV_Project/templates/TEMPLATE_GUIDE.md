# Guía para Crear Plantillas de CV (CV Builder)

Esta guía está diseñada para desarrolladores y modelos de IA que necesiten crear nuevas plantillas para el proyecto CV Builder.

## ⚠️ Reglas Críticas de Compatibilidad (PDF)

El sistema utiliza `wkhtmltopdf` para generar los PDFs. Este motor es antiguo y **NO soporta** características modernas de CSS correctamente. Para garantizar que el texto sea seleccionable y el diseño no se rompa, DEBES seguir estas reglas:

### 1. Estructura (Layout)
*   **PROHIBIDO**: Usar `display: flex` o `display: grid` para la estructura principal (columnas). Esto causa que el texto se rasterice (se convierta en imagen) o que el diseño se rompa.
*   **OBLIGATORIO**: Usar **Tablas HTML (`<table>`)** para el diseño de columnas.
    *   Ejemplo: Una tabla con una fila (`<tr>`) y dos celdas (`<td>`) para un diseño de dos columnas.
    *   Usa atributos HTML antiguos para ancho y color de fondo si es necesario: `<td width="30%" bgcolor="#333">`.

### 2. Fuentes (Fonts)
*   **PROHIBIDO**: Usar `@import` o `<link>` para cargar fuentes externas (Google Fonts, etc.). `wkhtmltopdf` a menudo falla al descargarlas, lo que rompe la generación del PDF.
*   **OBLIGATORIO**: Usar fuentes del sistema estándar.
    *   Stack recomendado: `font-family: "Roboto", "Segoe UI", Helvetica, Arial, sans-serif;`

### 3. CSS
*   Puedes usar CSS moderno para estilos de texto (colores, tamaños, negritas), padding y margin dentro de los bloques.
*   Evita `gap`, `transform`, o animaciones complejas.

## Variables Disponibles (Jinja2)

Tu plantilla HTML debe ser un archivo `.html` válido que use la sintaxis de Jinja2 `{{ variable }}`.

### Datos Personales
*   `{{ foto_url }}`: URL de la foto (base64). Usar en `<img>`.
*   `{{ nombre }}`: Nombre completo.
*   `{{ titulo }}`: Título profesional.
*   `{{ email }}`: Correo electrónico (puede contener HTML seguro).
*   `{{ telefono }}`: Número de teléfono.
*   `{{ linkedin }}`: URL o usuario de LinkedIn.
*   `{{ perfil }}`: Texto del perfil profesional.

### Listas y Estructuras
*   **Experiencia Laboral** (`experiencia_laboral`): Lista de objetos.
    ```html
    {% for exp in experiencia_laboral %}
        {{ exp.cargo }}
        {{ exp.empresa }}
        {{ exp.fecha }}
        {{ exp.descripcion }}
    {% endfor %}
    ```
*   **Educación**:
    *   `{{ carrera }}`
    *   `{{ universidad }}`
    *   `{{ fecha_edu }}`
*   **Certificaciones** (`certificaciones`): Lista de objetos.
    ```html
    {% for cert in certificaciones %}
        {{ cert.nombre }}
        {{ cert.entidad }}
        {{ cert.duracion }}
        {{ cert.folio }} (Opcional)
    {% endfor %}
    ```
*   **Habilidades** (`skills_input`): Lista de strings.
    ```html
    {% for skill in skills_input %}
        {{ skill }}
    {% endfor %}
    ```
*   **Idiomas**:
    *   `{{ nivel_ingles }}`: Nivel de inglés (ej. "B2", "C1").

## Ejemplo de Estructura Base

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        table { border-collapse: collapse; width: 100%; }
        td { vertical-align: top; }
    </style>
</head>
<body>
    <table width="100%">
        <tr>
            <td width="30%" bgcolor="#f0f0f0">
                <!-- Sidebar -->
                <h1>{{ nombre }}</h1>
            </td>
            <td width="70%">
                <!-- Contenido Principal -->
                <h2>Experiencia</h2>
                {% for exp in experiencia_laboral %}
                    <p><strong>{{ exp.cargo }}</strong></p>
                {% endfor %}
            </td>
        </tr>
    </table>
</body>
</html>
```

## Instalación de Nuevas Plantillas

Simplemente coloca el archivo `.html` en la carpeta `templates/`. El sistema lo detectará automáticamente y usará el nombre del archivo (sin extensión) como nombre de la plantilla en el menú.
