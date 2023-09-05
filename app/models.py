from django.db import models


# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=120)


class Tarefa(models.Model):
    name = models.CharField(max_length=120)
    categoria = models.ManyToManyField(Categoria, related_name="categoria")
    data_entrega = models.DateTimeField(blank=True, null=True)
    finalizada = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
