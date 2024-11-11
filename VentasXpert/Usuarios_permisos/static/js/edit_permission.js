function editarPermiso(permissionId, permissionName, codename, contentType) {
    // Set initial values in the modal form fields
    $('#editPermissionForm').attr('action', `/usuarios_permisos/permisos/edit/${permissionId}/`);
    $('#edit_permission').modal('show');
}

$(document).ready(function() {
    // Handle the submission of the edit form via AJAX
    $('#editPermissionForm').on('submit', function(event) {
        event.preventDefault();
        
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#edit_permission').modal('hide');
                    location.reload(); // Recargar la página para mostrar los cambios actualizados
                } else {
                    // Mostrar errores en caso de que existan
                    alert("Error al actualizar el permiso.");
                }
            },
            error: function() {
                alert("Error al intentar actualizar el permiso.");
            }
        });
    });
});
