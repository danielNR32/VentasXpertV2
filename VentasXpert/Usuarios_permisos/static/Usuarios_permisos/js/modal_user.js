document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#addUserForm');  // Asegúrate de darle este ID al formulario
    const modal = new bootstrap.Modal(document.getElementById('globalModal'), {});
    const successAlert = document.getElementById('successAlert');
    const errorAlert = document.getElementById('errorAlert');
    const userFormErrors = document.getElementById('userFormErrors');
    const personFormErrors = document.getElementById('personFormErrors');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Resetea las alertas y mensajes de error
        successAlert.style.display = 'none';
        errorAlert.style.display = 'none';
        userFormErrors.innerHTML = '';
        personFormErrors.innerHTML = '';

        const formData = new FormData(form);

        fetch('/usuarios_permisos/add_user/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // Indica que es una petición AJAX
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Muestra una alerta de éxito
                successAlert.style.display = 'block';
                successAlert.innerText = 'Usuario registrado correctamente';

                // Cierra el modal después de un tiempo
                setTimeout(() => {
                    modal.hide();
                    form.reset();
                }, 2000);
            } else {
                // Muestra los errores
                errorAlert.style.display = 'block';
                errorAlert.innerText = 'Ocurrieron errores al registrar el usuario';
                if (data.errors) {
                    userFormErrors.innerHTML = data.errors.user_form_errors.join('<br>');
                    personFormErrors.innerHTML = data.errors.person_form_errors.join('<br>');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorAlert.style.display = 'block';
            errorAlert.innerText = 'Ocurrió un error inesperado.';
        });
    });
});
