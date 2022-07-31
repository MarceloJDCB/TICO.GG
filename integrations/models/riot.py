from django.db import models

class BaseApiCall(models.Model):
    api = models.CharField(verbose_name="Nome da API", max_length=100)
    created = models.DateTimeField("data de criação do registro", auto_now_add=True)
    modified = models.DateTimeField("data de alteração do registro", auto_now=True)
    method = models.CharField(verbose_name="Tipo de chamada", max_length=200)
    url = models.CharField(verbose_name="Url da Api", max_length=200)
    data = models.TextField(verbose_name="Conteúdo enviado")
    success = models.BooleanField(verbose_name="Chamada bem sucedida")
    response_status_code = models.IntegerField("Status code", null=True)
    response_data = models.TextField("Resposta da api")
