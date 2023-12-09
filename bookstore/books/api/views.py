from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Libro
from books.api.serializers import LibroSerializer

class LibroBusquedaView(APIView):
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('titulo')
        subtitle = request.query_params.get('subtitulo')
        authors = request.query_params.get('autores')
        categories = request.query_params.get('categorias')
        publishing_date = request.query_params.get('fecha_publicacion')
        editor = request.query_params.get('editor')
        description = request.query_params.get('descripcion')
        source = request.query_params.get('fuente')


        queryset = Libro.objects.all()
        if title:
            queryset = queryset.filter(titulo__icontains=title)
        if subtitle:
            queryset = queryset.filter(subtitulo__icontains=subtitle)
        if authors:
            queryset = queryset.filter(autores__icontains=authors)
        if categories:
            queryset = queryset.filter(categorias__icontains=categories)
        if publishing_date:
            queryset = queryset.filter(fecha_publicacion=publishing_date)
        if editor:
            queryset = queryset.filter(editor__icontains=editor)
        if description:
            queryset = queryset.filter(descripcion__icontains=description)
        if source:
            queryset = queryset.filter(fuente__icontains=source)

        serializer = LibroSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
