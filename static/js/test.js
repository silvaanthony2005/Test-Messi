document.addEventListener('DOMContentLoaded', function() {
    const comenzarBtn = document.querySelector('.comenzar-btn');
    const preguntaContainer = document.querySelector('.pregunta');
    const siguienteBtn = document.querySelector('.siguiente-btn');
    const form = document.querySelector('.preguntas-form');
    const timerElement = document.querySelector('.timer');
    const progressBar = document.querySelector('.progress');
    let timeLeft = 30;
    let countdown;

    // Obtener las respuestas correctas y el índice de la pregunta actual desde los atributos data
    const correctAnswer = JSON.parse(document.getElementById('respuestas-correctas').dataset.respuestas);
    const preguntaActual = parseInt(document.getElementById('pregunta-actual').dataset.preguntaActual);

    if (comenzarBtn && preguntaActual === 0) {
        comenzarBtn.addEventListener('click', function() {
            // Ocultar el botón de comenzar y mostrar la primera pregunta
            comenzarBtn.style.display = 'none';
            preguntaContainer.style.display = 'block';
            startTimer();
        });
    } else {
        // Si no es la primera pregunta, mostrar directamente la pregunta
        if (comenzarBtn) comenzarBtn.style.display = 'none';
        if (preguntaContainer) preguntaContainer.style.display = 'block';
        startTimer();
    }

    function startTimer() {
        clearInterval(countdown);
        timeLeft = 30;
        timerElement.textContent = timeLeft;
        progressBar.style.width = '100%';

        countdown = setInterval(() => {
            timeLeft--;
            timerElement.textContent = timeLeft;
            progressBar.style.width = `${(timeLeft / 30) * 100}%`;

            if (timeLeft <= 0) {
                clearInterval(countdown);
                form.submit();
            }
        }, 1000);
    }

    if (siguienteBtn) {
        siguienteBtn.addEventListener('click', function() {
            const selectedOption = preguntaContainer.querySelector('input[type="radio"]:checked');

            if (selectedOption) {
                // Marcar respuesta correcta/incorrecta
                const options = preguntaContainer.querySelectorAll('.opciones label');
                options.forEach((option, i) => {
                    if (i + 1 === correctAnswer[preguntaActual]) {
                        option.style.backgroundColor = '#4CAF50'; // Verde para respuesta correcta
                    } else if (selectedOption.value == i + 1) {
                        option.style.backgroundColor = '#f44336'; // Rojo para respuesta incorrecta
                    }
                });

                // Esperar un momento antes de cambiar de pregunta
                setTimeout(() => {
                    form.submit();
                }, 1000); // 1 segundo de espera
            } else {
                alert('Por favor selecciona una respuesta');
            }
        });
    }
}); 