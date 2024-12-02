function editarUsuario(id, username) {
    $('#editModalLabel').text(`Editar Usuario: ${username}`);
    
    // Configura el action del formulario de edición con el id correcto
    $('#editUserForm').attr('action', `/usuarios_permisos/usuarios/editar/${id}/`);
    
    $.ajax({
        url: `/usuarios_permisos/usuarios/editar/${id}/`,
        type: 'GET',
        success: function(data) {
            $('#editModal .modal-body').html(data);
            $('#edit_Modal').modal('show');
        }
    });
}
