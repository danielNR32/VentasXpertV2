$(document).ready(function () {
    // Hacer global la función editarUsuario
    window.editarUsuario = function(userId, userName) {
        console.log("Editar usuario:", userId, userName); // Para depuración en consola

        // Actualizar el título del modal
        $('#editUserLabel').text(`Editar Usuario: ${userName}`);

        // Configurar la acción del formulario con el ID del usuario
        $('#editUserForm').attr('action', `/usuarios_permisos/usuarios/edit/${userId}/`);

        // Realizar la petición AJAX para obtener los datos del usuario
        $.ajax({
            url: `/usuarios_permisos/usuarios/edit/${userId}/`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('.user-username').val(data.formUser.username);
                $('.user-email').val(data.formUser.email);
                $('.user-password').val('');
                $('.user-newpassword').val('');

                $('.person-nombre').val(data.formPerson.nombre);
                $('.person-segNombre').val(data.formPerson.segNombre);
                $('.person-apPaterno').val(data.formPerson.apPaterno);
                $('.person-apMaterno').val(data.formPerson.apMaterno);
                $('.person-genero').val(data.formPerson.genero);
                $('.person-telefono').val(data.formPerson.telefono);
                $('.person-rfc').val(data.formPerson.rfc);
                $('.person-curp').val(data.formPerson.curp);
                $('.person-correo').val(data.formPerson.correo);

                // Mostrar el modal
                $('#edit_user').modal('show');
            },
            error: function () {
                console.error("Error al cargar los datos del usuario.");
            }
        });
    };

    // Manejo del formulario para editar usuario
    $('#editUserForm').submit(function (e) {
        e.preventDefault();
        
        const form = $(this);
        const url = form.attr('action');

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            success: function (response) {
                // Limpiar errores anteriores
                form.find('.is-invalid').removeClass('is-invalid');
                form.find('.invalid-feedback').remove();

                if (response.success) {
                    $('#edit_user').modal('hide');  // Oculta el modal
                    setTimeout(function () {
                        window.location.href = "/usuarios_permisos/usuarios/";  // Redirigir a user.html
                    }, 500);  // Pequeño delay para que se vea el cierre del modal
                } else if (response.errors) {
                    for (const [field, messages] of Object.entries(response.errors)) {
                        const fieldElement = form.find(`[name="${field}"]`);
                        if (fieldElement.length) {
                            fieldElement.addClass('is-invalid');
                            fieldElement.after(`<div class="invalid-feedback">${messages.join(', ')}</div>`);
                        } else {
                            console.warn(`Campo no encontrado en el formulario: ${field}`);
                        }
                    }
                } else {
                    alert("Error al actualizar el usuario");
                }
            },
            error: function (xhr) {
                console.error("Error en la petición AJAX:", xhr.responseText);
            }
        });
    });
});
