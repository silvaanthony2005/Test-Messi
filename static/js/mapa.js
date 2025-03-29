document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el mapa con un zoom más amplio
    var map = L.map('map').setView([10.495145, -66.829104], 3);

    // Añadir la capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Añadir marcadores significativos con más información
    L.marker([-34.5456, -58.4497]).addTo(map)
        .bindPopup(`
            <b>Estadio Monumental</b><br>
            Primer partido de Messi con Argentina<br>
            Fecha: 17/08/2005<br>
            Partido: Argentina vs Hungría<br>
            Messi debutó con solo 18 años
        `);

    L.marker([41.3809, 2.1228]).addTo(map)
        .bindPopup(`
            <b>Camp Nou</b><br>
            Estadio del FC Barcelona<br>
            Messi jugó aquí desde 2004 hasta 2021<br>
            Marcó 672 goles en 778 partidos<br>
            Ganó 4 Champions League y 10 Ligas
        `);

    L.marker([-32.9507, -60.6665]).addTo(map)
        .bindPopup(`
            <b>Rosario</b><br>
            Ciudad natal de Lionel Messi<br>
            Nació el 24/06/1987<br>
            Comenzó a jugar en Newell's Old Boys<br>
            Se mudó a Barcelona a los 13 años
        `);

    // Añadir más marcadores importantes
    L.marker([48.8414, 2.2530]).addTo(map)
        .bindPopup(`
            <b>Parque de los Príncipes</b><br>
            Estadio del PSG<br>
            Messi jugó aquí desde 2021 hasta 2023<br>
            Ganó 2 Ligas Francesas
        `);

    L.marker([25.7935, -80.1392]).addTo(map)
        .bindPopup(`
            <b>DRV PNK Stadium</b><br>
            Estadio del Inter Miami<br>
            Messi juega aquí desde 2023<br>
            Ganó la Leagues Cup en su primer año
        `);

        L.marker([10.495145, -66.829104]).addTo(map)
        .bindPopup(`
            <b>Universidad Alejandro de Humbolt</b><br>
            Punto de reunión con Messi<br>
            Todos esperamos conocerlo algún día<br>
        `);
});

document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-messages div');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.remove();
        }, 1000); // 1000ms = 1 segundos
    });
});