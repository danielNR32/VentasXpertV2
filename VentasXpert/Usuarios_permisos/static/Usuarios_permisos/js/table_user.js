// table_user.js

$(document).ready(function() {
    $('#userTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/Spanish.json'
        }
    });
});

function editarUsuario(id) {
    // Implementa lógica de edición aquí
    alert("Editar usuario: " + id);
}

function eliminarUsuario(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
        // Implementa lógica de eliminación aquí
        alert("Usuario eliminado: " + id);
    }
}
