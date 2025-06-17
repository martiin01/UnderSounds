# UnderSound - Plataforma E-Commerce de Música

## Descripción General

Bienvenido a UnderSound, una aplicación web diseñada para descubrir, comprar y vender productos musicales. Esta plataforma sirve como un mercado que conecta a los fans de la música con los artistas, ofreciendo una variedad de artículos que incluyen CDs, discos de vinilo, casetes y merchandising de artistas.

La aplicación está construida utilizando Python con el framework FastAPI para el backend, y HTML, CSS y JavaScript estándar para la interfaz frontend. Aprovecha Firebase para la autenticación de usuarios y Stripe para el procesamiento seguro de pagos.

## Roles de Usuario

La plataforma está diseñada para tres tipos distintos de usuarios, cada uno con capacidades específicas:

1.  **No Logueado:**
    *   Navegar por el catálogo completo de productos ([`pag_principal_NoLog.html`](servidor_fastapi/view/templates/pag_principal_NoLog.html), [`pag_explorar_NoLog.html`](servidor_fastapi/view/templates/pag_explorar_NoLog.html)).
    *   Ver información detallada sobre productos específicos ([`descripcion_Disco_NoLog.html`](servidor_fastapi/view/templates/descripcion_Disco_NoLog.html)).
    *   Añadir artículos a un carrito de compras temporal basado en el almacenamiento local ([`carrito1_NoLog.html`](servidor_fastapi/view/templates/carrito1_NoLog.html)).
    *   Comprar artículos directamente ("Comprar Ahora") o finalizar la compra del carrito completo como invitado usando Stripe ([`pago_NoLog.html`](servidor_fastapi/view/templates/pago_NoLog.html)).
    *   Debe registrarse o iniciar sesión para acceder a funciones persistentes.

2.  **Usuario/Fan (Usuario Logueado):**
    *   Todas las capacidades de un usuario no logueado.
    *   Carrito de compras persistente vinculado a su cuenta, gestionado por el backend ([`carrito1_Usuario.html`](servidor_fastapi/view/templates/carrito1_Usuario.html), [`controller/carrito.py`](servidor_fastapi/controller/carrito.py)).
    *   Inicio de sesión seguro a través de Firebase Authentication ([`loginLog.html`](servidor_fastapi/view/templates/loginLog.html)).
    *   Gestión del perfil de usuario ([`controller/perfil.py`](servidor_fastapi/controller/perfil.py)).
    *   Proceso de pago seguro utilizando Stripe, vinculado a su cuenta ([`pago_Usuario.html`](servidor_fastapi/view/templates/pago_Usuario.html)).
    *   Registro disponible a través de [`registro.html`](servidor_fastapi/view/templates/registro.html).

3.  **Artista:**
    *   Todas las capacidades de un usuario logueado (Fan).
    *   Capacidad para subir y gestionar sus propios productos musicales (CDs, Vinilos, Casetes) a través de [`subir_ProdMusicales.html`](servidor_fastapi/view/templates/subir_ProdMusicales.html).
    *   Capacidad para subir y gestionar su merchandising (ej. camisetas) a través de [`subir_Merch.html`](servidor_fastapi/view/templates/subir_Merch.html).
    *   Ver y gestionar sus productos listados a través de interfaces dedicadas ([`prodMusicales.html`](servidor_fastapi/view/templates/prodMusicales.html), [`tus_merch.html`](servidor_fastapi/view/templates/tus_merch.html)).
    *   Acceso a un perfil/panel de control específico para artistas ([`perfil_Artista.html`](servidor_fastapi/view/templates/perfil_Artista.html)).
    *   Registro disponible a través de [`registro_artista.html`](servidor_fastapi/view/templates/registro_artista.html).
    *   Proceso de pago seguro utilizando Stripe ([`pago_Artista.html`](servidor_fastapi/view/templates/pago_Artista.html)).

## Tecnologías Utilizadas

*   **Backend:** Python 3, FastAPI ([`main.py`](servidor_fastapi/main.py))
*   **Frontend:** HTML5 ([`view/templates/`](servidor_fastapi/view/templates/)), CSS3 ([`view/templates/css/`](servidor_fastapi/view/templates/css/)), JavaScript (ES6+) ([`view/templates/js/`](servidor_fastapi/view/templates/js/))
*   **Base de Datos:** SQLite (definida en [`model/dao/schema.sql`](servidor_fastapi/model/dao/schema.sql), datos iniciales en [`model/dao/initial_data.json`](servidor_fastapi/model/dao/initial_data.json))
*   **Autenticación:** Firebase Authentication
*   **Pagos:** Stripe API

## Arquitectura

