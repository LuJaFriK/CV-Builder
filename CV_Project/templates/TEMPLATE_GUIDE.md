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

### 3. Diseño de Página Completa (Full Page Layout)
Para evitar que el documento se vea "cortado" o con espacios en blanco extraños al final de la hoja en el PDF, y para asegurar que se vea bien en pantalla:

*   **HTML/Body**: Asegúrate de establecer `height: 100%` en `html` y `body`.
*   **Contenedor Principal**:
    *   Debes envolver todo tu contenido (incluyendo la tabla principal) en un `div` con clase `.cv-container`.
    *   Estilos requeridos para `.cv-container`:
        ```css
        .cv-container {
            width: 100%;
            max-width: 900px; /* O 850px. Importante para que no se vea "estirado" en monitores anchos */
            margin: 0 auto;   /* Para centrarlo */
            
            /* TRUCO: Gradiente Robusto (Compatible con wkhtmltopdf antiguo) */
            background-color: white;
            /* Old WebKit (Safari 4+, Chrome 1-9) - CRÍTICO para wkhtmltopdf */
            background: -webkit-gradient(linear, left top, right top, color-stop(30%, #eaebef), color-stop(30%, #ffffff));
            /* Newer WebKit */
            background: -webkit-linear-gradient(left, #eaebef 30%, #ffffff 30%);
            /* Standard */
            background: linear-gradient(to right, #eaebef 30%, #ffffff 30%);
            
            min-height: 100vh; 
        }
        
        /* Asegúrate de que las celdas de la tabla NO tengan background-color para que se vea el gradiente */
        .sidebar-cell, .main-cell {
            background: transparent;
        }

        /* TRUCO: Tablas Anidadas Transparentes */
        /* Si anidas tablas (ej. para experiencia laboral), asegúrate de que no tengan fondo */
        .job-header-table, .job-title {
            background: transparent;
        }
        ```
    *   **Evita `opacity` en textos**: Puede causar que `wkhtmltopdf` rasterice el texto.
    *   **Excepción para PDF (@media print)**:
        *   **CRÍTICO**: Usa `@page { margin: 0cm; }` para eliminar márgenes de impresora.
        *   Aplica el gradiente al `body` para asegurar que cubra toda la hoja ("hasta el suelo").
        *   Haz el contenedor transparente.
        ```css
        @media print {
            @page { margin: 0cm; }
            html, body { 
                height: 100%;
                margin: 0;
                padding: 0;
                /* Gradiente en el body para cubrir toda la página */
                background: -webkit-gradient(linear, left top, right top, color-stop(30%, #eaebef), color-stop(30%, #ffffff)) !important;
                background: -webkit-linear-gradient(left, #eaebef 30%, #ffffff 30%) !important;
            }
            .cv-container {
                min-height: 29.7cm;
                background: transparent !important;
                width: 100%;
                max-width: none;
            }
        }
        ```

### 4. CSS
*   Puedes usar CSS moderno para estilos de texto (colores, tamaños, negritas), padding y margin dentro de los bloques.
*   Evita `gap`, `transform`, o animaciones complejas.

## Variables Disponibles (Jinja2)

Tu plantilla HTML debe ser un archivo `.html` válido que use la sintaxis de Jinja2 `{{ variable }}`.

### Datos Personales
*   `{{ foto_url }}`: URL de la foto (base64). Usar en `<img>`.
    *   **Importante**: Si no hay foto, esta variable estará vacía. Debes usar `{% if foto_url %}` para envolver la etiqueta `<img>` y **NO** mostrar ningún placeholder o círculo vacío si el usuario no subió foto.
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
