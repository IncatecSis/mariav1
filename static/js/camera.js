/**
 * Funcionalidad de cámara para tomar fotos de usuario directamente en el formulario
 */
document.addEventListener('DOMContentLoaded', function() {
    // Buscar el campo de foto del usuario en el nuevo formulario
    const camposFoto = document.querySelectorAll('input[name="foto_perfil"]');
    
    // Recorrer cada campo encontrado 
    camposFoto.forEach(inputFoto => {
        // Solo aplicar la funcionalidad si es el campo en el formulario de usuario
        const contenedorPadre = inputFoto.parentElement;
        
        // 1. Crear el HTML para la interfaz de cámara
        const contenidoCamara = `
            <div class="mt-3 camara-interface" style="display: none;">
                <div class="card">
                    <div class="card-body">
                        <div class="ratio ratio-16x9 mb-2 bg-light rounded">
                            <video id="video-preview" class="rounded"></video>
                        </div>
                        <div class="d-none mb-2">
                            <canvas id="canvas-capture" class="w-100 rounded"></canvas>
                        </div>
                        <div class="d-flex flex-wrap gap-2">
                            <button type="button" class="btn btn-soft-primary btn-abrir-camara">
                                <i class="bi bi-camera"></i> Abrir Cámara
                            </button>
                            <button type="button" class="btn btn-soft-danger btn-capturar d-none">
                                <i class="bi bi-camera"></i> Capturar
                            </button>
                            <button type="button" class="btn btn-soft-secondary btn-cancelar d-none">
                                <i class="bi bi-x"></i> Cancelar
                            </button>
                            <button type="button" class="btn btn-soft-success btn-aceptar d-none">
                                <i class="bi bi-check"></i> Usar Foto
                            </button>
                            <button type="button" class="btn btn-soft-warning btn-rechazar d-none">
                                <i class="bi bi-arrow-repeat"></i> Otra Foto
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // 2. Crear botón para tomar foto
        const btnTomarFoto = document.createElement('button');
        btnTomarFoto.type = 'button';
        btnTomarFoto.className = 'btn btn-soft-primary ms-2';
        btnTomarFoto.innerHTML = '<i class="bi bi-camera"></i> Tomar Foto';
        
        // 3. Crear contenedor para el input y el botón
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';
        
        // 4. Mover elementos actuales al nuevo grupo
        const originalContainer = inputFoto.parentElement;
        
        // Mantener una referencia a la etiqueta (si existe)
        const label = originalContainer.querySelector('label');
        
        // Reorganizar los elementos
        // Insertar el grupo de entrada después de la etiqueta
        if (label) {
            originalContainer.insertBefore(inputGroup, label.nextSibling);
        } else {
            originalContainer.prepend(inputGroup);
        }
        
        // Mover el input al grupo
        inputFoto.parentNode.removeChild(inputFoto);
        inputGroup.appendChild(inputFoto);
        
        // Agregar el botón al grupo
        inputGroup.appendChild(btnTomarFoto);
        
        // 6. Agregar la interfaz de cámara
        const camaraDiv = document.createElement('div');
        camaraDiv.innerHTML = contenidoCamara;
        originalContainer.appendChild(camaraDiv.firstElementChild);
        
        // 7. Obtener referencias a los elementos de la interfaz
        const camaraInterface = originalContainer.querySelector('.camara-interface');
        const videoElement = originalContainer.querySelector('#video-preview');
        const canvasElement = originalContainer.querySelector('#canvas-capture');
        const btnAbrirCamara = originalContainer.querySelector('.btn-abrir-camara');
        const btnCapturar = originalContainer.querySelector('.btn-capturar');
        const btnCancelar = originalContainer.querySelector('.btn-cancelar');
        const btnAceptar = originalContainer.querySelector('.btn-aceptar');
        const btnRechazar = originalContainer.querySelector('.btn-rechazar');
        
        // Variable para almacenar la transmisión de cámara
        let streamCamara = null;
        
        // 8. Configurar eventos
        // Mostrar interfaz al hacer clic en "Tomar Foto"
        btnTomarFoto.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir comportamiento por defecto del botón
            camaraInterface.style.display = 'block';
        });
        
        // Iniciar cámara
        btnAbrirCamara.addEventListener('click', async function() {
            try {
                streamCamara = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        facingMode: 'user'
                    },
                    audio: false
                });
                
                videoElement.srcObject = streamCamara;
                videoElement.play();
                
                // Actualizar botones
                btnAbrirCamara.classList.add('d-none');
                btnCapturar.classList.remove('d-none');
                btnCancelar.classList.remove('d-none');
                
            } catch (error) {
                console.error('Error al acceder a la cámara:', error);
                
                // Mostrar mensaje de error
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error de cámara',
                        text: 'No se pudo acceder a la cámara. Verifique los permisos.',
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000
                    });
                } else {
                    alert('No se pudo acceder a la cámara. Verifique los permisos del navegador.');
                }
            }
        });
        
        // Capturar foto
        btnCapturar.addEventListener('click', function() {
            const context = canvasElement.getContext('2d');
            
            // Establecer dimensiones del canvas
            canvasElement.width = videoElement.videoWidth;
            canvasElement.height = videoElement.videoHeight;
            
            // Dibujar la imagen del video en el canvas
            context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
            
            // Mostrar canvas y ocultar video
            canvasElement.parentElement.classList.remove('d-none');
            videoElement.parentElement.classList.add('d-none');
            
            // Actualizar botones
            btnCapturar.classList.add('d-none');
            btnCancelar.classList.add('d-none');
            btnAceptar.classList.remove('d-none');
            btnRechazar.classList.remove('d-none');
            
            // Detener la transmisión de cámara
            if (streamCamara) {
                streamCamara.getTracks().forEach(track => track.stop());
                streamCamara = null;
            }
        });
        
        // Cancelar proceso
        btnCancelar.addEventListener('click', function() {
            // Detener cámara
            if (streamCamara) {
                streamCamara.getTracks().forEach(track => track.stop());
                streamCamara = null;
            }
            
            // Ocultar interfaz
            camaraInterface.style.display = 'none';
            
            // Restablecer vista
            videoElement.parentElement.classList.remove('d-none');
            canvasElement.parentElement.classList.add('d-none');
            
            // Restablecer botones
            btnCapturar.classList.add('d-none');
            btnCancelar.classList.add('d-none');
            btnAceptar.classList.add('d-none');
            btnRechazar.classList.add('d-none');
            btnAbrirCamara.classList.remove('d-none');
        });
        
        // Rechazar foto
        btnRechazar.addEventListener('click', function() {
            // Volver a modo inicio
            videoElement.parentElement.classList.remove('d-none');
            canvasElement.parentElement.classList.add('d-none');
            
            // Actualizar botones
            btnAceptar.classList.add('d-none');
            btnRechazar.classList.add('d-none');
            btnAbrirCamara.classList.remove('d-none');
        });
        
        // Aceptar foto
        btnAceptar.addEventListener('click', function() {
            // Convertir canvas a archivo
            canvasElement.toBlob(function(blob) {
                // Crear archivo
                const file = new File([blob], 'foto_usuario.jpg', { type: 'image/jpeg' });
                
                // Asignar al input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                inputFoto.files = dataTransfer.files;
                
                // Disparar evento change
                const event = new Event('change', { bubbles: true });
                inputFoto.dispatchEvent(event);
                
                // Ocultar interfaz y restablecer
                camaraInterface.style.display = 'none';
                videoElement.parentElement.classList.remove('d-none');
                canvasElement.parentElement.classList.add('d-none');
                
                // Restablecer botones
                btnAceptar.classList.add('d-none');
                btnRechazar.classList.add('d-none');
                btnAbrirCamara.classList.remove('d-none');
                
                // Mostrar mensaje de éxito
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Foto guardada',
                        text: 'La foto del usuario se ha capturado correctamente',
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000
                    });
                } else {
                    alert('Foto guardada correctamente');
                }
            }, 'image/jpeg', 0.9);
        });
    });
});