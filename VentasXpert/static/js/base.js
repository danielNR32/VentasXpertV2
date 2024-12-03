let inactivityTimeout;

function resetInactivityTimer() {
    clearTimeout(inactivityTimeout);

    // Cierra sesión después de 15 minutos (900,000 milisegundos)
    inactivityTimeout = setTimeout(() => {
        alert("Has sido desconectado por inactividad.");
        window.location.href = "/logout/"; // Cambia a la URL de logout configurada en tu proyecto
    }, 900000); // 15 minutos
}

// Escuchar eventos de actividad del usuario
['click', 'mousemove', 'keydown', 'scroll', 'touchstart'].forEach(event => {
    window.addEventListener(event, resetInactivityTimer);
});

// Inicializa el temporizador
resetInactivityTimer();
