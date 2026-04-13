from django.db import models

DIAS_SEMANA = [
    ("seg", "Segunda-feira"),
    ("ter", "Terça-feira"),
    ("qua", "Quarta-feira"),
    ("qui", "Quinta-feira"),
    ("sex", "Sexta-feira"),
    ("sab", "Sábado"),
    ("dom", "Domingo"),
]

STATUS_CHOICES = [
    ("pendente", "Pendente"),
    ("em_andamento", "Em andamento"),
    ("concluido", "Concluído"),
]

PRIORIDADE_CHOICES = [
    ("baixa", "Baixa"),
    ("media", "Média"),
    ("alta", "Alta"),
]


class Materia(models.Model):
    nome = models.CharField(max_length=100)
    cor = models.CharField(max_length=7, default="#6366f1")  # hex color
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Matéria"
        verbose_name_plural = "Matérias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    materia = models.ForeignKey(
        Materia, on_delete=models.SET_NULL, null=True, blank=True, related_name="tarefas"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default="media")
    prazo = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo

    def esta_atrasada(self):
        from django.utils import timezone

        if self.prazo and self.status != "concluido":
            return self.prazo < timezone.now().date()
        return False


class SessaoEstudo(models.Model):
    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="sessoes"
    )
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    descricao = models.CharField(max_length=200, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sessão de Estudo"
        verbose_name_plural = "Sessões de Estudo"
        ordering = ["dia_semana", "hora_inicio"]

    def __str__(self):
        return f"{self.materia.nome} - {self.get_dia_semana_display()} {self.hora_inicio}"

    def duracao_minutos(self):
        from datetime import date, datetime

        inicio = datetime.combine(date.today(), self.hora_inicio)
        fim = datetime.combine(date.today(), self.hora_fim)
        delta = fim - inicio
        return int(delta.total_seconds() / 60)
