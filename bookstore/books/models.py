from django.db import models


class Libro(models.Model):
    id = models.SmallAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255)
    autores = models.CharField(max_length=255)
    categorias = models.CharField(max_length=255)
    fecha_publicacion = models.DateField()
    editor = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.TextField(null=True)
    fuente = models.CharField(max_length=255)
    google_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "libros"