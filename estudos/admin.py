from django.contrib import admin

from .models import Materia, SessaoEstudo, Tarefa

admin.site.register(Materia)
admin.site.register(Tarefa)
admin.site.register(SessaoEstudo)
