$(document).ready(function () {
    $('#addUserForm').submit(function (e) {
        e.preventDefault();
        
        const form = $(this);
        const url = form.attr('action');  // Toma la URL del atributo action en el formulario

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            headers: {
                "X-Requested-With": "XMLHttpRequest"  // Asegura que Django reconozca la solicitud AJAX
            },
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
                        // Verifica si el campo existe en el formulario antes de agregar la clase de error
                        const fieldElement = form.find(`[name="${field}"]`);
                        if (fieldElement.length) {
                            fieldElement.addClass('is-invalid');
                            fieldElement.after(`<div class="invalid-feedback">${messages.join(', ')}</div>`);
                        } else {
                            console.warn(`Campo no encontrado en el formulario: ${field}`);
                        }
                    }
                } else {
                    alert("Error al añadir el usuario");
                }
            },
            error: function (xhr) {
                alert("Ocurrió un error al procesar la solicitud.");
                console.error("Error en la petición AJAX:", xhr.responseText);
            }
        });
    });
});
