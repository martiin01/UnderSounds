document.addEventListener("DOMContentLoaded", () => {
  const contenedor = document.getElementById("contenedor-productos-usuario");
  const filtroOrden = document.getElementById("ordenar-usuario");
  const pagContainer = document.getElementById("paginacion-usuario");
  const porPagina = 5; // Número de productos por página

  // Obtener los productos desde los nodos del DOM
  const nodos = Array.from(contenedor.querySelectorAll(".producto"));
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

  let filtrados = [...productos]; // Productos filtrados (inicialmente todos)
  let paginaActual = 1; // Página actual

  renderizar(); // Renderizar la primera vez

  // Función para renderizar los productos en la página actual
  function renderizar() {
    contenedor.innerHTML = ""; // Limpiar el contenedor
    const inicio = (paginaActual - 1) * porPagina;
    const slice = filtrados.slice(inicio, inicio + porPagina); // Obtener los productos de la página actual

    slice.forEach(p => {
      const div = document.createElement("div");
      div.className = "producto";
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
        <button class="btn-add-cart" onclick="addToCart('${p.id}')">
          Añadir al carrito
        </button>
      `;
      contenedor.appendChild(div);
    });

    renderizarPaginacion(); // Actualizar la paginación
  }

  // Función para renderizar los botones de paginación
  function renderizarPaginacion() {
    pagContainer.innerHTML = ""; // Limpiar el contenedor de paginación
    const totalPaginas = Math.ceil(filtrados.length / porPagina); // Calcular el número total de páginas

    for (let i = 1; i <= totalPaginas; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      btn.className = "pagina-btn" + (i === paginaActual ? " activo" : "");
      btn.addEventListener("click", () => {
        paginaActual = i; // Cambiar a la página seleccionada
        renderizar(); // Renderizar la nueva página
      });
      pagContainer.appendChild(btn);
    }
  }

  // Evento para ordenar los productos
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
    paginaActual = 1; // Reiniciar a la primera página
    renderizar();
  });
});

// Función para añadir al carrito
function addToCart(productId) {
  console.log("Añadir al carrito:", productId);
  alert(`Producto ${productId} añadido al carrito (simulación).`);
}