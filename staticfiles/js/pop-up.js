// JavaScript Document

// Obtén el pop-up
var popup = document.getElementById("popup");

// Obtén el botón que abre el pop-up
var openPopupBtns = document.querySelectorAll(".openPopupBtn");

// Obtén el botón que cierra el pop-up
var closePopupBtn = document.getElementById("closePopupBtn");

// Cuando el usuario hace clic en el botón, muestra el pop-up
openPopupBtns.forEach(function(btn) {
    btn.onclick = function() {
        popup.style.display = "block";
    }
});

// Cuando el usuario hace clic en el botón de cerrar, oculta el pop-up
closePopupBtn.onclick = function() {
    popup.style.display = "none";
}

// Cuando el usuario hace clic fuera del contenido del pop-up, lo oculta
window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
}

    document.addEventListener("DOMContentLoaded", function() {
        // Obtener la fecha actual
        var today = new Date().toISOString().split('T')[0];
        // Asignar la fecha actual al campo de texto
        document.getElementById('fechaPago').value = today;
    });

    // Función para alternar la visibilidad del historial de pagos
    document.getElementById('toggleHistorialBtn').addEventListener('click', function () {
        var historialPagos = document.getElementById('historialPagos');
        if (historialPagos.style.display === 'none') {
            historialPagos.style.display = 'block';
        } else {
            historialPagos.style.display = 'none';
        }
    });

document.addEventListener('DOMContentLoaded', function () {
    // Función para alternar la visibilidad del historial de notas débito
    document.getElementById('toggleHistorialDebitoBtn').addEventListener('click', function () {
        var historialNotasDebito = document.getElementById('historialNotasDebito');
        if (historialNotasDebito.style.display === 'none') {
            historialNotasDebito.style.display = 'block';
        } else {
            historialNotasDebito.style.display = 'none';
        }
    });
});

// Función para iniciar el temporizador en el pop-up
function startPopupTimer(timeRemaining) {
    var countdownElement = document.getElementById("countdown");

    // Guardar el tiempo restante en localStorage
    localStorage.setItem('retry_after', timeRemaining);

    // Mostrar el modal
    popup.style.display = "block";

    // Temporizador de cuenta regresiva
    var interval = setInterval(function() {
        timeRemaining--;
        countdownElement.textContent = timeRemaining;

        // Actualizar localStorage con el tiempo restante
        localStorage.setItem('retry_after', timeRemaining);

        if (timeRemaining <= 0) {
            clearInterval(interval);
            popup.style.display = "none";  // Ocultar el modal
            localStorage.removeItem('retry_after');  // Limpiar el localStorage al terminar el temporizador
        }
    }, 1000);
}

// Verificar si existe un temporizador en localStorage al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    var storedTimeRemaining = localStorage.getItem('retry_after');

    if (storedTimeRemaining !== null && storedTimeRemaining > 0) {
        startPopupTimer(storedTimeRemaining);
    }
});

