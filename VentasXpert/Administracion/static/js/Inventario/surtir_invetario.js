document.addEventListener('DOMContentLoaded', function () {
    // Búsqueda de productos
    document.querySelector('.custom-input').addEventListener('keyup', buscarProducto);
    document.querySelector('.styled-select').addEventListener('change', buscarProducto);

    function buscarProducto() {
        const codigo = document.querySelector('.codigo').value;
        const nombre = document.querySelector('.nombre').value;
        const categoria = document.querySelector('.styled-select').value;

        fetch(`/buscar_producto/?codigo=${codigo}&nombre=${nombre}&categoria=${categoria}`)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('.custom-table tbody');
                tbody.innerHTML = '';  // Limpiar tabla

                data.productos.forEach(producto => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${producto.id}</td>
                        <td>${producto.codigo}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.categoria}</td>
                        <td>${producto.stock_Inventario}</td>
                        <td><input type="number" min="1" value="1" class="cantidad-surtir"></td>
                        <td><button class="btn-add" onclick="agregarASurtido(${producto.id}, this)">Agregar</button></td>
                    `;
                    tbody.appendChild(row);
                });
            });
    }

    // Agregar producto a surtido temporal
    window.agregarASurtido = function (id, button) {
        const cantidad = button.closest('tr').querySelector('.cantidad-surtir').value;
        fetch('/confirmar_surtido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ id, cantidad })
        }).then(response => {
            if (response.ok) {
                alert("Producto agregado a surtido temporal");
                button.disabled = true;
            }
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
