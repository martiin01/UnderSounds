document.addEventListener('DOMContentLoaded', function() {
    fetch('../footer.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al cargar el footer');
        }
        return response.text();
      })
      .then(html => {
        const footerContainer = document.getElementById('footer-placeholder');
        if (footerContainer) {
          footerContainer.innerHTML = html;
        } else {
          console.error('No se encontró el elemento contenedor del footer.');
        }
      })
      .catch(error => console.error('Error al insertar el footer:', error));
  });