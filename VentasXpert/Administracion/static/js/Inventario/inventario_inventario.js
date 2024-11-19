$(document).ready(function () {
    const table = $('#productosTable').DataTable({
        responsive: true,
        scrollY: "400px",  // Altura máxima para el desplazamiento vertical
        scrollCollapse: true,  // Habilita colapsar si los datos son pocos
        paging: true,
        ajax: {
            url: "{% url 'productos_api' %}",
            data: function (d) {
                d.categoria = $('#categoriaFilter').val();
                d.estado = $('#estadoFilter').val();
            },
            dataSrc: 'data',
        },
        columns: [
            { data: 'codigo' },
            { data: 'nombre' },
            { data: 'categoria' },
            { data: 'estado_stock' },
            { data: 'cantidad_minima' },
            { data: 'cantidad_total' },
            { data: 'precio_tienda' },
            { data: 'ganancia' },

        ],
        createdRow: function (row, data, dataIndex) {
            // Seleccionar la celda correspondiente al "Estado en stock"
            const estadoCell = $('td', row).eq(3);

            // Agregar clases según el estado de inventario
            if (data.estado_stock === "Sin existencia") {
                estadoCell.addClass('sin-existencia');
            } else if (data.estado_stock === "Poca existencia") {
                estadoCell.addClass('poca-existencia');
            } else if (data.estado_stock === "Suficiente") {
                estadoCell.addClass('Suficiente');
            }
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.1/i18n/es-ES.json',
        },
        pagingType: "simple_numbers",
        dom: '<"top"f>rt<"bottom"p>',
    });

    // Actualizar tabla cuando se selecciona un filtro
    $('#categoriaFilter, #estadoFilter').change(function () {
        table.ajax.reload();
    });

    // Buscar en la tabla
    $('#searchInput').on('keyup', function () {
        table.search(this.value).draw();
    });
});


$(document).ready(function () {
    // Cargar categorías dinámicamente
    $.ajax({
        url: "{% url 'categorias_api' %}", // Ruta a la vista de categorías
        method: "GET",
        success: function (response) {
            const categoriaFilter = $('#categoriaFilter');
            categoriaFilter.empty(); // Limpia las opciones
            categoriaFilter.append('<option value="">Filtrar por categoría</option>');
            response.categorias.forEach(categoria => {
                categoriaFilter.append(`<option value="${categoria.nombre}">${categoria.nombre}</option>`);
            });
        },
        error: function () {
            alert("Error al cargar las categorías");
        }
    });
});
