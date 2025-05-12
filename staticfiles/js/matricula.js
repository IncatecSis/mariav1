document.addEventListener("DOMContentLoaded", function () {
    const ocupacion = document.getElementById("ocupacion");
    const camposEmpleado = ["empresa_labora", "celular-empresa", "cargo"];

    function toggleCamposEmpleado() {
        const isEmpleado = ocupacion.value === "empleado";
        camposEmpleado.forEach(id => {
            const field = document.getElementById(id);
            field.closest(".mb-3").style.display = isEmpleado ? "block" : "none";
        });
    }

    ocupacion.addEventListener("change", toggleCamposEmpleado);
    toggleCamposEmpleado(); // Ejecuta al cargar por si hay un valor por defecto

    // Controlar los campos según el checkbox en la tabla
    const controles = [
        { check: "bachillerato", inputs: ["enfasis", "lugar_bachillerato"] },
        { check: "tecnico", inputs: ["programa", "lugar_tecnico"] },
        { check: "universitarios", inputs: ["carrera", "lugar_universitarios"] },
        { check: "otros", inputs: ["cual", "lugar_otros"] },
    ];

    controles.forEach(({ check, inputs }) => {
        const checkbox = document.getElementById(check);
        const campos = inputs.map(id => document.getElementById(id));

        function toggleCampos() {
            const habilitar = checkbox.checked;
            campos.forEach(campo => campo.disabled = !habilitar);
        }

        checkbox.addEventListener("change", toggleCampos);
        toggleCampos(); // ejecutar por defecto
    });
});
