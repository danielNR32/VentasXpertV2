$(document).ready(function () {
    $('#addUserForm').submit(function (e) {
        e.preventDefault();
        
        const form = $(this);
        const url = form.attr('action');  // Usamos la URL del atributo action en el formulario

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            success: function (response) {
                // Limpiar errores anteriores
                form.find('.is-invalid').removeClass('is-invalid');
                form.find('.invalid-feedback').remove();

                if (response.success) {
                    alert(response.message);
                    $('#add_user').modal('hide');  // Oculta el modal después de guardar
                    location.reload();  // Recarga la página para ver el nuevo usuario en la lista
                } else if (response.errors) {
                    // Mostrar errores en los campos específicos
                    for (const [field, messages] of Object.entries(response.errors)) {
                        const fieldElement = form.find(`#id_${field}`);
                        fieldElement.addClass('is-invalid');
                        fieldElement.after(`<div class="invalid-feedback">${messages.join(', ')}</div>`);
                    }
                } else {
                    alert("Error al añadir el usuario");
                }
            },
            error: function () {
                alert("Ocurrió un error al procesar la solicitud.");
            }
        });
    });
});
