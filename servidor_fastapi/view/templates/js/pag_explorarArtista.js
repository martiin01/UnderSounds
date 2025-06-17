document.addEventListener("DOMContentLoaded", () => {
    const contenedor = document.getElementById("contenedor-productos");
    const filtroOrden = document.getElementById("ordenar");
    const botonesFiltro = document.querySelectorAll(".filter-btn");
    const pagContainer = document.getElementById("paginacion");
    const porPagina = 5;

    // 1) Leemos TODOS los nodos que Jinja ya ha insertado
    const nodos = Array.from(contenedor.querySelectorAll(".producto"));
    // 2) Convertimos esos <div> en objetos JS
    const productos = nodos.map(div => {
        const btn = div.querySelector(".btn-add-cart");
        const match = btn.getAttribute("onclick").match(/'(.+)'/);
        return {
            id: match ? match[1] : "",
            nombre: div.dataset.nombre,
            imagen: div.querySelector("img").src,
            precio: parseFloat(div.dataset.precio),
            fecha: div.dataset.fecha,
            tipo: div.dataset.categoria,
            estilo: div.dataset.estilo,
            link: div.querySelector("a").href
        };
    });

    // Estado inicial
    let filtrados = [...productos];
    let paginaActual = 1;
    let filtrosActivos = new Set();

    // Renderizamos por primera vez
    renderizar();

    // --- Funciones ---
    function renderizar() {
        contenedor.innerHTML = ""; // limpio
        // segmentamos por página
        const inicio = (paginaActual - 1) * porPagina;
        const slice = filtrados.slice(inicio, inicio + porPagina);

        slice.forEach(p => {
            const div = document.createElement("div");
            div.className = "producto";
            // volvemos a inyectar data-attributes (por si cambian filtros)
            div.dataset.categoria = p.tipo;
            div.dataset.estilo = p.estilo;
            div.dataset.precio = p.precio;
            div.dataset.nombre = p.nombre;
            div.dataset.fecha = p.fecha;
            div.innerHTML = `
                <a href="${p.link}">
                    <img src="${p.imagen}" alt="${p.nombre}">
                </a>
                <h3><a href="${p.link}">${p.nombre}</a></h3>
                <p>Precio: ${p.precio}€</p>
                <p>Tipo: ${p.tipo}</p>
                <button class="btn-add-cart" onclick="addToCart('${p.id}')">
                    Añadir al carrito
                </button>
            `;
            contenedor.appendChild(div);
        });

        renderizarPaginacion();
    }

    function renderizarPaginacion() {
        pagContainer.innerHTML = "";
        const totalPaginas = Math.ceil(filtrados.length / porPagina);
        for (let i = 1; i <= totalPaginas; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            btn.className = "pagina-btn" + (i === paginaActual ? " activo" : "");
            btn.addEventListener("click", () => {
                paginaActual = i;
                renderizar();
            });
            pagContainer.appendChild(btn);
        }
    }

    // Ordenación
    filtroOrden.addEventListener("change", () => {
        const c = filtroOrden.value;
        filtrados.sort((a, b) => {
            switch (c) {
                case "precio-asc": return a.precio - b.precio;
                case "precio-desc": return b.precio - a.precio;
                case "nombre-asc": return a.nombre.localeCompare(b.nombre);
                case "nombre-desc": return b.nombre.localeCompare(a.nombre);
                case "fecha-asc": return new Date(a.fecha) - new Date(b.fecha);
                case "fecha-desc": return new Date(b.fecha) - new Date(a.fecha);
                default: return 0;
            }
        });
        paginaActual = 1;
        renderizar();
    });

    // Filtros de categoría / estilo
    botonesFiltro.forEach(boton => {
        boton.addEventListener("click", () => {
            const f = boton.dataset.filter;
            if (filtrosActivos.has(f)) {
                filtrosActivos.delete(f);
                boton.classList.remove("activo");
            } else {
                filtrosActivos.add(f);
                boton.classList.add("activo");
            }
            aplicarFiltros();
        });
    });

    function aplicarFiltros() {
        if (filtrosActivos.size === 0) {
            filtrados = [...productos];
        } else {
            filtrados = productos.filter(p =>
                [...filtrosActivos].some(f => {
                    // comparar en minúsculas para evitar mismatch de mayúsculas
                    return p.tipo.toLowerCase() === f.toLowerCase()
                        || p.estilo.toLowerCase() === f.toLowerCase();
                })
            );
        }
        paginaActual = 1;
        renderizar();
    }
});

function addToCart(productId) {
    console.log("Añadir al carrito:", productId);
    alert(`Producto ${productId} añadido al carrito (simulación).`);
}
