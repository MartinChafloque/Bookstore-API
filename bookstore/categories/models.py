from django.db import models

class Categoria(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=255)
    class Meta:
        db_table = "categorias"
