function editarUsuario(userId, userName) {
    const editUserLabel = document.getElementById("editUserLabel");
    if (editUserLabel) {
        editUserLabel.innerText = `Editar Usuario: ${userName} (ID: ${userId})`;
    }

    const editForm = document.getElementById("editUserForm");
    if (editForm) {
        editForm.action = `/usuarios_permisos/usuarios/edit/${userId}/`;
    }

    $.ajax({
        url: `/usuarios_permisos/usuarios/edit/${userId}/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            document.querySelector('.user-username').value = data.formUser.username;
            document.querySelector('.user-email').value = data.formUser.email;
            document.querySelector('.user-password').value = ''; // Dejar vacío para nueva contraseña
            document.querySelector('.user-newpassword').value = ''; // Dejar vacío para la nueva contraseña

            document.querySelector('.person-nombre').value = data.formPerson.nombre;
            document.querySelector('.person-segNombre').value = data.formPerson.segNombre;
            document.querySelector('.person-apPaterno').value = data.formPerson.apPaterno;
            document.querySelector('.person-apMaterno').value = data.formPerson.apMaterno;
            document.querySelector('.person-genero').value = data.formPerson.genero;
            document.querySelector('.person-telefono').value = data.formPerson.telefono;
            document.querySelector('.person-rfc').value = data.formPerson.rfc;
            document.querySelector('.person-curp').value = data.formPerson.curp;
            document.querySelector('.person-correo').value = data.formPerson.correo;

            $('#edit_user').modal('show');
        },
        error: function () {
            alert("Error al cargar los datos del usuario.");
        }
    });
}
