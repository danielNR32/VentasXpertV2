        // Función para abrir el modal
        function openModal() {
            document.getElementById('userModal').style.display = 'flex';
        }

        // Función para cerrar el modal
        function closeModal() {
            document.getElementById('userModal').style.display = 'none';
        }

        // Cerrar el modal si se hace clic fuera del contenido
        window.onclick = function(event) {
            if (event.target == document.getElementById('userModal')) {
                closeModal();
            }
        }