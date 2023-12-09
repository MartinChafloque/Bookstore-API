from django.db import models

class Autor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    class Meta:
        db_table = "autores"
