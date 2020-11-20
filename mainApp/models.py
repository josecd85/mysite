from django.db import models
from django.utils import timezone

# Create your models here.
class Alertas(models.Model):
    idAlert = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=25)
    descrip = models.CharField(max_length=100)
    estado = models.CharField(max_length=1)
    falta = models.DateTimeField(default=timezone.now)
    ffin = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return str(self.idAlert)+"-"+self.titulo

class Informe001(models.Model):
    anio = models.IntegerField()
    mes = models.IntegerField()
    cemptitu = models.IntegerField()
    segmento = models.CharField(max_length=50)
    importe = models.DecimalField(decimal_places=3, max_digits=13)

    def __str__(self):
        return str(self.anio)+"-"+str(self.mes)+"-"+str(self.cemptitu)+"-"+self.segmento+"-"+str(self.importe)
    