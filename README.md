# Bookstore-API
API web que permite administrar una pequeña biblioteca. El servicio tiene un repositorio interno y además se alimenta de 2 APIs públicas:
- Google Books API: https://developers.google.com/books/docs/v1/using?hl=es-419
- Open Library API: https://openlibrary.org/developers/api

El API web fue implementado en Django con una base de datos en MySQL.

Requerimientos técnicos:
Para utilizar este API web se necesita los siguientes requerimientos:
- Python 3.11.X
- MySQL Sever 8.2.0
- MySQL Workbench 8.0.34

Para utilizar el entorno de dependencias que se utilizó para el API web es necesario tener instalado localmente pipenv. 
- Para esto correr el comando: `pip install pipenv`.
- Dirigirse a una terminal en el directorio raíz de este proyecto y correr el comando: `pipenv install`
- Finalmente, correr el comando: `pip shell` para entrar al entorno virtual con las dependencias necesarias.

Para comenzar el servidor del API web, correr el comando: `python bookstore/manage.py runserver`.

ENDPOINTS
- `api/v1/libros/`: Método GET. Busqueda de los libros en la base de datos o en la api de google. Este endpoint hace uso de query parameters para filtrar resultados, estos son: `titulo`, `subtitulo`, `autor`, `categoria`, `fecha_publicacion (el formato debe seguir YYYY-MM-DD)`, `editor`, `descripcion`, `fuente`.

- `api/v1/libros/<int:libro_id>`: Método DELETE. Elimina un libro de la base de datos. Este endpoint hace uso de un path parameter llamado `libro_id` que hace referencia al primary key de la base de datos.

- `api/v1/libros/<str:google_id>`: Método POST. Registra un libro en la base de datos con información recuperada de la API de google. Este endpoint hace uso de un path parameter llamado `google_id` que hace referencia al key principal de la API de google que puede ser recuperada con el anterior endpoint en el campo `google_id`.

- `api/v1/libros/external/`: Método GET. Busqueda de los libros en la api Open Library con el fin de ver libros organizados por su rating. Este endpoint hace uso de query parameters para filtrar resultados, estos son: `titulo`, `subtitulo`, `autor`, `categoria`, `fecha_publicacion (el formato debe seguir YYYY)`, `editor`.
