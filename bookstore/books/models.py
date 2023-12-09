from django.db import models

class Autor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    class Meta:
        db_table = "autores"


class Categoria(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=255)
    class Meta:
        db_table = "categorias"


class Libro(models.Model):
    id = models.SmallAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255)
    fecha_publicacion = models.DateField()
    editor = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=255, null=True)
    autores = models.ManyToManyField(Autor, related_name="libros", through="LibroAutor")
    categorias = models.ManyToManyField(Categoria, related_name="libros", through="LibroCategoria")
    class Meta:
        db_table = "libros"


class LibroAutor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, db_column="libro_id")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE,  db_column="autor_id")
    class Meta:
        db_table = "libros_autores"

class LibroCategoria(models.Model):
    id = models.SmallAutoField(primary_key=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE,  db_column="libro_id")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,  db_column="categoria_id")
    class Meta:
        db_table = "libros_categorias"