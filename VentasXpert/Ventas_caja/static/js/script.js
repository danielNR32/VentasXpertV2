function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.querySelector('.backdrop'); // Corregir referencia aquí

    if (sidebar.style.left === '0px') {
        sidebar.style.left = '-270px'; // Oculta la barra lateral
        backdrop.style.display = 'none'; // Oculta el fondo oscuro
    } else {
        sidebar.style.left = '0'; // Muestra la barra lateral
        backdrop.style.display = 'block'; // Muestra el fondo oscuro
    }
}

// Asegúrate de que el DOM está completamente cargado antes de añadir el listener
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.backdrop').addEventListener('click', function() {
        toggleSidebar();
    });
});
