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

        input.addEventListener('keydown', function (e) {
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

                // EXCEPCIÓN: Si es el campo "Folio" del formulario de certificaciones,
                // queremos que el Enter envíe el formulario (comportamiento default de Streamlit).
                if (input.getAttribute("aria-label") === "Folio o ID (Opcional)") {
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

// Función para poner foco por label (se puede llamar inyectando un script que la use)
function focusInputByLabel(labelText) {
    setTimeout(function () {
        const doc = window.parent.document;
        const input = doc.querySelector(`input[aria-label="${labelText}"]`);
        if (input) {
            input.focus();
        }
    }, 100);
}
