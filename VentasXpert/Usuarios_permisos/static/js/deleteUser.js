function eliminarUsuario(id, username) {
    $('#delete_Modal .modal-title').text('Eliminar Usuario');
    $('#delete_Modal .modal-body').html(`<p>¿Estás seguro de que deseas eliminar a <strong>${username}</strong>?</p>`);
    $('#deleteUserForm').attr('action', `/usuarios_permisos/usuarios/eliminar/${id}/`);
    $('#delete_Modal').modal('show');
}
