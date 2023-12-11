import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Libro
from books.api.serializers import LibroSerializer
from decouple import config

class LibrosView(APIView):
    def get(self, request):
        title = request.query_params.get('titulo')
        subtitle = request.query_params.get('subtitulo')
        author = request.query_params.get('autor')
        category = request.query_params.get('categoria')
        publishing_date = request.query_params.get('fecha_publicacion')
        editor = request.query_params.get('editor')
        description = request.query_params.get('descripcion')
        source = request.query_params.get('fuente')

        queryset = Libro.objects.all()
        if title:
            queryset = queryset.filter(titulo__icontains=title)
        if subtitle:
            queryset = queryset.filter(subtitulo__icontains=subtitle)
        if author:
            queryset = queryset.filter(autores__icontains=author)
        if category:
            queryset = queryset.filter(categorias__icontains=category)
        if publishing_date:
            queryset = queryset.filter(fecha_publicacion=publishing_date)
        if editor:
            queryset = queryset.filter(editor__icontains=editor)
        if description:
            queryset = queryset.filter(descripcion__icontains=description)
        if source:
            queryset = queryset.filter(fuente__icontains=source)
        
        if not queryset.exists():
            google_books_results = self.llamar_google_books_api(request.query_params)
            return Response(data={"libros": google_books_results, "fuente": "google"}, status=status.HTTP_200_OK)

        serializer = LibroSerializer(queryset, many=True)
        return Response(data={"libros": serializer.data, "fuente": "interna"}, status=status.HTTP_200_OK)
    
    def llamar_google_books_api(self, filters):
        google_books_api_url = "https://www.googleapis.com/books/v1/volumes"
        api_key = config('GOOGLE_API_KEY')
        params = {}

        if 'titulo' in filters: params["q"] = filters.get('titulo')
        elif 'subtitulo' in filters: params["q"] = filters.get('subtitulo')
        elif 'autor' in filters: params["q"] = filters.get('autor')
        elif 'categoria' in filters: params["q"] = filters.get('categoria')
        elif 'fecha_publicacion' in filters: params["q"] = filters.get('fecha_publicacion')
        elif 'editor' in filters: params["q"] = filters.get('editor')
        elif 'descripcion' in filters: params["q"] = filters.get('descripcion')

        params['intitle'] = filters.get('titulo', '')
        params['inauthor'] = filters.get('autor', '')
        params['inpublisher'] = filters.get('editor', '')
        params['subject'] = filters.get('categoria', '')

        response = requests.get(google_books_api_url, params=params, headers={'key': api_key})
        response_data = response.json()

        books = []
        for item in response_data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            book_data = {
                'titulo': volume_info.get('title', ''),
                'subtitulo': volume_info.get('subtitle', ''),
                'autores': ",".join(volume_info.get('authors', [])),
                'categorias': ",".join(volume_info.get('categories', [])),
                'fecha_publicacion': volume_info.get('publishedDate', ''),
                'editor': volume_info.get('publisher', ''),
                'descripcion': volume_info.get('description', ''),
                'imagen': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'fuente': "google",
                'google_id': item.get('id', '')
            }
            books.append(book_data)

        return books

class LibroPorIdView(APIView):
    def delete(self, request, libro_id):
        try:
            book = Libro.objects.get(pk=libro_id)
            book.delete()
            return Response(status=status.HTTP_200_OK, data={"mensaje": "El libro con id: " + str(libro_id) + " se eliminó correctamente!"})
        except Libro.DoesNotExist:
            return Response(data={"error": "Libro no existe"}, status=status.HTTP_404_NOT_FOUND)

class LibroPorGoogleIdView(APIView):
    def post(self, request, google_id):
        book = Libro.objects.filter(google_id=google_id).first()
        if book is not None:
            return Response(data={"error": "Libro ya se encuentra registrado con ese id de google"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = self.llamar_google_api_por_id(google_id)

        if book is None:
            return Response(data={"error": "Id de google inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        Libro.objects.create(**book)
        return Response(status=status.HTTP_201_CREATED, data={"mensaje": "El libro con id de google: " + google_id + " se agregó correctamente!"})
    
    def llamar_google_api_por_id(self, id):
        google_books_api_url = "https://www.googleapis.com/books/v1/volumes/" + id
        api_key = config('GOOGLE_API_KEY')

        response = requests.get(google_books_api_url, headers={'key': api_key})
        response_data = response.json()
        if "error" in response_data:
            return None

        volume_info = response_data.get('volumeInfo', {})
        book_data = {
            'titulo': volume_info.get('title', ''),
            'subtitulo': volume_info.get('subtitle', ''),
            'autores': ",".join(volume_info.get('authors', [])),
            'categorias': ",".join(volume_info.get('categories', [])),
            'fecha_publicacion': volume_info.get('publishedDate', ''),
            'editor': volume_info.get('publisher', ''),
            'descripcion': volume_info.get('description', ''),
            'imagen': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'fuente': "google",
            'google_id': response_data.get('id', '')
        }
        return book_data

class LibroExternalApiView(APIView):
    def get(self, request):
        open_library_api_url = "https://openlibrary.org/search.json"

        title = request.query_params.get('titulo')
        subtitle = request.query_params.get('subtitulo')
        author = request.query_params.get('autor')
        category = request.query_params.get('categoria')
        publishing_date = request.query_params.get('fecha_publicacion')
        editor = request.query_params.get('editor')
        description = request.query_params.get('descripcion')
        params = {}
        
        if title is None and subtitle is None and author is None and category is None and publishing_date is None and editor is None and description is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Es necesario al menos uno de los siguientes parametros: titulo, subitulo, autor, categoria, fecha_publicacion, editor, descripcion"})

        if title:
            params["q"] = title
        elif subtitle:
            params["q"] = subtitle
        elif author:
            params["q"] = author
        elif category:
            params["q"] = category
        elif publishing_date:
            params["q"] = publishing_date
        elif editor:
            params["q"] = editor
        elif description:
            params["q"] = description
        
        params['title'] = title
        params['subtitle'] = subtitle
        params['author_name'] = author
        params['subject'] = category
        params['publisher'] = editor
        params['first_publish_year'] = publishing_date

        response = requests.get(open_library_api_url, params=params)
        response_data = response.json()
        
        external_books = []
        for doc in response_data.get('docs', []):
            if 'ratings_average' in doc and (doc.get('ratings_count') and float(doc['ratings_count']) > 50):
                external_book = {
                    'titulo': doc.get('title', ''),
                    'autor': doc.get('author_name', []),
                    'fecha_publicacion': doc.get('first_publish_year', ''),
                    'categoria': doc.get('subject', []),  
                    'editor': doc.get('publisher', [''])[0],
                    'rating (1-5)': doc.get('ratings_average', ''),
                    'numero de ratings': doc.get('ratings_count', '')
                }
                external_books.append(external_book)
        
        sorted_books = sorted(external_books, key=lambda x: float(x['rating (1-5)']), reverse=True)

        return Response(status=status.HTTP_200_OK, data={"libros": sorted_books, "fuente": "externa"})