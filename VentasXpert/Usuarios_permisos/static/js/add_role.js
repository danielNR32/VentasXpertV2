$(document).ready(function () {
    $('#addRoleForm').submit(function (e) {
        e.preventDefault();
        
        const form = $(this);
        const url = form.attr('action');  // Usamos la URL del atributo action en el formulario

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    $('#add_role').modal('hide');  // Oculta el modal después de guardar
                    location.reload();  // Recarga la página para ver el nuevo rol en la lista
                } else {
                    alert("Error al añadir el rol");
                }
            },
            error: function () {
                alert("Ocurrió un error al procesar la solicitud.");
            }
        });
    });
});
