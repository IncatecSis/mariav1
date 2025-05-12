// Variables para polling
let pollingInterval = null;
const POLLING_TIME = 3000; // 3 segundos

// Función para iniciar el polling cuando estamos en una conversación
function iniciarPolling() {
    // Verificar si estamos en una conversación
    const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
    if (!conversacionId || !document.getElementById('chatMessages')) return;
    
    console.log('Iniciando polling para conversación:', conversacionId);
    
    // Obtener el ID del usuario actual desde el atributo data-current-user
    const currentUserElement = document.querySelector('[data-current-user]');
    const currentUserId = currentUserElement ? currentUserElement.dataset.currentUser : null;
    
    if (!currentUserId) {
        console.error('No se pudo determinar el ID del usuario actual');
        return;
    }
    
    // Si ya hay un intervalo activo, limpiarlo
    if (pollingInterval) clearInterval(pollingInterval);
    
    // Determinar el ID del último mensaje que tenemos
    let ultimoMensajeId = obtenerIdUltimoMensaje();
    
    // Iniciar el intervalo de polling
    pollingInterval = setInterval(() => {
        actualizarMensajes(conversacionId, ultimoMensajeId, currentUserId);
    }, POLLING_TIME);
}

// Función para obtener el ID del último mensaje en el chat
function obtenerIdUltimoMensaje() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages || chatMessages.children.length === 0) return 0;
    
    const mensajes = Array.from(chatMessages.querySelectorAll('[data-id]'));
    if (mensajes.length > 0) {
        const ultimoMensaje = mensajes[mensajes.length - 1];
        return parseInt(ultimoMensaje.dataset.id) || 0;
    }
    
    return 0;
}

// Función para desplazarse al final del chat
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Función para actualizar mensajes
function actualizarMensajes(conversacionId, ultimoMensajeId, currentUserId) {
    fetch(`/incatec/nuevos_mensajes/?conversacion=${conversacionId}&ultimo_id=${ultimoMensajeId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            if (data.nuevos_mensajes && data.nuevos_mensajes.length > 0) {
                // Mostrar los nuevos mensajes
                mostrarNuevosMensajes(data.nuevos_mensajes, currentUserId);
                
                // Actualizar el ID del último mensaje para la próxima consulta
                const nuevoUltimoMensaje = data.nuevos_mensajes[data.nuevos_mensajes.length - 1];
                ultimoMensajeId = nuevoUltimoMensaje.id;
                
                // Hacer scroll al último mensaje si el usuario estaba al final del chat
                const chatMessages = document.getElementById('chatMessages');
                const estaEnElFondo = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < 100;
                if (estaEnElFondo) {
                    scrollToBottom();
                }
            }
        })
        .catch(error => {
            console.error('Error al actualizar mensajes:', error);
        });
}

// Función para mostrar nuevos mensajes
function mostrarNuevosMensajes(mensajes, currentUserId) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    mensajes.forEach(mensaje => {
        // Verificar si el mensaje ya existe
        if (document.querySelector(`[data-id="${mensaje.id}"]`)) return;
        
        // Solo procesar mensajes de otros usuarios (los propios ya se muestran al enviarlos)
        if (mensaje.remitente.id == currentUserId) return;
        
        // Crear el HTML del mensaje siguiendo el mismo formato que tienes en tu código principal
        const nuevoMensajeHTML = `
            <div class="mb-3" data-id="${mensaje.id}">
                <div class="text-start mb-1">
                    <small class="text-muted">
                        ${mensaje.remitente.nombre}
                    </small>
                </div>
                <div class="d-inline-block position-relative bg-light rounded p-2" style="max-width: 75%;">
                    <div class="message-content">
                        ${mensaje.contenido}
                    </div>
                    <div class="d-flex align-items-center justify-content-end gap-1 mt-1">
                        <small class="text-muted">
                            ${mensaje.fecha}
                        </small>
                        ${mensaje.editado ? '<small class="text-muted">editado</small>' : ''}
                    </div>
                    
                    <!-- Dropdown de acciones -->
                    <div class="dropdown position-absolute top-0 end-0">
                        <button class="btn btn-sm text-muted dropdown-toggle" 
                            type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a href="#" class="dropdown-item btn-reply">
                                    <i class="fas fa-reply me-2"></i> Responder
                                </a>
                            </li>
                            <li>
                                <a href="#" class="dropdown-item">
                                    <i class="fas fa-smile me-2"></i> Reaccionar
                                </a>
                            </li>
                            <li>
                                <a href="#" class="dropdown-item">
                                    <i class="far fa-bookmark me-2"></i> Guardar mensaje
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.insertAdjacentHTML('beforeend', nuevoMensajeHTML);
        
        // Agregar eventos a los nuevos mensajes
        const nuevoMensajeElement = chatMessages.lastElementChild;
        
        // Agregar eventos para responder a mensajes
        const btnReply = nuevoMensajeElement.querySelector('.btn-reply');
        if (btnReply) {
            btnReply.addEventListener('click', function(e) {
                e.preventDefault();
                
                const messageId = nuevoMensajeElement.dataset.id;
                const messageContent = nuevoMensajeElement.querySelector('.message-content').textContent.trim();
                
                const respuestaAInput = document.getElementById('respuestaA');
                const replyPreviewText = document.getElementById('replyPreviewText');
                const replyPreview = document.getElementById('replyPreview');
                const mensajeContenido = document.getElementById('mensajeContenido');
                
                if (respuestaAInput && replyPreviewText && replyPreview && mensajeContenido) {
                    respuestaAInput.value = messageId;
                    replyPreviewText.textContent = messageContent;
                    replyPreview.classList.remove('d-none');
                    
                    // Enfocar el textarea
                    mensajeContenido.focus();
                }
            });
        }
    });
}

// Iniciar el polling al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar polling con un pequeño retraso para asegurar que todo esté cargado
    setTimeout(iniciarPolling, 1000);
    
    // Detener el polling si el usuario cambia de página
    window.addEventListener('beforeunload', function() {
        if (pollingInterval) clearInterval(pollingInterval);
    });
});