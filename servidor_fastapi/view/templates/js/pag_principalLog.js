document.addEventListener("DOMContentLoaded", function () {
    fetch("../json/productos.json")
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

    document.getElementById("destacado-link").href = producto.link;
    document.getElementById("destacado-imagen").src = producto.imagen;
    document.getElementById("destacado-imagen").alt = producto.nombre;
    document.getElementById("destacado-nombre").href = producto.link;
    document.getElementById("destacado-nombre").textContent = producto.nombre;
}

// Función para mostrar productos en los carruseles
function mostrarProductos(contenedorId, productos, carruselId) {
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor || !productos) return;

    contenedor.innerHTML = ""; // Limpiar antes de agregar productos

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.classList.add("splide__slide");
        li.innerHTML = `
            <a href="${producto.link}">
                <img src="${producto.imagen}" alt="${producto.nombre}">
            </a>
            <h3><a href="${producto.link}">${producto.nombre}</a></h3>
        `;
        contenedor.appendChild(li);
    });

    // Inicializar Splide en el carrusel correspondiente
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
