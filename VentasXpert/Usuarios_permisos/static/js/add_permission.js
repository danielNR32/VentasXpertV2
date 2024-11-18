$(document).ready(function() {
    // Evento para abrir el modal de agregar permiso
    $('#addPermissionButton').on('click', function() {
        $('#add_permission').modal('show');
    });

    // Manejar el envío del formulario de agregar permiso
    $('#addPermissionForm').on('submit', function(event) {
        event.preventDefault();
        
        $.ajax({
            url: $(this).attr('action'),  // URL del formulario de Django
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#add_permission').modal('hide');
                    location.reload(); // Recargar la página para mostrar el nuevo permiso
                } else {
                    // Manejo de errores si existen
                    alert("Error al añadir el permiso.");
                }
            },
            error: function() {
                alert("Error al intentar añadir el permiso.");
            }
        });
    });
});
