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


// Script para agregar neuvo prodcuto con opcion de editar
document.addEventListener('DOMContentLoaded', function () {
    const categoryFilter = document.getElementById('filter-category');
    const searchInput = document.getElementById('search-product');
    const tableRows = document.querySelectorAll('.custom-table tbody tr');

    // Filtrado por categoría
    categoryFilter.addEventListener('change', function () {
        const selectedCategory = this.value.toLowerCase();
        filterTable();
    });

    // Filtrado por texto
    searchInput.addEventListener('keyup', function () {
        filterTable();
    });

    function filterTable() {
        const selectedCategory = categoryFilter.value.toLowerCase();
        const searchTerm = searchInput.value.toLowerCase();

        tableRows.forEach(function (row) {
            const productName = row.cells[1].textContent.toLowerCase();  // Nombre del producto
            const productCategory = row.cells[2].textContent.toLowerCase();  // Categoría del producto

            const matchesCategory = !selectedCategory || productCategory.includes(selectedCategory);
            const matchesSearch = !searchTerm || productName.includes(searchTerm);

            if (matchesCategory && matchesSearch) {
                row.style.display = '';  // Mostrar fila
            } else {
                row.style.display = 'none';  // Ocultar fila
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('productos-tbody');

    tableBody.addEventListener('dblclick', function (event) {
        const target = event.target;

        // Verificar si la celda es editable
        if (target.classList.contains('editable')) {
            const currentValue = target.textContent.trim();
            const fieldName = target.getAttribute('data-field');
            const row = target.closest('tr');
            const rowIndex = row.getAttribute('data-index');

            // Crear un input para editar la celda
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentValue;
            input.classList.add('edit-input');

            // Reemplazar el contenido de la celda con el input
            target.textContent = '';
            target.appendChild(input);
            input.focus();

            // Guardar cambios cuando se presiona Enter o se pierde el foco
            input.addEventListener('blur', function () {
                submitChanges(target, input.value, rowIndex, fieldName);
            });

            input.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    submitChanges(target, input.value, rowIndex, fieldName);
                }
            });
        }
    });

    function submitChanges(cell, newValue, rowIndex, fieldName) {
        // Actualizar el valor visualmente
        cell.textContent = newValue;

        // Actualizar el formulario oculto con los nuevos datos
        document.getElementById('editFieldName').value = fieldName;
        document.getElementById('editFieldValue').value = newValue;
        document.getElementById('editRowIndex').value = rowIndex;

        // Actualizar la acción del formulario con el índice correcto
        const form = document.getElementById('editCellForm');
        form.action = `/administracion/editar_producto_temporal/${rowIndex}/`;

        // Enviar el formulario automáticamente
        form.submit();
    }

});
