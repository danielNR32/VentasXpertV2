// Función para abrir el modal de asignación de rol
function assignRoleToUser(userId, userName) {
    // Actualizar el título del modal
    $('#assignRoleToUserLabel').text(`Asignar Rol al Usuario: ${userName}`);

    // Configurar la acción del formulario
    $('#assignRoleForm').attr('action', `/usuarios_permisos/usuarios/assign_role/${userId}/`);

    // Mostrar el modal
    $('#assign_role_to_user').modal('show');
}

// Manejo del formulario de asignación de rol
$(document).on('submit', '#assignRoleForm', function(event) {
    event.preventDefault(); // Prevenir el envío del formulario por defecto

    // Deshabilitar el botón de envío para evitar múltiples envíos
    $('#assignRoleForm button[type="submit"]').prop('disabled', true);

    $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: $(this).serialize(), // Serializar los datos del formulario
        success: function(response) {
            // Habilitar el botón de envío
            $('#assignRoleForm button[type="submit"]').prop('disabled', false);

            if (response.success) {
                $('#assign_role_to_user').modal('hide'); // Ocultar el modal
                location.reload(); // Recargar la página
            } else {
                $('#formErrors').text(response.error ? response.error : 'Ocurrió un error al asignar el rol. Intente nuevamente.');
            }
        },
        error: function() {
            // Habilitar el botón de envío
            $('#assignRoleForm button[type="submit"]').prop('disabled', false);

            alert("Error al intentar asignar el rol.");
        }
    });
});
