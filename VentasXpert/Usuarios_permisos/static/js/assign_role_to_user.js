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
    event.preventDefault(); // Evitar recarga de página

    const form = $(this);
    const url = form.attr('action');

    // Deshabilitar botón para evitar múltiples envíos
    form.find('button[type="submit"]').prop('disabled', true);

    $.ajax({
        url: url,
        type: 'POST',
        data: form.serialize(),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function (response) {
            form.find('button[type="submit"]').prop('disabled', false); // Rehabilitar botón

            if (response.success) {
                $('#assign_role_to_user').modal('hide');  // Cerrar modal sin recargar
                actualizarListaUsuarios();  // Actualizar la lista de usuarios sin recargar la página
            } else {
                alert(response.error || 'Ocurrió un error al asignar el rol.');
            }
        },
        error: function () {
            form.find('button[type="submit"]').prop('disabled', false);
            console.error("Error al intentar asignar el rol.");
        }
    });
});

function actualizarListaUsuarios() {
    $.ajax({
        url: '/usuarios_permisos/usuarios/',  // Asegura que esta URL es correcta
        type: 'GET',
        success: function (response) {
            $('#userTableContainer').html($(response).find('#userTableContainer').html()); // Solo actualiza la tabla
        },
        error: function () {
            console.error("Error al actualizar la lista de usuarios.");
        }
    });
}



