from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MateriaForm, SessaoEstudoForm, TarefaForm
from .models import DIAS_SEMANA, Materia, SessaoEstudo, Tarefa


def dashboard(request):
    total_tarefas = Tarefa.objects.count()
    tarefas_pendentes = Tarefa.objects.filter(status="pendente").count()
    tarefas_concluidas = Tarefa.objects.filter(status="concluido").count()
    tarefas_atrasadas = [t for t in Tarefa.objects.filter(status__in=["pendente", "em_andamento"]) if t.esta_atrasada()]
    tarefas_recentes = Tarefa.objects.exclude(status="concluido").order_by("-criado_em")[:5]
    materias = Materia.objects.all()

    # Organizar grade semanal
    ordem_dias = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
    nomes_dias = dict(DIAS_SEMANA)
    grade = []
    for dia in ordem_dias:
        sessoes = SessaoEstudo.objects.filter(dia_semana=dia).select_related("materia")
        grade.append({"codigo": dia, "nome": nomes_dias[dia], "sessoes": sessoes})

    context = {
        "total_tarefas": total_tarefas,
        "tarefas_pendentes": tarefas_pendentes,
        "tarefas_concluidas": tarefas_concluidas,
        "total_atrasadas": len(tarefas_atrasadas),
        "tarefas_recentes": tarefas_recentes,
        "materias": materias,
        "grade": grade,
    }
    return render(request, "estudos/dashboard.html", context)


# ── Matérias ──────────────────────────────────────────────────────────────────

def materia_lista(request):
    materias = Materia.objects.all()
    return render(request, "estudos/materia_lista.html", {"materias": materias})


def materia_criar(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matéria criada com sucesso!")
            return redirect("materia_lista")
    else:
        form = MateriaForm()
    return render(request, "estudos/materia_form.html", {"form": form, "titulo": "Nova Matéria"})


def materia_editar(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == "POST":
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, "Matéria atualizada!")
            return redirect("materia_lista")
    else:
        form = MateriaForm(instance=materia)
    return render(request, "estudos/materia_form.html", {"form": form, "titulo": "Editar Matéria"})


def materia_excluir(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == "POST":
        materia.delete()
        messages.success(request, "Matéria removida.")
        return redirect("materia_lista")
    return render(request, "estudos/confirmar_exclusao.html", {"objeto": materia, "tipo": "matéria"})


# ── Tarefas ───────────────────────────────────────────────────────────────────

def tarefa_lista(request):
    status_filtro = request.GET.get("status", "")
    materia_filtro = request.GET.get("materia", "")
    prioridade_filtro = request.GET.get("prioridade", "")

    tarefas = Tarefa.objects.select_related("materia")
    if status_filtro:
        tarefas = tarefas.filter(status=status_filtro)
    if materia_filtro:
        tarefas = tarefas.filter(materia__id=materia_filtro)
    if prioridade_filtro:
        tarefas = tarefas.filter(prioridade=prioridade_filtro)

    materias = Materia.objects.all()
    context = {
        "tarefas": tarefas,
        "materias": materias,
        "status_filtro": status_filtro,
        "materia_filtro": materia_filtro,
        "prioridade_filtro": prioridade_filtro,
    }
    return render(request, "estudos/tarefa_lista.html", context)


def tarefa_criar(request):
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect("tarefa_lista")
    else:
        form = TarefaForm()
    return render(request, "estudos/tarefa_form.html", {"form": form, "titulo": "Nova Tarefa"})


def tarefa_editar(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa atualizada!")
            return redirect("tarefa_lista")
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, "estudos/tarefa_form.html", {"form": form, "titulo": "Editar Tarefa"})


def tarefa_excluir(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        tarefa.delete()
        messages.success(request, "Tarefa removida.")
        return redirect("tarefa_lista")
    return render(request, "estudos/confirmar_exclusao.html", {"objeto": tarefa, "tipo": "tarefa"})


def tarefa_concluir(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    tarefa.status = "concluido"
    tarefa.save()
    messages.success(request, f'"{tarefa.titulo}" marcada como concluída!')
    return redirect("tarefa_lista")


# ── Sessões de Estudo ─────────────────────────────────────────────────────────

def sessao_lista(request):
    ordem_dias = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
    nomes_dias = dict(DIAS_SEMANA)
    grade = []
    for dia in ordem_dias:
        sessoes = SessaoEstudo.objects.filter(dia_semana=dia).select_related("materia")
        grade.append({"codigo": dia, "nome": nomes_dias[dia], "sessoes": sessoes})
    return render(request, "estudos/sessao_lista.html", {"grade": grade})


def sessao_criar(request):
    if request.method == "POST":
        form = SessaoEstudoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sessão de estudo adicionada!")
            return redirect("sessao_lista")
    else:
        form = SessaoEstudoForm()
    return render(request, "estudos/sessao_form.html", {"form": form, "titulo": "Nova Sessão"})


def sessao_editar(request, pk):
    sessao = get_object_or_404(SessaoEstudo, pk=pk)
    if request.method == "POST":
        form = SessaoEstudoForm(request.POST, instance=sessao)
        if form.is_valid():
            form.save()
            messages.success(request, "Sessão atualizada!")
            return redirect("sessao_lista")
    else:
        form = SessaoEstudoForm(instance=sessao)
    return render(request, "estudos/sessao_form.html", {"form": form, "titulo": "Editar Sessão"})


def sessao_excluir(request, pk):
    sessao = get_object_or_404(SessaoEstudo, pk=pk)
    if request.method == "POST":
        sessao.delete()
        messages.success(request, "Sessão removida.")
        return redirect("sessao_lista")
    return render(request, "estudos/confirmar_exclusao.html", {"objeto": sessao, "tipo": "sessão de estudo"})
