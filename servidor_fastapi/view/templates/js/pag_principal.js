document.addEventListener("DOMContentLoaded", function () {
    // 1) Carga el JSON desde /static/No_log/pag_principal/productos.json
    fetch("json/productos.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al cargar productos.json");
            }
            return response.json();
        })
        .then(data => {
            // Mostrar producto destacado
            mostrarProductoDestacado(data.destacado);

            // Mostrar productos en los carruseles
            mostrarProductos("productos-destacados", data.destacados, "carrusel-destacados");
            mostrarProductos("productos-venta", data.venta, "carrusel-venta");
        })
        .catch(error => console.error("Error al cargar productos:", error));
});

// Función para mostrar el producto destacado
function mostrarProductoDestacado(producto) {
    if (!producto) return;

    // 2) Enlaza a la página de detalle con ruta absoluta
    document.getElementById("destacado-link").href =
        "/No_log/detalle-productos_No_Logeado/descripcion_Disco_No_Logueado.html";

    // 3) La imagen sigue apuntando al recurso dinámico
    document.getElementById("destacado-imagen").src = producto.imagen;
    document.getElementById("destacado-imagen").alt = producto.nombre;

    document.getElementById("destacado-nombre").href = producto.link;
    document.getElementById("destacado-nombre").textContent = producto.nombre;
}

// Función para mostrar productos en los carruseles
function mostrarProductos(contenedorId, productos, carruselId) {
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor || !productos) return;

    contenedor.innerHTML = ""; // Limpiar antes de agregar

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.classList.add("splide__slide");

        // 4) Usa rutas absolutas para la página de detalle
        const detalleHref = "/No_log/detalle-productos_No_Logeado/descripcion_Disco_No_Logueado.html";

        li.innerHTML = `
            <a href="${detalleHref}">
                <img src="${producto.imagen}" alt="${producto.nombre}">
            </a>
            <h3>
              <a href="${producto.link}">
                ${producto.nombre}
              </a>
            </h3>
        `;
        contenedor.appendChild(li);
    });

    // Inicializar Splide
    new Splide(`#${carruselId}`, {
        type: "loop",
        perPage: 3,
        perMove: 1,
        gap: "1rem",
        autoplay: true,
        interval: 3000,
        arrows: true,
        pagination: false
    }).mount();
}