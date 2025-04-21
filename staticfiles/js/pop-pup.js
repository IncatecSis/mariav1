// Función general para mostrar un pop-up
function showPopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = "block";
}

// Función general para cerrar un pop-up
function closePopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = "none";
}

// Detectar botones con atributo 'data-popup' para abrir un pop-up específico
document.querySelectorAll("[data-popup]").forEach(function(btn) {
    btn.addEventListener("click", function() {
        var popupId = btn.getAttribute("data-popup");
        showPopup(popupId);
    });
});

// Función para cerrar el pop-up
document.querySelectorAll("[data-close]").forEach(function(btn) {
    btn.addEventListener("click", function() {
        var popupId = btn.getAttribute("data-close");
        closePopup(popupId);
    });
});

// Cerrar pop-up si haces clic fuera de él
window.addEventListener("click", function(event) {
    if (event.target.classList.contains("popup")) {
        event.target.style.display = "none";
    }
});


// Función para alternar la visibilidad utilizando clases y data-target
function toggleDisplayWithClass() {
    // Seleccionamos todos los botones que tienen la clase "toggleBtn"
    var buttons = document.querySelectorAll('.toggleBtn');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Obtener el valor del atributo data-target del botón
            var targetId = this.getAttribute('data-target');
            var targetElement = document.getElementById(targetId);

            // Alternar la visibilidad del elemento correspondiente
            if (targetElement.style.display === 'none' || targetElement.style.display === '') {
                targetElement.style.display = 'block';
            } else {
                targetElement.style.display = 'none';
            }
        });
    });
}

// Ejecutar la función al cargar la página
document.addEventListener('DOMContentLoaded', toggleDisplayWithClass);
