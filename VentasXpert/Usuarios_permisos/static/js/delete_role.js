$(document).ready(function () {
    // Función para mostrar el modal de confirmación de eliminación
    window.eliminarRol = function (roleId, roleName) {
        console.log("Función eliminarRol llamada con:", roleId, roleName);
        
        // Asigna el nombre del rol al elemento en el modal, si existe
        const roleNameElement = document.getElementById("deleteRoleName");
        if (roleNameElement) {
            roleNameElement.innerText = roleName;
        } else {
            console.error("Elemento deleteRoleName no encontrado");
        }

        // Configura el evento de confirmación de eliminación
        const confirmButton = document.getElementById("confirmDeleteRole");
        if (confirmButton) {
            confirmButton.onclick = function () {
                console.log("Confirmación de eliminación para el rol:", roleId);
                window.location.href = `/usuarios_permisos/roles/delete/${roleId}/`;
            };
        } else {
            console.error("Botón confirmDeleteRole no encontrado");
        }

        // Muestra el modal de eliminación
        $('#delete_role').modal('show');
    };
});
