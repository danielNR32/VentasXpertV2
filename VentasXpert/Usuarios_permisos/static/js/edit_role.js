function editarRol(roleId, roleName) {
    // Verificar si el elemento con id "editRoleLabel" existe
    const editRoleLabel = document.getElementById("editRoleLabel");
    if (editRoleLabel) {
        editRoleLabel.innerText = "Editar el Rol: " + roleName;
    } else {
        console.error("Elemento 'editRoleLabel' no encontrado");
    }
    
    const editRoleName = document.getElementById("editRoleName");
    if (editRoleName) {
        editRoleName.innerText = roleName;
    } else {
        console.error("Elemento 'editRoleName' no encontrado");
    }

    const editForm = document.getElementById("editRoleForm");
    if (editForm) {
        editForm.action = `/usuarios_permisos/roles/edit/${roleId}/`;
    } else {
        console.error("Formulario 'editRoleForm' no encontrado");
    }

    // Obtener los datos del rol mediante AJAX
    $.ajax({
        url: `/usuarios_permisos/roles/get/${roleId}/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            document.getElementById('nombre').value = data.nombre;
            const permisosSelect = document.getElementById('permisos');
            for (let option of permisosSelect.options) {
                option.selected = false;
            }
            for (let permisoId of data.permisos_ids) {
                for (let option of permisosSelect.options) {
                    if (parseInt(option.value) === permisoId) {
                        option.selected = true;
                        break;
                    }
                }
            }
            $('#edit_role').modal('show');
        },
        error: function () {
            alert("Error al cargar los datos del rol.");
        }
    });
}
