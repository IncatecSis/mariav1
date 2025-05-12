document.addEventListener('DOMContentLoaded', function () {
    // Referencias a elementos del DOM
    const chatMessages = document.getElementById('chatMessages');
    const formMensaje = document.getElementById('formMensaje');
    const mensajeContenido = document.getElementById('mensajeContenido');
    const adjuntosInput = document.getElementById('adjuntos');
    const attachmentsPreview = document.getElementById('attachmentsPreview');
    const attachmentsList = document.getElementById('attachmentsList');
    const replyPreview = document.getElementById('replyPreview');
    const replyPreviewText = document.getElementById('replyPreviewText');
    const respuestaAInput = document.getElementById('respuestaA');
    const buscarConversacion = document.getElementById('buscarConversacion');
    const btnInfo = document.getElementById('btnInfo');
    const infoPanel = document.getElementById('infoPanel');
    const btnCloseInfo = document.querySelector('.btn-close');
    const loadMoreBtn = document.querySelector('.btn-load-more');
    const conversationsList = document.querySelector('.list-group');
    const btnAddParticipantes = document.getElementById('btnAddParticipantes');
    const btnCrearConversacion = document.getElementById('btnCrearConversacion');
    const btnAgregarParticipantes = document.getElementById('btnAgregarParticipantes');
    const tipoConversacion = document.getElementById('tipoConversacion');
    const grupoTitulo = document.getElementById('grupoTitulo');

    // ID del usuario actual
    const currentUserId = document.querySelector('[data-current-user]')?.dataset.currentUser;

    // Mostrar/ocultar campo de título según tipo de conversación
    if (tipoConversacion) {
        tipoConversacion.addEventListener('change', function () {
            if (this.value === 'individual') {
                grupoTitulo.classList.add('d-none');
            } else {
                grupoTitulo.classList.remove('d-none');
            }
        });
    }

    // Función para desplazarse al final del chat
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Desplazarse al fondo al cargar la página
    scrollToBottom();

    // Búsqueda de conversaciones
    if (buscarConversacion) {
        buscarConversacion.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const conversations = document.querySelectorAll('.list-group-item');
            
            conversations.forEach(function (conversation) {
                const title = conversation.querySelector('.fw-bold').textContent.toLowerCase();
                const lastMessage = conversation.querySelector('.text-muted').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || lastMessage.includes(searchTerm)) {
                    conversation.style.display = 'flex';
                } else {
                    conversation.style.display = 'none';
                }
            });
        });
    }

    // Mostrar/ocultar panel de información (usando Offcanvas de Bootstrap 5)
    if (btnInfo) {
        btnInfo.addEventListener('click', function () {
            const offcanvas = new bootstrap.Offcanvas(document.getElementById('infoPanel'));
            offcanvas.show();
        });
    }

    // Cargar mensajes anteriores
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function () {
            const page = this.dataset.page;
            const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
            
            fetch(`/incatec/chat/cargar-mensajes-anteriores/?conversacion=${conversacionId}&page=${page}`)
                .then(response => response.json())
                .then(data => {
                    if (data.mensajes && data.mensajes.length > 0) {
                        // Insertar mensajes al inicio
                        const mensajesHTML = data.mensajes.map(mensaje => {
                            // Generar HTML compatible con Bootstrap
                            return `
                                <div class="mb-3 ${mensaje.remitente.id === currentUserId ? 'text-end' : ''}" 
                                     data-id="${mensaje.id_mensaje}">
                                    <div class="${mensaje.remitente.id !== currentUserId ? 'text-start mb-1' : 'd-none'}">
                                        <small class="text-muted">
                                            ${mensaje.remitente.nombre}
                                        </small>
                                    </div>
                                    <div class="d-inline-block position-relative ${mensaje.remitente.id === currentUserId ? 'bg-primary text-white' : 'bg-light'} rounded p-2" style="max-width: 75%;">
                                        <div>
                                            ${mensaje.contenido}
                                        </div>
                                        <div class="d-flex align-items-center justify-content-end gap-1 mt-1">
                                            <small class="text-${mensaje.remitente.id === currentUserId ? 'light' : 'muted'}">
                                                ${mensaje.fecha}
                                            </small>
                                            ${mensaje.editado ? `<small class="text-${mensaje.remitente.id === currentUserId ? 'light' : 'muted'}">editado</small>` : ''}
                                        </div>
                                    </div>
                                </div>
                            `;
                        }).join('');
                        
                        // Insertar antes del primer mensaje
                        const primerMensaje = chatMessages.querySelector('.mb-3');
                        if (primerMensaje) {
                            primerMensaje.insertAdjacentHTML('beforebegin', mensajesHTML);
                        } else {
                            chatMessages.innerHTML = mensajesHTML;
                        }
                        
                        // Actualizar botón para cargar más
                        if (data.hay_mas) {
                            loadMoreBtn.dataset.page = data.pagina_anterior;
                        } else {
                            loadMoreBtn.closest('.text-center').remove();
                        }
                    }
                })
                .catch(error => {
                    console.error('Error cargando mensajes:', error);
                });
        });
    }

    // Cambiar entre conversaciones
    if (conversationsList) {
        conversationsList.addEventListener('click', function (e) {
            const conversationItem = e.target.closest('.list-group-item');
            if (conversationItem) {
                const conversacionId = conversationItem.dataset.id;
                window.location.href = `/incatec/chat/?conversacion=${conversacionId}`;
            }
        });
    }

    // Previsualización de archivos adjuntos
    if (adjuntosInput) {
        adjuntosInput.addEventListener('change', function () {
            attachmentsList.innerHTML = '';
            
            if (this.files.length > 0) {
                attachmentsPreview.classList.remove('d-none');
                
                Array.from(this.files).forEach(file => {
                    const fileType = file.type.split('/')[0];
                    const fileSize = file.size;
                    
                    if (fileType === 'image') {
                        const reader = new FileReader();
                        reader.onload = function (e) {
                            const previewHTML = `
                                <div class="card me-2 mb-2" style="width: 120px;">
                                    <img src="${e.target.result}" class="card-img-top" alt="${file.name}">
                                    <div class="card-body p-2">
                                        <p class="card-text small text-truncate">${file.name}</p>
                                        <p class="card-text small text-muted">${formatFileSize(fileSize)}</p>
                                        <button type="button" class="btn btn-sm btn-outline-danger btn-remove-attachment">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                            `;
                            
                            attachmentsList.insertAdjacentHTML('beforeend', previewHTML);
                            addRemoveListeners();
                        };
                        reader.readAsDataURL(file);
                    } else {
                        let iconClass = 'fas fa-file';
                        
                        switch (fileType) {
                            case 'audio':
                                iconClass = 'fas fa-music';
                                break;
                            case 'video':
                                iconClass = 'fas fa-video';
                                break;
                            case 'application':
                                if (file.type.includes('pdf')) {
                                    iconClass = 'fas fa-file-pdf';
                                } else if (file.type.includes('word') || file.type.includes('document')) {
                                    iconClass = 'fas fa-file-word';
                                } else if (file.type.includes('excel') || file.type.includes('spreadsheet')) {
                                    iconClass = 'fas fa-file-excel';
                                }
                                break;
                        }
                        
                        const previewHTML = `
                            <div class="card me-2 mb-2" style="width: 120px;">
                                <div class="card-body text-center p-2">
                                    <i class="${iconClass} fa-2x mb-2"></i>
                                    <p class="card-text small text-truncate">${file.name}</p>
                                    <p class="card-text small text-muted">${formatFileSize(fileSize)}</p>
                                    <button type="button" class="btn btn-sm btn-outline-danger btn-remove-attachment">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                        `;
                        
                        attachmentsList.insertAdjacentHTML('beforeend', previewHTML);
                        addRemoveListeners();
                    }
                });
            } else {
                attachmentsPreview.classList.add('d-none');
            }
        });
    }
    
    // Añadir listeners para eliminar adjuntos
    function addRemoveListeners() {
        document.querySelectorAll('.btn-remove-attachment').forEach((btn) => {
            btn.addEventListener('click', function () {
                this.closest('.card').remove();
                
                // Si no quedan adjuntos, ocultar la previsualización
                if (attachmentsList.children.length === 0) {
                    attachmentsPreview.classList.add('d-none');
                }
            });
        });
    }
    
    // Formatear tamaño de archivo
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Responder a mensajes
    document.querySelectorAll('[data-id]').forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (e.target.closest('.dropdown-item') && e.target.closest('.dropdown-item').classList.contains('btn-reply')) {
                e.preventDefault();
                
                const messageId = this.dataset.id;
                const messageContent = this.querySelector('.message-content').textContent.trim();
                
                respuestaAInput.value = messageId;
                replyPreviewText.textContent = messageContent;
                replyPreview.classList.remove('d-none');
                
                // Enfocar el textarea
                mensajeContenido.focus();
            }
        });
    });
    
    // Cerrar previsualización de respuesta
    if (document.querySelector('.btn-close')) {
        document.querySelector('.btn-close').addEventListener('click', function () {
            if (this.closest('#replyPreview')) {
                replyPreview.classList.add('d-none');
                respuestaAInput.value = '';
            }
        });
    }

    // Enviar mensaje
    if (formMensaje) {
        formMensaje.addEventListener('submit', function (e) {
            e.preventDefault();
            
            // Validación básica
            if (mensajeContenido.value.trim() === '' && adjuntosInput.files.length === 0) {
                return;
            }
            
            // Crear FormData para enviar datos y archivos
            const formData = new FormData(this);
            
            fetch('/incatec/enviar_mensaje/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.id) {
                        mensajeContenido.value = '';
                        adjuntosInput.value = '';
                        respuestaAInput.value = '';
                        replyPreview.classList.add('d-none');
                        attachmentsPreview.classList.add('d-none');
                        attachmentsList.innerHTML = '';
            
                        // Insertar el mensaje en el DOM con formato Bootstrap
                        const nuevoMensajeHTML = `
                        <div class="mb-3 text-end" data-id="${data.id}">
                            <div class="d-inline-block position-relative bg-primary text-white rounded p-2" style="max-width: 75%;">
                                <div>
                                    ${data.contenido}
                                </div>
                                <div class="d-flex align-items-center justify-content-end gap-1 mt-1">
                                    <small class="text-light">
                                        ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </small>
                                    <small class="text-light">
                                        <i class="fas fa-check"></i>
                                    </small>
                                </div>
                                
                                <!-- Dropdown de acciones -->
                                <div class="dropdown position-absolute top-0 end-0">
                                    <button class="btn btn-sm text-light dropdown-toggle" 
                                        type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                        <i class="fas fa-ellipsis-v"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-end">
                                        <li>
                                            <a href="#" class="dropdown-item" data-id="${data.id}">
                                                <i class="fas fa-reply me-2"></i> Responder
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" class="dropdown-item">
                                                <i class="fas fa-edit me-2"></i> Editar
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" class="dropdown-item text-danger">
                                                <i class="fas fa-trash me-2"></i> Eliminar
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    `;
                    
                        chatMessages.insertAdjacentHTML('beforeend', nuevoMensajeHTML);
                        scrollToBottom();
                        
                    } else {
                        alert('Error al enviar el mensaje: ' + (data.error || 'Error desconocido'));
                    }
                })
                .catch(error => {
                    console.error('Error al enviar el mensaje:', error);
                });
        });
    }

    // Crear nueva conversación
    if (btnCrearConversacion) {
        btnCrearConversacion.addEventListener('click', function (event) {
            event.preventDefault();

            const tipo = document.getElementById('tipoConversacion').value;
            let titulo = '';

            if (tipo !== 'individual') {
                titulo = document.getElementById('tituloConversacion').value.trim();
                if (titulo === '') {
                    alert('Debes ingresar un título para la conversación grupal');
                    return;
                }
            }

            const participantes = Array.from(document.getElementById('participantesSelect').selectedOptions).map(option => option.value);

            if (participantes.length === 0) {
                alert('Debes seleccionar al menos un participante');
                return;
            }

            fetch('/incatec/crear_chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    tipo: tipo,
                    titulo: titulo,
                    participantes: participantes
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    } else if (data.error) {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error creando conversación:', error);
                    alert('Error al crear la conversación. Inténtalo de nuevo.');
                });
        });
    }
    
    // Añadir participantes a conversación existente
    if (btnAddParticipantes) {
        btnAddParticipantes.addEventListener('click', function (e) {
            e.preventDefault();
            // Usar Bootstrap 5 Modal
            const modal = new bootstrap.Modal(document.getElementById('agregarParticipantesModal'));
            modal.show();
        });
    }
    
    if (btnAgregarParticipantes) {
        btnAgregarParticipantes.addEventListener('click', function () {
            const nuevosParticipantes = Array.from(document.getElementById('nuevosParticipantesSelect').selectedOptions).map(option => option.value);
            
            if (nuevosParticipantes.length === 0) {
                alert('Debes seleccionar al menos un participante');
                return;
            }
            
            const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
            
            fetch('/incatec/agregar_participantes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    conversacion: conversacionId,
                    participantes: nuevosParticipantes
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Cerrar modal con Bootstrap 5
                        const modalEl = document.getElementById('agregarParticipantesModal');
                        const modal = bootstrap.Modal.getInstance(modalEl);
                        modal.hide();
                    
                        // Refrescar la página para ver los cambios
                        location.reload();
                    } else if (data.error) {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error añadiendo participantes:', error);
                    alert('Error al añadir participantes. Inténtalo de nuevo.');
                });
        });
    }
    
    // Silenciar notificaciones
    const btnSilenciar = document.getElementById('btnSilenciar');
    if (btnSilenciar) {
        btnSilenciar.addEventListener('click', function (e) {
            e.preventDefault();
            
            const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
            
            fetch('/incatec/chat/silenciar-notificaciones/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    conversacion: conversacionId
                })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.silenciado ? 'Notificaciones silenciadas' : 'Notificaciones activadas');
                })
                .catch(error => {
                    console.error('Error al cambiar estado de notificaciones:', error);
                });
        });
    }
    
    // Salir de conversación (sin restricciones)
    const btnSalir = document.getElementById('btnSalir');
    if (btnSalir) {
        btnSalir.addEventListener('click', function (e) {
            e.preventDefault();
            
            // Crear un modal de confirmación Bootstrap
            const modalHTML = `
                <div class="modal fade" id="confirmModal" tabindex="-1" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Confirmar acción</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>¿Estás seguro de que quieres salir de esta conversación?</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-danger" id="btnConfirmSalir">Salir</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Añadir el modal al DOM
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            // Inicializar y mostrar el modal
            const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
            confirmModal.show();
            
            // Manejar el clic en el botón de confirmación
            document.getElementById('btnConfirmSalir').addEventListener('click', function () {
                const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
                
                fetch('/incatec/salir_conversacion/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({
                        conversacion: conversacionId
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        confirmModal.hide();
                    
                        // Eliminar el modal después de ocultarlo
                        document.getElementById('confirmModal').addEventListener('hidden.bs.modal', function () {
                            this.remove();
                        });
                    
                        if (data.success) {
                            if (data.eliminada) {
                                // Si la conversación fue eliminada, mostrar mensaje
                                mostrarToast('Conversación eliminada', 'La conversación ha sido eliminada.', 'success');
                            } else {
                                mostrarToast('Acción completada', 'Has salido de la conversación exitosamente.', 'success');
                            }
                        
                            // Redireccionar a la lista de conversaciones
                            setTimeout(function () {
                                window.location.href = '/incatec/chat/';
                            }, 1000);
                        } else if (data.error) {
                            mostrarToast('Error', data.error, 'danger');
                        }
                    })
                    .catch(error => {
                        confirmModal.hide();
                        console.error('Error al salir de la conversación:', error);
                        mostrarToast('Error', 'Error al procesar la solicitud. Inténtalo de nuevo.', 'danger');
                    });
            });
        });
    }

    // Eliminar conversación (solo para administradores)
    const btnEliminarConversacion = document.getElementById('btnEliminarConversacion');
    if (btnEliminarConversacion) {
        btnEliminarConversacion.addEventListener('click', function (e) {
            e.preventDefault();
            
            // Crear un modal de confirmación Bootstrap
            const modalHTML = `
                <div class="modal fade" id="confirmEliminarModal" tabindex="-1" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Confirmar eliminación</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>¿Estás seguro de que quieres eliminar esta conversación?</p>
                                <p class="text-danger"><small>Esta acción no se puede deshacer y eliminará la conversación para todos los participantes.</small></p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-danger" id="btnConfirmEliminar">Eliminar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Añadir el modal al DOM
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            // Inicializar y mostrar el modal
            const confirmModal = new bootstrap.Modal(document.getElementById('confirmEliminarModal'));
            confirmModal.show();
            
            // Manejar el clic en el botón de confirmación
            document.getElementById('btnConfirmEliminar').addEventListener('click', function () {
                const conversacionId = new URLSearchParams(window.location.search).get('conversacion');
                
                fetch('/incatec/eliminar_conversacion/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({
                        conversacion: conversacionId
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        confirmModal.hide();
                    
                        // Eliminar el modal después de ocultarlo
                        document.getElementById('confirmEliminarModal').addEventListener('hidden.bs.modal', function () {
                            this.remove();
                        });
                    
                        if (data.success) {
                            mostrarToast('Conversación eliminada', 'La conversación ha sido eliminada exitosamente.', 'success');
                        
                            // Redireccionar a la lista de conversaciones
                            setTimeout(function () {
                                window.location.href = '/incatec/chat/';
                            }, 1000);
                        } else if (data.error) {
                            mostrarToast('Error', data.error, 'danger');
                        }
                    })
                    .catch(error => {
                        confirmModal.hide();
                        console.error('Error al eliminar la conversación:', error);
                        mostrarToast('Error', 'Error al procesar la solicitud. Inténtalo de nuevo.', 'danger');
                    });
            });
        });
    }
    // Función para mostrar Toast de Bootstrap
    function mostrarToast(titulo, mensaje, tipo) {
        // Crear el toast
        const toastHTML = `
            <div class="toast-container position-fixed bottom-0 end-0 p-3">
                <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header bg-${tipo} text-white">
                        <strong class="me-auto">${titulo}</strong>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                        ${mensaje}
                    </div>
                </div>
            </div>
        `;
        
        // Añadir el toast al DOM
        document.body.insertAdjacentHTML('beforeend', toastHTML);
        
        // Inicializar y mostrar el toast
        const toastEl = document.querySelector('.toast:last-child');
        const toast = new bootstrap.Toast(toastEl, {
            delay: 5000
        });
        toast.show();
        
        // Eliminar el toast del DOM después de ocultarse
        toastEl.addEventListener('hidden.bs.toast', function() {
            this.closest('.toast-container').remove();
        });
    }
    
    // Obtener token CSRF de las cookies
    function getCsrfToken() {
        const name = 'csrftoken';
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return '';
    }

    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Llamar a la función para añadir el botón eliminar si el usuario es administrador
    if (document.querySelector('.participant-role')) {
        agregarBotonEliminar();
    }
});