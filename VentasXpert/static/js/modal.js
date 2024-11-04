document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("confirmModal");
    var closeModalBtn = document.getElementById("closeModal");
    var cancelBtn = document.getElementById("cancelBtn");
    var confirmBtn = document.getElementById("confirmBtn");
    var confirmAction = null; // Acción que se ejecutará cuando se confirme

    // Función global para abrir el modal con diferentes configuraciones
    function openModal(title, onConfirm) {
        // Cambiar el título dinámicamente
        document.getElementById("modal-title").textContent = title || "¿Confirmar acción?";
        modal.style.display = "block"; // Mostrar el modal

        // Asignar la función que se ejecutará cuando el usuario confirme
        confirmAction = onConfirm;
    }

    // Cerrar el modal cuando se haga clic en "X" o "Cancelar"
    closeModalBtn.onclick = function () {
        modal.style.display = "none";
    };
    cancelBtn.onclick = function () {
        modal.style.display = "none";
    };

    // Ejecutar la acción de confirmación cuando el usuario haga clic en "Confirmar"
    confirmBtn.onclick = function () {
        if (confirmAction) {
            confirmAction(); // Ejecutar la función de confirmación
        }
        modal.style.display = "none"; // Cerrar el modal después de confirmar
    };

    // Cerrar el modal si el usuario hace clic fuera del contenido
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // Hacer la función `openModal` global para que pueda ser utilizada en otros scripts
    window.showGlobalModal = openModal;
});
