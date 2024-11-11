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
                'X-CSRFToken': getCSRFToken()  // Usar la función para obtener el token CSRF
            },
            success: function (response) {
                if (response.success) {
                    $('#delete_user').modal('hide');
                    location.reload();
                } else {
                    alert("Error al eliminar el usuario.");
                }
            },
            error: function () {
                alert("Error al intentar eliminar el usuario.");
            }
        });
    };

    $('#delete_user').modal('show');
}
