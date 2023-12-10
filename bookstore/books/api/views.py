import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Libro
from books.api.serializers import LibroSerializer
from decouple import config

class LibrosView(APIView):
    def get(self, request, *args, **kwargs):
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
    def delete(self, request, libro_id, *args, **kwargs):
        try:
            book = Libro.objects.get(pk=libro_id)
            book.delete()
            return Response(status=status.HTTP_200_OK, data="El libro con id: " + str(libro_id) + " se eliminó correctamente!")
        except Libro.DoesNotExist:
            return Response({"error": "Libro no existe"}, status=status.HTTP_404_NOT_FOUND)
