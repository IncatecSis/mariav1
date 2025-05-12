document.addEventListener('DOMContentLoaded', function () {
    // =========== FUNCIONES DE UTILIDAD ===========
    
    // Función para formatear la fecha en formato ISO
    function formatearFechaISO(fecha) {
        const año = fecha.getFullYear();
        const mes = String(fecha.getMonth() + 1).padStart(2, "0");
        const dia = String(fecha.getDate()).padStart(2, "0");
        return `${año}-${mes}-${dia}`;
    }

    // Función para parsear un string "YYYY-MM-DD" como fecha local
    function parseLocalDateFromString(dateStr) {
        const [year, month, day] = dateStr.split("-").map(Number);
        return new Date(year, month - 1, day);
    }

    // Función para formatear fecha para mostrar
    function formatDate(date) {
        return date.toLocaleDateString("es-ES", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        });
    }

    // Función para formatear hora
    function formatHora(hora) {
        const [h, m] = hora.split(":");
        return `${h}:${m}`;
    }

    // Función para obtener el nombre del día de la semana
    function getDiaSemana(numeroDia) {
        const dias = [
            "Domingo",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
        ];
        return dias[numeroDia];
    }

    // =========== REFERENCIAS A ELEMENTOS DEL DOM ===========
    
    // Elementos principales del formulario
    const selectTipoSalon = document.getElementById('tipo_salon');
    const selectSalon = document.getElementById('salon');
    const inputCapacidad = document.getElementById('capacidad');
    const selectPrograma = document.getElementById('programa');
    const selectModulo = document.getElementById('modulo');
    const inputHorasTotales = document.getElementById('horasTotales');
    const grupoForm = document.getElementById('grupoForm');
    const nombreInput = document.getElementById('nombre');
    const profesorSelect = document.getElementById('profesor');
    const fechaInicioInput = document.getElementById('fechaInicio');
    const fechaFinInput = document.getElementById('fechaFin');
    const horaInicioInput = document.getElementById('horaInicio');
    const horaFinInput = document.getElementById('horaFin');
    const calcularBtn = document.getElementById('calcularBtn');
    const resultadoCalculo = document.getElementById('resultadoCalculo');
    const clasesTotalesSpan = document.getElementById('clasesTotales');
    const horasPorSesionSpan = document.getElementById('horasPorSesion');
    const errorMessage = document.getElementById('errorMessage');
    const gruposTable = document.getElementById('gruposTable').querySelector('tbody');
    const checkboxesDias = document.querySelectorAll('input[name="dias"]');

    // Elementos del modal de detalle
    const detalleModal = document.getElementById('detalleModal');
    const closeModal = document.querySelector('.close');
    const detalleNombre = document.getElementById('detalleNombre');
    const detalleInfo = document.getElementById('detalleInfo');

    // Variables globales
    let diasFestivos = new Set();
    let grupos = JSON.parse(localStorage.getItem("grupos")) || []; // Cargar grupos existentes

    // =========== FUNCIÓN CENTRALIZADA PARA CERRAR EL MODAL (NUEVA) ===========
    
    // Función para cerrar el modal y restaurar el scroll
    function cerrarModal() {
        detalleModal.style.display = 'none';
        document.body.style.overflow = ''; // Restaura el scroll
    }

    // =========== MANTENEMOS LAS FUNCIONALIDADES BÁSICAS EXISTENTES ===========
    
    // Funcionalidad: Tipo de salón → Salón → Capacidad
    if (selectTipoSalon && selectSalon && inputCapacidad) {
        selectTipoSalon.addEventListener('change', function () {
            const idAreaSeleccionada = this.value;

            Array.from(selectSalon.options).forEach(option => {
                const areaOption = option.getAttribute('data-area');
                option.hidden = !(option.value === "" || areaOption === idAreaSeleccionada);
            });

            selectSalon.value = '';
            inputCapacidad.value = '';
        });

        selectSalon.addEventListener('change', function () {
            const aforo = this.options[this.selectedIndex].getAttribute('data-aforo');
            inputCapacidad.value = aforo || '';
        });
    }

    // Funcionalidad: Programa → Módulos
    if (selectPrograma && selectModulo) {
        selectPrograma.addEventListener('change', function () {
            const idPrograma = this.value;

            Array.from(selectModulo.options).forEach(option => {
                const programaOption = option.getAttribute('data-programa');
                option.hidden = !(option.value === "" || programaOption === idPrograma);
            });

            selectModulo.value = '';
            if (inputHorasTotales) {
                inputHorasTotales.value = '';
            }
        });

        selectModulo.addEventListener('change', function () {
            const horas = this.options[this.selectedIndex].getAttribute('data-horas');
            if (inputHorasTotales) {
                inputHorasTotales.value = horas || '';
            }
        });
    }

    // =========== FUNCIONES PARA INTEGRACIÓN CON API FESTIVOS ===========
    
    // Función para obtener días festivos de la API
    async function obtenerDiasFestivos(año) {
        try {
            // Intentar primero la URL relativa
            let url = `/api/festivos/${año}/`;
            
            // Si estás trabajando en un entorno local, prueba la URL de desarrollo
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        // Si falla, intentar con la URL de desarrollo
                        url = `http://192.168.1.162/festivos/${año}`;
                        
                    }
                } catch (e) {
                    // Si hay un error (CORS, etc.), intentar con la URL de desarrollo
                    url = `http://192.168.1.162/festivos/${año}`;
                }
            }
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Error al obtener días festivos: ${response.status}`);
            }
            
            const data = await response.json();

            // Convertir cada fecha recibida a una fecha local y formatearla
            const diasFestivosSet = new Set(
                data.map(item => formatearFechaISO(parseLocalDateFromString(item.fecha)))
            );

            console.log("Días festivos recibidos:", Array.from(diasFestivosSet));
            return diasFestivosSet;
        } catch (error) {
            console.error("Error al obtener días festivos:", error);
            mostrarError("Error al obtener días festivos. Verifique su conexión.");
            return new Set();
        }
    }

    // =========== FUNCIONES PARA CÁLCULO DE FECHAS Y CLASES ===========
    
    // Función principal para calcular fecha fin y clases
    async function calcularFechaFinYClases() {
        // Obtener los valores del formulario
        const fechaInicio = fechaInicioInput.value;
        const horaInicio = horaInicioInput.value;
        const horaFin = horaFinInput.value;
        const horasTotales = parseInt(inputHorasTotales.value);
        
        const diasSeleccionados = [];
        checkboxesDias.forEach(checkbox => {
            if (checkbox.checked) {
                diasSeleccionados.push(checkbox.value);
            }
        });

        // Validar datos
        if (!fechaInicio || !horaInicio || !horaFin || isNaN(horasTotales) || diasSeleccionados.length === 0) {
            mostrarError("Por favor complete todos los campos necesarios para el cálculo.");
            return false;
        }

        // Calcular duración de cada sesión en horas
        const [horaInicioH, horaInicioM] = horaInicio.split(":").map(Number);
        const [horaFinH, horaFinM] = horaFin.split(":").map(Number);
        
        const inicioMinutos = horaInicioH * 60 + horaInicioM;
        const finMinutos = horaFinH * 60 + horaFinM;
        
        if (inicioMinutos >= finMinutos) {
            mostrarError("La hora de inicio debe ser anterior a la hora de fin.");
            return false;
        }
        
        const horasPorSesion = (finMinutos - inicioMinutos) / 60;

        // Mostrar mensaje de carga
        mostrarCargando();

        try {
            // Usar la versión mejorada de calcularFechaFin
            const resultado = await calcularFechaFin(
                fechaInicio,
                diasSeleccionados,
                horasTotales,
                horasPorSesion
            );
            
            // Establecer la fecha de fin en el formulario
            fechaFinInput.value = formatearFechaISO(resultado.fechaFin);
            fechaFinInput.disabled = false; // Permitir editar si es necesario
            
            // Actualizar información en el resultado
            clasesTotalesSpan.textContent = resultado.sesionesTotales;
            horasPorSesionSpan.textContent = horasPorSesion.toFixed(2);
            resultadoCalculo.classList.remove('d-none');
            
            // Mostrar calendario de clases
            mostrarCalendarioClases(resultado.fechasClases);
            
            // Si las horas acumuladas son mayores que las requeridas, mostrar advertencia
            if (resultado.horasAcumuladas > horasTotales) {
                mostrarError(
                    `Con los días y horarios seleccionados se acumularán ${resultado.horasAcumuladas.toFixed(2)} horas, que es mayor que las ${horasTotales} horas requeridas.`
                );
            } else {
                ocultarError();
            }
            
            // Ocultar mensaje de carga
            ocultarCargando();
            
            return true;
        } catch (error) {
            console.error("Error al calcular fecha fin:", error);
            mostrarError(`Error al calcular la fecha de finalización: ${error.message}`);
            ocultarCargando();
            return false;
        }
    }

    // Función principal para calcular la fecha de finalización y fechas de clases
    async function calcularFechaFin(fechaInicio, diasSeleccionados, horasTotales, horasPorSesion) {
        if (
            !fechaInicio ||
            !Array.isArray(diasSeleccionados) ||
            diasSeleccionados.length === 0 ||
            !horasTotales ||
            !horasPorSesion ||
            horasTotales <= 0 ||
            horasPorSesion <= 0
        ) {
            throw new Error("Parámetros inválidos");
        }

        // Convertir fechaInicio a objeto Date
        let inicio = parseLocalDateFromString(fechaInicio);
        if (isNaN(inicio.getTime())) {
            throw new Error("Fecha de inicio inválida");
        }

        // Mapear nombres de días a números (0=Domingo, 1=Lunes, etc.)
        const mapaDias = {
            Domingo: 0,
            Lunes: 1,
            Martes: 2,
            Miércoles: 3,
            Jueves: 4,
            Viernes: 5,
            Sábado: 6,
        };

        // Convertir los nombres de días seleccionados a sus números correspondientes
        const diasIndices = diasSeleccionados.map(dia => mapaDias[dia]);

        // Calcular el número de sesiones necesarias
        const sesionesNecesarias = Math.ceil(horasTotales / horasPorSesion);

        // Obtener los años involucrados
        const añoInicio = inicio.getFullYear();
        const añoSiguiente = añoInicio + 1;

        // Obtener los días festivos para ambos años y combinarlos
        const festivosAñoInicio = await obtenerDiasFestivos(añoInicio);
        const festivosAñoSiguiente = await obtenerDiasFestivos(añoSiguiente);
        const todosFestivos = new Set([...festivosAñoInicio, ...festivosAñoSiguiente]);

        // Iniciar el cálculo desde la fecha de inicio
        let currentDate = new Date(inicio);
        let sesionesCompletadas = 0;
        const fechasClases = [];

        while (sesionesCompletadas < sesionesNecesarias) {
            // Avanzar al siguiente día
            currentDate.setDate(currentDate.getDate() + 1);

            // Obtener la fecha en formato "YYYY-MM-DD"
            const fechaFormateada = formatearFechaISO(currentDate);

            // Si es un día de clase seleccionado y NO es festivo, contar la sesión
            if (diasIndices.includes(currentDate.getDay()) && !todosFestivos.has(fechaFormateada)) {
                sesionesCompletadas++;
                fechasClases.push({
                    fecha: new Date(currentDate),
                    diaSemana: getDiaSemana(currentDate.getDay()),
                    sesion: sesionesCompletadas,
                });
            } else if (
                // Si es festivo pero cae en un día de clase, registrarlo como festivo omitido
                todosFestivos.has(fechaFormateada) &&
                diasIndices.includes(currentDate.getDay())
            ) {
                fechasClases.push({
                    fecha: new Date(currentDate),
                    diaSemana: getDiaSemana(currentDate.getDay()),
                    esFestivo: true,
                    festivoOmitido: true,
                });
            }
        }

        return {
            fechaFin: currentDate,
            sesionesTotales: sesionesCompletadas,
            horasAcumuladas: sesionesCompletadas * horasPorSesion,
            fechasClases: fechasClases,
        };
    }

    // =========== FUNCIONES PARA VERIFICACIÓN DE CONFLICTOS ===========
    
    // Función para verificar conflictos de salón (CORREGIDA)
    function verificarConflictoSalon(salon, fechaInicio, fechaFin, horaInicio, horaFin, dias) {
        return grupos.some(grupo => {
            // Si es el mismo salón - CORREGIDO para comparar IDs, no nombres
            if (grupo.salonId === salon) {
                // Comprobar si hay solapamiento de fechas
                const grupoInicio = new Date(grupo.fechaInicio);
                const grupoFin = new Date(grupo.fechaFin);
                const nuevoInicio = new Date(fechaInicio);
                const nuevoFin = new Date(fechaFin);

                const hayOverlapFechas = !(nuevoFin < grupoInicio || nuevoInicio > grupoFin);

                if (hayOverlapFechas) {
                    // Comprobar si hay solapamiento de horas
                    const [grupoInicioH, grupoInicioM] = grupo.horaInicio.split(":").map(Number);
                    const [grupoFinH, grupoFinM] = grupo.horaFin.split(":").map(Number);
                    const [nuevoInicioH, nuevoInicioM] = horaInicio.split(":").map(Number);
                    const [nuevoFinH, nuevoFinM] = horaFin.split(":").map(Number);

                    const grupoInicioMinutos = grupoInicioH * 60 + grupoInicioM;
                    const grupoFinMinutos = grupoFinH * 60 + grupoFinM;
                    const nuevoInicioMinutos = nuevoInicioH * 60 + nuevoInicioM;
                    const nuevoFinMinutos = nuevoFinH * 60 + nuevoFinM;

                    const hayOverlapHoras = !(
                        nuevoFinMinutos <= grupoInicioMinutos ||
                        nuevoInicioMinutos >= grupoFinMinutos
                    );

                    if (hayOverlapHoras) {
                        // Comprobar si coinciden los días de la semana
                        const hayDiaComun = grupo.dias.some(dia => dias.includes(dia));
                        return hayDiaComun;
                    }
                }
            }
            return false;
        });
    }

    // Función para verificar conflictos de profesor
    function verificarConflictoProfesor(profesor, fechaInicio, fechaFin, horaInicio, horaFin, dias) {
        return grupos.some(grupo => {
            if (grupo.profesor === profesor) {
                // Comprobar si hay solapamiento de fechas
                const grupoInicio = new Date(grupo.fechaInicio);
                const grupoFin = new Date(grupo.fechaFin);
                const nuevoInicio = new Date(fechaInicio);
                const nuevoFin = new Date(fechaFin);

                const hayOverlapFechas = !(nuevoFin < grupoInicio || nuevoInicio > grupoFin);

                if (hayOverlapFechas) {
                    // Comprobar si hay solapamiento de horas
                    const [grupoInicioH, grupoInicioM] = grupo.horaInicio.split(":").map(Number);
                    const [grupoFinH, grupoFinM] = grupo.horaFin.split(":").map(Number);
                    const [nuevoInicioH, nuevoInicioM] = horaInicio.split(":").map(Number);
                    const [nuevoFinH, nuevoFinM] = horaFin.split(":").map(Number);

                    const grupoInicioMinutos = grupoInicioH * 60 + grupoInicioM;
                    const grupoFinMinutos = grupoFinH * 60 + grupoFinM;
                    const nuevoInicioMinutos = nuevoInicioH * 60 + nuevoInicioM;
                    const nuevoFinMinutos = nuevoFinH * 60 + nuevoFinM;

                    const hayOverlapHoras = !(
                        nuevoFinMinutos <= grupoInicioMinutos ||
                        nuevoInicioMinutos >= grupoFinMinutos
                    );

                    if (hayOverlapHoras) {
                        // Comprobar si coinciden los días de la semana
                        const hayDiaComun = grupo.dias.some(dia => dias.includes(dia));
                        return hayDiaComun;
                    }
                }
            }
            return false;
        });
    }

    // =========== FUNCIONES PARA GESTIÓN DE GRUPOS ===========
    
    // Función para crear un nuevo grupo
    function crearGrupo(event) {
        event.preventDefault();
        
        // Obtener datos del formulario
        const nombre = nombreInput.value;
        const modulo = selectModulo.options[selectModulo.selectedIndex].text;
        const moduloId = selectModulo.value;
        const profesor = profesorSelect.value;
        const salon = selectSalon.options[selectSalon.selectedIndex].text;
        const salonId = selectSalon.value;
        const capacidad = inputCapacidad.value;
        const fechaInicio = fechaInicioInput.value;
        const fechaFin = fechaFinInput.value;
        const horaInicio = horaInicioInput.value;
        const horaFin = horaFinInput.value;
        const horasTotales = inputHorasTotales.value;
        
        const diasSeleccionados = [];
        checkboxesDias.forEach(checkbox => {
            if (checkbox.checked) {
                diasSeleccionados.push(checkbox.value);
            }
        });
        
        // Verificar que todos los campos estén completos
        if (!nombre || !modulo || !profesor || !salon || 
            !fechaInicio || !fechaFin || !horaInicio || !horaFin || 
            !horasTotales || diasSeleccionados.length === 0) {
            mostrarError("Por favor complete todos los campos del formulario.");
            return;
        }
        
        // Verificar si hay conflicto de salón
        const haySalonConflicto = verificarConflictoSalon(
            salonId,
            fechaInicio,
            fechaFin,
            horaInicio,
            horaFin,
            diasSeleccionados
        );
        
        if (haySalonConflicto) {
            mostrarError("No se puede crear el grupo. Ya existe un salón en el horario y fechas seleccionados.");
            return;
        }
        
        // Verificar si hay conflicto con el profesor
        const hayProfesorConflicto = verificarConflictoProfesor(
            profesor,
            fechaInicio,
            fechaFin,
            horaInicio,
            horaFin,
            diasSeleccionados
        );
        
        if (hayProfesorConflicto) {
            mostrarError("No se puede asignar el profesor. Ya esta asignado a otro grupo en el mismo horario y días seleccionados.");
            return;
        }
        
        // Obtener el calendario de clases (si se ha calculado)
        const calendarioClases = localStorage.getItem('calendarioClases')
            ? JSON.parse(localStorage.getItem('calendarioClases'))
            : [];
        
        // Crear un objeto para el grupo
        const grupo = {
            id: Date.now(), // ID único basado en timestamp
            nombre,
            modulo,
            moduloId,
            profesor,
            salon,
            salonId,
            capacidad,
            fechaInicio,
            fechaFin,
            horaInicio,
            horaFin,
            horasTotales,
            dias: diasSeleccionados,
            clasesTotales: parseInt(clasesTotalesSpan.textContent) || 0,
            horasPorSesion: parseFloat(horasPorSesionSpan.textContent) || 0,
            fechasClases: calendarioClases,
            creado: new Date().toISOString()
        };
        
        // Intentar guardar en el backend (aquí puedes agregar la llamada al backend cuando esté listo)
        let guardadoEnBackend = false;
        
        // Mientras tanto, guardar en localStorage
        grupos.push(grupo);
        localStorage.setItem('grupos', JSON.stringify(grupos));
        
        // Limpiar formulario
        grupoForm.reset();
        resultadoCalculo.classList.add('d-none');
        
        // Ocultar el calendario si existe
        const calendarioDiv = document.getElementById('calendarioClases');
        if (calendarioDiv) {
            calendarioDiv.style.display = 'none';
        }
        
        // Recargar tabla de grupos
        cargarGrupos();
        
        // Mostrar mensaje de éxito
        mostrarExito("Grupo guardado correctamente");
    }

    // Función para cargar grupos existentes
    function cargarGrupos() {
        // Limpiar tabla
        gruposTable.innerHTML = '';
        
        if (grupos.length === 0) {
            gruposTable.innerHTML = '<tr><td colspan="7" class="text-center">No hay grupos creados todavía</td></tr>';
            return;
        }
        
        // Mostrar cada grupo en la tabla
        grupos.forEach(grupo => {
            const fila = document.createElement('tr');
            
            const fechaInicio = new Date(grupo.fechaInicio);
            const fechaFin = new Date(grupo.fechaFin);
            const ahora = new Date();
            
            const estado = ahora < fechaFin ? "Activo" : "Finalizado";
            const estadoClass = ahora < fechaFin ? "bg-success" : "bg-danger";
            
            fila.innerHTML = `
                <td>${grupo.nombre}</td>
                <td>${grupo.modulo}</td>
                <td>${grupo.profesor}</td>
                <td>${grupo.salon}</td>
                <td>${formatDate(fechaInicio)} - ${formatDate(fechaFin)}</td>
                <td><span class="badge ${estadoClass}">${estado}</span></td>
                <td>
                    <button class="btn btn-sm btn-info ver-detalle" data-id="${grupo.id}">
                        <i class="mdi mdi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-danger eliminar-grupo" data-id="${grupo.id}">
                        <i class="mdi mdi-trash-can"></i>
                    </button>
                </td>
            `;
            
            gruposTable.appendChild(fila);
        });
        
        // Agregar event listeners a los botones
        document.querySelectorAll('.ver-detalle').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = parseInt(this.getAttribute('data-id'));
                mostrarDetalleGrupo(id);
            });
        });
        
        document.querySelectorAll('.eliminar-grupo').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = parseInt(this.getAttribute('data-id'));
                eliminarGrupo(id);
            });
        });
    }

    // Función para ver detalle de un grupo
    function mostrarDetalleGrupo(id) {
        const grupo = grupos.find(g => g.id === id);
        
        if (!grupo) {
            // Usar SweetAlert2 si está disponible, sino el alert tradicional
            if (window.Swal) {
                Swal.fire({
                    title: 'Error',
                    text: 'No se encontró información del grupo',
                    icon: 'error'
                });
            } else {
                alert("No se encontró información del grupo");
            }
            return;
        }
        
        // Modificar la estructura del modal si es necesario
        if (!detalleModal.querySelector('.modal-header')) {
            // Obtener referencias a los elementos originales
            const modalContent = detalleModal.querySelector('.modal-content');
            const closeBtn = modalContent.querySelector('.close');
            const h2 = modalContent.querySelector('h2');
            
            // Crear el nuevo encabezado con flexbox
            const modalHeader = document.createElement('div');
            modalHeader.className = 'modal-header';
            
            // Mover elementos al nuevo encabezado
            modalHeader.appendChild(h2.cloneNode(true));
            modalHeader.appendChild(closeBtn.cloneNode(true));
            
            // Limpiar el contenido actual y agregar la nueva estructura
            modalContent.innerHTML = '';
            modalContent.appendChild(modalHeader);
            
            // Agregar div para el contenido del detalle
            const detalleInfoDiv = document.createElement('div');
            detalleInfoDiv.id = 'detalleInfo';
            modalContent.appendChild(detalleInfoDiv);
            
            // Restaurar los event listeners para el botón de cierre
            modalContent.querySelector('.close').addEventListener('click', cerrarModal);
        }
        
        // Obtener referencias actualizadas
        const detalleNombre = detalleModal.querySelector('h2 span');
        const detalleInfo = detalleModal.querySelector('#detalleInfo');
        
        // Actualizar el título
        if (detalleNombre) {
            detalleNombre.textContent = grupo.nombre;
        }
        
        const fechaInicio = new Date(grupo.fechaInicio);
        const fechaFin = new Date(grupo.fechaFin);
        
        // Estructura mejorada de tabla con columnas de ancho fijo
        detalleInfo.innerHTML = `
            <table class="detail-table">
                <tr>
                    <th>Módulo Académico:</th>
                    <td>${grupo.modulo}</td>
                    <th>Profesor:</th>
                    <td>${grupo.profesor}</td>
                </tr>
                <tr>
                    <th>Salón:</th>
                    <td>${grupo.salon}</td>
                    <th>Capacidad:</th>
                    <td>${grupo.capacidad} estudiantes</td>
                </tr>
                <tr>
                    <th>Fecha de Inicio:</th>
                    <td>${formatDate(fechaInicio)}</td>
                    <th>Fecha de Fin:</th>
                    <td>${formatDate(fechaFin)}</td>
                </tr>
                <tr>
                    <th>Hora de Inicio:</th>
                    <td>${formatHora(grupo.horaInicio)}</td>
                    <th>Hora de Fin:</th>
                    <td>${formatHora(grupo.horaFin)}</td>
                </tr>
                <tr>
                    <th>Días:</th>
                    <td colspan="3">
                        ${grupo.dias.map(dia => `<span class="badge">${dia}</span>`).join(" ")}
                    </td>
                </tr>
                <tr>
                    <th>Horas Totales:</th>
                    <td>${grupo.horasTotales}</td>
                    <th>Horas por Sesión:</th>
                    <td>${grupo.horasPorSesion ? grupo.horasPorSesion.toFixed(2) : '0.00'}</td>
                </tr>
                <tr>
                    <th>Clases Totales:</th>
                    <td>${grupo.clasesTotales || 0}</td>
                    <th>Horas Acumuladas:</th>
                    <td>${grupo.clasesTotales && grupo.horasPorSesion ? (grupo.clasesTotales * grupo.horasPorSesion).toFixed(2) : '0.00'}</td>
                </tr>
            </table>
        `;
        
        // Mostrar el calendario de clases si existe, con mejor estructura para evitar overflow
        if (grupo.fechasClases && grupo.fechasClases.length > 0) {
            let calendarioHTML = `
                <div class="calendario-titulo">
                    <h4>Calendario de Clases</h4>
                </div>
                <ul class="clases-lista">`;
            
            // Limitar a un máximo de elementos para evitar sobrecarga visual
            const maxItems = 50;
            const itemsToShow = grupo.fechasClases.slice(0, maxItems);
            
            itemsToShow.forEach(item => {
                // Formateamos la fecha usando formatDate para mantener la consistencia
                let fechaFormateada;
                try {
                    fechaFormateada = formatDate(new Date(item.fecha));
                } catch (e) {
                    // Manejo de errores en caso de fechas inválidas
                    fechaFormateada = "Fecha inválida";
                }
                let diaSemana = item.diaSemana || "";
                
                if (item.esFestivo) {
                    calendarioHTML += `<li class="clase-item clase-festivo">${fechaFormateada} - ${diaSemana} (Festivo - No hay clase)</li>`;
                } else {
                    calendarioHTML += `<li class="clase-item">${fechaFormateada} - ${diaSemana} - Sesión ${item.sesion || ""}</li>`;
                }
            });
            
            // Si hay más elementos que los mostrados, indicarlo
            if (grupo.fechasClases.length > maxItems) {
                calendarioHTML += `<li class="clase-item" style="font-style: italic;">... y ${grupo.fechasClases.length - maxItems} sesiones más</li>`;
            }
            
            calendarioHTML += `</ul>`;
            detalleInfo.innerHTML += calendarioHTML;
        }
        
        // Hacer que el modal sea scrollable si el contenido es muy largo
        document.body.style.overflow = 'hidden';
        
        // Mostrar el modal con un comportamiento más robusto
        detalleModal.style.display = "block";
    }

    // Función para eliminar un grupo
    function eliminarGrupo(id) {
        if (confirm("¿Está seguro que desea eliminar este grupo?")) {
            grupos = grupos.filter(grupo => grupo.id !== id);
            localStorage.setItem('grupos', JSON.stringify(grupos));
            cargarGrupos();
            mostrarExito("Grupo eliminado correctamente");
        }
    }

    // =========== FUNCIONES PARA CALENDARIO DE CLASES ===========
    
    // Función para mostrar calendario de clases
    function mostrarCalendarioClases(fechasClases) {
        // Guardar el calendario para usarlo al guardar el grupo
        localStorage.setItem('calendarioClases', JSON.stringify(fechasClases));
        
        // Crear un div para el calendario si no existe
        let calendarioDiv = document.getElementById('calendarioClases');
        if (!calendarioDiv) {
            calendarioDiv = document.createElement('div');
            calendarioDiv.id = 'calendarioClases';
            calendarioDiv.className = 'calendario-clases';
            
            // Añadir estilos para el calendario
            const styles = document.createElement('style');
            styles.textContent = `
                .calendario-clases {
                    margin-top: 20px;
                    max-height: 400px;
                    overflow-y: auto;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    background-color: #fff;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }

                .calendario-clases h3 {
                    margin-bottom: 15px;
                    color: #2c3e50;
                    font-size: 1.5rem;
                    text-align: center;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }

                .fechas-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                    gap: 15px;
                }

                .fecha-clase {
                    padding: 12px;
                    border-radius: 8px;
                    background-color: #f9fafb;
                    border-left: 5px solid #3498db;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s;
                }

                .fecha-clase:hover {
                    transform: translateY(-2px);
                }

                .fecha-festivo {
                    background-color: #ffe6e6;
                    border-left: 5px solid #e74c3c;
                    text-decoration: line-through;
                }

                .fecha-mes-header {
                    grid-column: 1 / -1;
                    margin-top: 10px;
                    margin-bottom: 5px;
                    padding: 8px;
                    background: linear-gradient(135deg, #2c3e50, #34495e);
                    color: #fff;
                    border-radius: 8px;
                    font-weight: 600;
                    text-align: center;
                    text-transform: uppercase;
                }
            `;
            document.head.appendChild(styles);
            
            // Añadir el div al formulario después del resultadoCalculo
            const resultadoCalculo = document.getElementById('resultadoCalculo');
            resultadoCalculo.parentNode.insertBefore(calendarioDiv, resultadoCalculo.nextSibling);
        }
        
        // Limpiar el div del calendario
        calendarioDiv.innerHTML = '';
        
        // Crear el título
        const titulo = document.createElement('h3');
        titulo.textContent = 'Calendario de Clases';
        calendarioDiv.appendChild(titulo);
        
        // Crear el contenedor de fechas
        const fechasGrid = document.createElement('div');
        fechasGrid.className = 'fechas-grid';
        calendarioDiv.appendChild(fechasGrid);
        
        // Agrupar fechas por mes
        const fechasPorMes = {};
        fechasClases.forEach(item => {
            const fecha = new Date(item.fecha);
            const mesAño = `${fecha.getFullYear()}-${fecha.getMonth() + 1}`;
            
            if (!fechasPorMes[mesAño]) {
                fechasPorMes[mesAño] = [];
            }
            
            fechasPorMes[mesAño].push(item);
        });
        
        // Mostrar fechas agrupadas por mes
        Object.keys(fechasPorMes).sort().forEach(mesAño => {
            const [año, mes] = mesAño.split('-').map(Number);
            
            // Crear encabezado del mes
            const mesHeader = document.createElement('div');
            mesHeader.className = 'fecha-mes-header';
            mesHeader.textContent = new Date(año, mes - 1, 1).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
            fechasGrid.appendChild(mesHeader);
            
            // Mostrar cada fecha de clase
            fechasPorMes[mesAño].forEach(item => {
                const fechaDiv = document.createElement('div');
                fechaDiv.className = item.esFestivo ? 'fecha-clase fecha-festivo' : 'fecha-clase';
                
                // Construir texto de la fecha
                let textoFecha = `${formatDate(new Date(item.fecha))} - ${item.diaSemana}`;
                
                if (item.esFestivo) {
                    textoFecha += ' (Festivo - No hay clase)';
                } else if (item.sesion) {
                    textoFecha += ` - Sesión ${item.sesion}`;
                }
                
                fechaDiv.textContent = textoFecha;
                fechasGrid.appendChild(fechaDiv);
            });
        });
        
        // Hacer visible el calendario
        calendarioDiv.style.display = 'block';
    }

    // =========== FUNCIONES DE UTILIDAD UI ===========
    
    // Función para mostrar mensaje de error
    function mostrarError(mensaje) {
        errorMessage.textContent = mensaje;
        errorMessage.style.display = 'block';
        
        // Ocultar el mensaje después de 5 segundos
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    // Función para ocultar mensaje de error
    function ocultarError() {
        errorMessage.style.display = 'none';
    }

    // Función para mostrar mensaje de éxito
    function mostrarExito(mensaje) {
        // Crear mensaje de éxito si no existe
        let exitoMessage = document.getElementById('exitoMessage');
        
        if (!exitoMessage) {
            exitoMessage = document.createElement('div');
            exitoMessage.id = 'exitoMessage';
            exitoMessage.className = 'alert alert-success mt-3';
            errorMessage.parentNode.insertBefore(exitoMessage, errorMessage);
        }
        
        exitoMessage.textContent = mensaje;
        exitoMessage.style.display = 'block';
        
        // Ocultar el mensaje después de 3 segundos
        setTimeout(() => {
            exitoMessage.style.display = 'none';
        }, 3000);
    }

    // Función para mostrar mensaje de carga
    function mostrarCargando() {
        // Crear indicador de carga si no existe
        let cargandoIndicator = document.getElementById('cargandoIndicator');
        
        if (!cargandoIndicator) {
            cargandoIndicator = document.createElement('div');
            cargandoIndicator.id = 'cargandoIndicator';
            cargandoIndicator.style.display = 'none';
            cargandoIndicator.style.padding = '10px';
            cargandoIndicator.style.backgroundColor = '#f8f9fa';
            cargandoIndicator.style.borderRadius = '4px';
            cargandoIndicator.style.margin = '10px 0';
            cargandoIndicator.style.textAlign = 'center';
            cargandoIndicator.textContent = 'Calculando fechas, por favor espere...';
            
            // Insertar antes del div de error
            errorMessage.parentNode.insertBefore(cargandoIndicator, errorMessage);
        }
        
        cargandoIndicator.style.display = 'block';
    }

    // Función para ocultar mensaje de carga
    function ocultarCargando() {
        const cargandoIndicator = document.getElementById('cargandoIndicator');
        
        if (cargandoIndicator) {
            cargandoIndicator.style.display = 'none';
        }
    }

    // =========== EVENT LISTENERS ===========
    
    // Evento para calcular clases y fecha fin
    if (calcularBtn) {
        calcularBtn.addEventListener('click', calcularFechaFinYClases);
    }
    
    // Evento para enviar formulario
    if (grupoForm) {
        grupoForm.addEventListener('submit', crearGrupo);
    }
    
    // Eventos para el modal - ACTUALIZADOS PARA USAR LA FUNCIÓN cerrarModal
    if (closeModal) {
        closeModal.addEventListener('click', cerrarModal);
        
        window.addEventListener('click', function(event) {
            if (event.target === detalleModal) {
                cerrarModal();
            }
        });
    }

    // =========== INICIALIZACIÓN ===========
    
    // Cargar grupos al iniciar
    cargarGrupos();
});