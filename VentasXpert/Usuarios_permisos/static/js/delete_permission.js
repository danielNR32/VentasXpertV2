function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function eliminarPermiso(permissionId, permissionName) {
    // Set the permission name in the modal for user confirmation
    document.getElementById("deletePermissionName").innerText = permissionName;

    // Set the delete action on the confirm button
    document.getElementById("confirmDeletePermission").onclick = function() {
        $.ajax({
            url: `/usuarios_permisos/permisos/delete/${permissionId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()  // Include the CSRF token in the headers
            },
            success: function(response) {
                if (response.success) {
                    $('#delete_permission').modal('hide');
                    location.reload();  // Reload the page to show the updated list
                } else {
                    alert("Error al eliminar el permiso.");
                }
            },
            error: function(xhr) {
                if (xhr.status === 403) {
                    alert("Error de autenticación CSRF. Intente nuevamente.");
                } else {
                    alert("Error al intentar eliminar el permiso.");
                }
            }
        });
    };

    // Show the modal
    $('#delete_permission').modal('show');
}
