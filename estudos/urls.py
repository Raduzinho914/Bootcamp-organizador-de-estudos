from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Matérias
    path("materias/", views.materia_lista, name="materia_lista"),
    path("materias/nova/", views.materia_criar, name="materia_criar"),
    path("materias/<int:pk>/editar/", views.materia_editar, name="materia_editar"),
    path("materias/<int:pk>/excluir/", views.materia_excluir, name="materia_excluir"),
    # Tarefas
    path("tarefas/", views.tarefa_lista, name="tarefa_lista"),
    path("tarefas/nova/", views.tarefa_criar, name="tarefa_criar"),
    path("tarefas/<int:pk>/editar/", views.tarefa_editar, name="tarefa_editar"),
    path("tarefas/<int:pk>/excluir/", views.tarefa_excluir, name="tarefa_excluir"),
    path("tarefas/<int:pk>/concluir/", views.tarefa_concluir, name="tarefa_concluir"),
    # Sessões de Estudo
    path("sessoes/", views.sessao_lista, name="sessao_lista"),
    path("sessoes/nova/", views.sessao_criar, name="sessao_criar"),
    path("sessoes/<int:pk>/editar/", views.sessao_editar, name="sessao_editar"),
    path("sessoes/<int:pk>/excluir/", views.sessao_excluir, name="sessao_excluir"),
]
