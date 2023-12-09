from rest_framework import serializers
from books.models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'subtitulo', 'autores', 'categorias', 'fecha_publicacion', 'editor', 'descripcion', 'imagen', 'fuente', 'google_id',]
