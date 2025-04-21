document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos todas las cabeceras con la clase 'toggle-card'
    const cardHeaders = document.querySelectorAll('.toggle-card');

    cardHeaders.forEach(function (header) {
        header.addEventListener('click', function () {
            // Obtenemos la clase común del grupo de tarjetas (la clase que identifica el grupo)
            const cardGroupClass = header.closest('.card').classList[1]; // Segunda clase es 'group-1', 'group-2', etc.

            // Seleccionamos todas las tarjetas que comparten la misma clase de grupo
            const cardsToToggle = document.querySelectorAll(`.${cardGroupClass}`);

            // Iteramos sobre cada tarjeta para colapsar/expandir su contenido
            cardsToToggle.forEach(function (card) {
                const cardContent = card.querySelector('.collapse');

                // Usamos Bootstrap Collapse para alternar el contenido de cada tarjeta
                const collapseInstance = new bootstrap.Collapse(cardContent, {
                    toggle: true
                });

                collapseInstance.toggle(); // Alternamos el estado de la tarjeta
            });
        });
    });
});