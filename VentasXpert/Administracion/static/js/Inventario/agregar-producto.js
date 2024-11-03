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








// funcion agregar producto
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.product-form');

    // Detect form autocomplete or suggested values
    form.addEventListener('submit', function () {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.dispatchEvent(new Event('change'));  // Trigger change event to ensure input is registered
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
            const precioProveedorInput = document.getElementById('precio_proveedor');
            const precioTiendaInput = document.getElementById('precio_tienda');
            const gananciaPorcentajeInput = document.getElementById('ganancia_porcentaje');
            const gananciaPesosInput = document.getElementById('ganancia_pesos');

            function calcularGanancia() {
                const precioProveedor = parseFloat(precioProveedorInput.value) || 0;
                const precioTienda = parseFloat(precioTiendaInput.value) || 0;

                if (precioProveedor > 0) {
                    const gananciaPesos = precioTienda - precioProveedor;
                    const gananciaPorcentaje = (gananciaPesos / precioProveedor) * 100;

                    // Actualizar los campos de ganancia en tiempo real
                    gananciaPesosInput.value = gananciaPesos.toFixed(2);
                    gananciaPorcentajeInput.value = gananciaPorcentaje.toFixed(2) + '%';
                } else {
                    gananciaPesosInput.value = '0.00';
                    gananciaPorcentajeInput.value = '0%';
                }
            }

            // Escuchar los cambios en los campos de precio
            precioProveedorInput.addEventListener('input', calcularGanancia);
            precioTiendaInput.addEventListener('input', calcularGanancia);
        });


