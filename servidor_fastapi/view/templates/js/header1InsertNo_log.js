document.addEventListener('DOMContentLoaded', function() {
    fetch('header1.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al cargar el header');
        }
        return response.text();
      })
      .then(html => {
        const headerContainer = document.getElementById('header');
        if (headerContainer) {
          headerContainer.innerHTML = html;
        } else {
          console.error('No se encontró el elemento contenedor del header.');
        }
      })
      .catch(error => console.error('Error al insertar el header:', error));
  });