El proyecto sigue patrones de diseño de software establecidos para asegurar la mantenibilidad, escalabilidad y separación de responsabilidades:

*   **Modelo-Vista-Controlador (MVC):**
    *   **Modelo:** Representa los datos y la lógica de negocio. Esto incluye la lógica de interacción con la base de datos encapsulada dentro de las clases DAO ([`model/dao/implementations/`](servidor_fastapi/model/dao/implementations/)) y el esquema de la base de datos ([`model/dao/schema.sql`](servidor_fastapi/model/dao/schema.sql)).
    *   **Vista:** Maneja la capa de presentación. Consiste en plantillas HTML Jinja2 ([`view/templates/`](servidor_fastapi/view/templates/)), hojas de estilo CSS ([`view/templates/css/`](servidor_fastapi/view/templates/css/)) y JavaScript del lado del cliente ([`view/templates/js/`](servidor_fastapi/view/templates/js/)).
    *   **Controlador:** Actúa como intermediario entre el Modelo y la Vista. Los endpoints de FastAPI definidos en el directorio [`controller/`](servidor_fastapi/controller/) ([`productos.py`](servidor_fastapi/controller/productos.py), [`carrito.py`](servidor_fastapi/controller/carrito.py), [`pago.py`](servidor_fastapi/controller/pago.py), [`auth.py`](servidor_fastapi/controller/auth.py)) manejan las solicitudes HTTP entrantes, interactúan con el Modelo (DAOs) para obtener o manipular datos, y seleccionan la Vista (plantilla) apropiada para renderizar la respuesta.

*   **Data Access Object (DAO):**
    *   Este patrón abstrae el mecanismo de persistencia de datos subyacente (base de datos SQLite). Clases como [`CartDAO`](servidor_fastapi/model/dao/implementations/cart_dao.py) y [`UserDAO`](servidor_fastapi/model/dao/implementations/user_dao.py) proporcionan una API limpia para operaciones CRUD (Crear, Leer, Actualizar, Borrar) sin exponer detalles específicos de la base de datos a los controladores.

*   **Data Transfer Object (DTO):**
    *   Aunque no se muestra explícitamente en todas las capas, FastAPI se basa en gran medida en modelos Pydantic que a menudo sirven como DTOs. Estos objetos se utilizan para definir la estructura de los datos que se transfieren entre diferentes partes de la aplicación, como cuerpos de solicitud, modelos de respuesta y datos pasados entre controladores y servicios/DAOs. Esto asegura la consistencia de los datos y proporciona validación automática.

## Integración de Servicios Externos

*   **Firebase Authentication:**
    *   Maneja el registro ([`registro.html`](servidor_fastapi/view/templates/registro.html), [`registro_artista.html`](servidor_fastapi/view/templates/registro_artista.html)) e inicio de sesión ([`loginLog.html`](servidor_fastapi/view/templates/loginLog.html)) de usuarios de forma segura utilizando correo electrónico y contraseña.
    *   El frontend interactúa directamente con el SDK de Firebase para las acciones de autenticación.
    *   El backend ([`controller/auth_api_impl.py`](servidor_fastapi/controller/auth_api_impl.py), [`controller/auth.py`](servidor_fastapi/controller/auth.py)) probablemente verifica los tokens de ID de Firebase para autenticar las solicitudes API y gestiona la sincronización de datos del usuario con la base de datos local.

*   **Stripe API:**
    *   Gestiona todo el flujo de pago de forma segura.
    *   El frontend utiliza Stripe Elements ([`pago_NoLog.html`](servidor_fastapi/view/templates/pago_NoLog.html), [`pago_Usuario.html`](servidor_fastapi/view/templates/pago_Usuario.html), [`pago_Artista.html`](servidor_fastapi/view/templates/pago_Artista.html)) para recopilar los detalles de la tarjeta directamente en los servidores de Stripe, mejorando la seguridad (cumplimiento PCI).
    *   El backend ([`controller/pago.py`](servidor_fastapi/controller/pago.py)) interactúa con la API de Stripe para crear Payment Intents (que representan una transacción de pago), confirmar pagos y manejar webhooks (aunque los webhooks podrían no estar completamente implementados según el código proporcionado). Calcula los montos para pagos de invitados y se basa en el carrito del usuario para los pagos de usuarios registrados.

## Configuración

*(Placeholder: Añade aquí instrucciones sobre cómo configurar el proyecto localmente, incluyendo dependencias, variables de entorno para Firebase/Stripe, inicialización de la base de datos, etc.)*

# Comandos de configuración de ejemplo
pip install -r requirements.txt
# Configurar el archivo .env con las claves API
# Ejecutar migraciones/inicialización de la base de datos
uvicorn main:app --reload


