function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function eliminarUsuario(userId, userName) {
    document.getElementById("deleteUserName").innerText = userName;
    
    document.getElementById("confirmDeleteUser").onclick = function () {
        $.ajax({
            url: `/usuarios_permisos/usuarios/delete/${userId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function (response) {
                if (response.success) {
                    $('#delete_user').modal('hide');  // ✅ Cierra el modal
                    actualizarListaUsuarios();  // ✅ Actualiza la lista sin recargar
                } else {
                    console.error("Error al eliminar el usuario.");
                }
            },
            error: function () {
                console.error("Error en la petición AJAX.");
            }
        });
    };

    $('#delete_user').modal('show');
}

function actualizarListaUsuarios() {
    $.ajax({
        url: '/usuarios_permisos/usuarios/',  // ✅ Asegúrate de que esta URL es correcta
        type: 'GET',
        success: function (response) {
            $('#userTableContainer').html($(response).find('#userTableContainer').html()); // ✅ Solo actualiza la tabla
        },
        error: function () {
            console.error("Error al actualizar la lista de usuarios.");
        }
    });
}
