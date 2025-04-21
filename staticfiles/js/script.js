// JavaScript Document
function toggleInput(checkboxId, inputId) {
    var checkbox = document.getElementById(checkboxId);
    var input = document.getElementById(inputId);

    if (checkbox.checked) {
        input.disabled = false;  // Habilita el campo de texto
    } else {
        input.disabled = true;   // Deshabilita el campo de texto
        input.value = '';        // Limpia el campo de texto cuando se deshabilita
    }
}


// Asegúrate de que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function () {
    // Definición de municipios por departamento
    const municipiosPorDepartamento = {
        amazonas: ["Leticia", "Puerto Nariño"],
        antioquia: ["Medellín", "Bello", "Itagüí", "Envigado", "Apartadó", "Turbo", "Rionegro", "Caucasia", "La Ceja", "Caldas", "Sabaneta", "Copacabana", "Girardota", "Guarne", "Guatapé"],
        arauca: ["Arauca", "Arauquita", "Saravena", "Tame", "Cravo Norte", "Fortul"],
        atlantico: ["Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Galapa", "Puerto Colombia", "Baranoa", "Juan de Acosta"],
        bolivar: ["Cartagena", "Magangué", "Turbaco", "Arjona", "Santa Rosa", "San Juan Nepomuceno", "Mompós", "El Carmen de Bolívar"],
        boyaca: ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Puerto Boyacá", "Samacá", "Tibaná", "Moniquirá"],
        caldas: ["Manizales", "Villamaría", "Chinchiná", "Riosucio", "La Dorada", "Salamina", "Neira", "Anserma"],
        caqueta: ["Florencia", "San Vicente del Caguán", "Cartagena del Chairá", "El Doncello", "Puerto Rico", "Solano", "Morelia"],
        casanare: ["Yopal", "Aguazul", "Villanueva", "Tauramena", "Monterrey", "Trinidad", "Maní", "Paz de Ariporo"],
        cauca: ["Popayán", "Santander de Quilichao", "Puerto Tejada", "Cajibío", "El Tambo", "Guapi", "Miranda", "Patía"],
        cesar: ["Valledupar", "Aguachica", "Bosconia", "Chimichagua", "Curumaní", "El Copey", "La Jagua de Ibirico", "Manaure"],
        choco: ["Quibdó", "Istmina", "Tadó", "Condoto", "Riosucio", "Acandí", "Bahía Solano", "El Carmen de Atrato"],
        cordoba: ["Montería", "Cereté", "Sahagún", "Lorica", "Montelíbano", "Planeta Rica", "Tierralta", "San Antero"],
        cundinamarca: ["Bogotá", "Soacha", "Girardot", "Fusagasugá", "Chía", "Zipaquirá", "Facatativá", "Mosquera", "Cajicá", "La Calera"],
        guainia: ["Inírida", "Barranco Minas", "Mapiripana", "San Felipe"],
        guaviare: ["San José del Guaviare", "Calamar", "El Retorno", "Miraflores"],
        huila: ["Neiva", "Pitalito", "Garzón", "La Plata", "Campoalegre", "San Agustín", "Yaguará"],
        laguajira: ["Riohacha", "Maicao", "Uribia", "Albania", "Dibulla", "Fonseca", "Hatonuevo", "San Juan del Cesar"],
        magdalena: ["Santa Marta", "Ciénaga", "Fundación", "Aracataca", "El Banco", "Pivijay", "Plato"],
        meta: ["Villavicencio", "Acacías", "Granada", "San Martín", "Puerto López", "Cumaral", "La Macarena", "San Carlos de Guaroa"],
        narino: ["Pasto", "Tumaco", "Ipiales", "Túquerres", "Samaniego", "La Unión", "Cumbal", "Guachucal"],
        nortesantander: ["Cúcuta", "Ocaña", "Pamplona", "Villa del Rosario", "Los Patios", "Tibú", "Chinácota", "Ábrego"],
        putumayo: ["Mocoa", "Puerto Asís", "La Hormiga", "Orito", "Sibundoy", "Villagarzón", "Puerto Leguízamo"],
        quindio: ["Armenia", "Quimbaya", "Montenegro", "Calarcá", "La Tebaida", "Salento", "Filandia"],
        risaralda: ["Pereira", "Dosquebradas", "Santa Rosa de Cabal", "La Virginia", "Belén de Umbría", "Quinchía"],
        sanandres: ["San Andrés", "Providencia"],
        santander: ["Bucaramanga", "Floridablanca", "Girón", "Piedecuesta", "Barrancabermeja", "San Gil", "Socorro", "Málaga"],
        sucre: ["Sincelejo", "Corozal", "Sampués", "Tolú", "San Marcos", "San Onofre", "Coveñas"],
        tolima: ["Ibagué", "Espinal", "Melgar", "Honda", "Líbano", "Chaparral", "Mariquita"],
        valledelcauca: ["Cali", "Palmira", "Buenaventura", "Tuluá", "Buga", "Cartago", "Yumbo", "Jamundí"],
        vaupes: ["Mitú", "Carurú", "Taraira", "Papunaua"],
        vichada: ["Puerto Carreño", "La Primavera", "Santa Rosalía", "Cumaribo"]
    };

    // Función para actualizar el select de municipios de expedición
    function updateMunicipiosExpedicion() {
        const departamentoSelect = document.getElementById("departamento_expedicion");
        const municipioSelect = document.getElementById("municipio_expedicion");
        const departamento = departamentoSelect.value;

        // Limpiar los municipios actuales
        municipioSelect.innerHTML = '<option value="">Seleccione un Municipio</option>';

        if (municipiosPorDepartamento[departamento]) {
            municipiosPorDepartamento[departamento].forEach(municipio => {
                const option = document.createElement("option");
                option.value = municipio.toLowerCase().replace(/\s+/g, '');
                option.textContent = municipio;
                municipioSelect.appendChild(option);
            });
        }
    }

    // Función para actualizar el select de municipios de nacimiento
    function updateMunicipiosNacimiento() {
        const departamento2Select = document.getElementById("departamento_nacimiento");
        const municipio2Select = document.getElementById("municipio_nacimiento");
        const departamento2 = departamento2Select.value;

        // Limpiar los municipios actuales
        municipio2Select.innerHTML = '<option value="">Seleccione un Municipio</option>';

        if (municipiosPorDepartamento[departamento2]) {
            municipiosPorDepartamento[departamento2].forEach(municipio2 => {
                const option = document.createElement("option");
                option.value = municipio2.toLowerCase().replace(/\s+/g, '');
                option.textContent = municipio2;
                municipio2Select.appendChild(option);
            });
        }
    }
	
	// Función para actualizar el select de municipios de recidencia
    function updateMunicipiosRecidencia() {
        const departamento3Select = document.getElementById("departamento_recidencia");
        const municipio3Select = document.getElementById("municipio_recidencia");
        const departamento3 = departamento3Select.value;

        // Limpiar los municipios actuales
        municipio3Select.innerHTML = '<option value="">Seleccione un Municipio</option>';

        if (municipiosPorDepartamento[departamento3]) {
            municipiosPorDepartamento[departamento3].forEach(municipio3 => {
                const option = document.createElement("option");
                option.value = municipio3.toLowerCase().replace(/\s+/g, '');
                option.textContent = municipio3;
                municipio3Select.appendChild(option);
            });
        }
    }

    // Asignar las funciones de actualización a los eventos onchange de los selects
    const deptExpSelect = document.getElementById("departamento_expedicion");
    if (deptExpSelect) {
        deptExpSelect.addEventListener('change', updateMunicipiosExpedicion);
    }

    const deptNacSelect = document.getElementById("departamento_nacimiento");
    if (deptNacSelect) {
        deptNacSelect.addEventListener('change', updateMunicipiosNacimiento);
    }
	
	const deptResSelect = document.getElementById("departamento_recidencia");
    if (deptResSelect) {
        deptResSelect.addEventListener('change', updateMunicipiosRecidencia);
    }
	
});

 document.getElementById('documento').addEventListener('input', function (event) {
            const input = event.target;
            // Remover caracteres que no sean dígitos
            input.value = input.value.replace(/\D/g, '');
 });

 document.getElementById('telefono').addEventListener('input', function (event) {
            const input = event.target;
            // Remover caracteres que no sean dígitos
            input.value = input.value.replace(/\D/g, '');
 });

 document.getElementById('celular').addEventListener('input', function (event) {
            const input = event.target;
            // Remover caracteres que no sean dígitos
            input.value = input.value.replace(/\D/g, '');
 });

 document.getElementById('celular-empresa').addEventListener('input', function (event) {
            const input = event.target;
            // Remover caracteres que no sean dígitos
            input.value = input.value.replace(/\D/g, '');
 });