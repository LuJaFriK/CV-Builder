import streamlit.components.v1 as components

def inject_focus_js():
    """
    Inyecta JavaScript para manejar la navegación con Enter en los formularios.
    Busca inputs y textareas en el sidebar y mueve el foco al siguiente elemento al presionar Enter.
    """
    js_code = """
    <script>
    const doc = window.parent.document;
    
    // Función para agregar los listeners
    function addEnterNavigation() {
        // Seleccionamos el sidebar
        const sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        // Seleccionamos inputs y textareas dentro del sidebar
        const inputs = Array.from(sidebar.querySelectorAll('input[type="text"], textarea'));
        
        inputs.forEach((input, index) => {
            // Evitamos duplicar listeners
            if (input.dataset.enterNav) return;
            input.dataset.enterNav = "true";

            input.addEventListener('keydown', function(e) {
                // Si es Enter (13) y no es un textarea (o es Ctrl+Enter en textarea)
                if (e.key === 'Enter') {
                    // Permitir saltos de línea normales en textarea si no se usa Ctrl
                    if (input.tagName === 'TEXTAREA' && !e.ctrlKey) {
                        return;
                    }

                    // EXCEPCIÓN: Si el input es para "Nueva Skill", NO interceptamos el Enter.
                    // Streamlit asocia el label con el input mediante aria-label o estructura DOM.
                    // Buscamos si el aria-label contiene "Nueva Skill" o si hay un label cercano.
                    if (input.getAttribute("aria-label") === "Nueva Skill") {
                        return; 
                    }
                    
                    // Intento alternativo de detección si aria-label no es exacto:
                    // Verificamos si el input está dentro de un bloque que parece ser la sección de skills.
                    // Pero aria-label suele ser fiable en Streamlit para st.text_input("Label").

                    e.preventDefault();
                    
                    // Buscar el siguiente input habilitado
                    const nextInput = inputs[index + 1];
                    if (nextInput) {
                        nextInput.focus();
                    }
                }
            });
        });
    }

    // Ejecutar al cargar y observar cambios
    addEnterNavigation();
    
    // Observador para re-aplicar si el DOM cambia (Streamlit re-renderiza mucho)
    const observer = new MutationObserver(() => {
        addEnterNavigation();
    });
    
    observer.observe(doc.body, { childList: true, subtree: true });
    </script>
    """
    components.html(js_code, height=0, width=0)

def focus_input_by_label(label_text):
    """
    Inyecta JS para poner el foco en un input que tenga cierto aria-label.
    Útil para resetear el foco al principio del formulario.
    """
    js_code = f"""
    <script>
    setTimeout(function() {{
        const doc = window.parent.document;
        const input = doc.querySelector('input[aria-label="{label_text}"]');
        if (input) {{
            input.focus();
        }}
    }}, 100); // Pequeño delay para asegurar que el DOM se actualizó
    </script>
    """
    components.html(js_code, height=0, width=0)
