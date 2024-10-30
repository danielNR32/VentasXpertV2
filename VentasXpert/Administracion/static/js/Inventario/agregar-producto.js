document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("confirmModal");
    var closeModalBtn = document.getElementById("closeModal");
    var cancelBtn = document.getElementById("cancelBtn");
    var openModalBtn = document.getElementById("openModal");
    var openModalBtn2 = document.getElementById("openModal2");
    var confirmBtn = document.getElementById("confirmBtn");

    // Abrir el modal
    openModalBtn.addEventListener('click', function () {
        modal.style.display = "block"; // Mostrar el modal
    });

    // Abrir el modal cancerlar
    openModalBtn2.addEventListener('click', function () {
        modal.style.display = "block"; // Mostrar el modal
    });

    // Cerrar el modal con la "X"
    closeModalBtn.addEventListener('click', function () {
        modal.style.display = "none"; // Cerrar el modal
    });

    // Abrir confirmar"
    confirmBtn.addEventListener('click', function () {
        modal.style.display = "none"; // Cerrar el modal
        window.history.back();

    });
    // Cerrar el modal con el botón "Cancelar"
    cancelBtn.addEventListener('click', function () {
        modal.style.display = "none"; // Cerrar el modal
    });

    // Cerrar el modal si el usuario hace clic fuera del contenido
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});


