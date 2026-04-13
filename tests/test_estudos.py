import pytest
from datetime import date, time, timedelta
from django.utils import timezone

from estudos.models import Materia, Tarefa, SessaoEstudo
from estudos.forms import TarefaForm, MateriaForm, SessaoEstudoForm


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def materia(db):
    return Materia.objects.create(nome="Matemática", cor="#6366f1")


@pytest.fixture
def materia_secundaria(db):
    return Materia.objects.create(nome="Português", cor="#f5a524")


# ── Modelo: Materia ───────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_materia_criada_com_sucesso():
    materia = Materia.objects.create(nome="Física", cor="#22d3a0")
    assert materia.pk is not None
    assert str(materia) == "Física"


@pytest.mark.django_db
def test_materia_cor_padrao():
    materia = Materia.objects.create(nome="Química")
    assert materia.cor == "#6366f1"


@pytest.mark.django_db
def test_materia_str(materia):
    assert str(materia) == "Matemática"


# ── Modelo: Tarefa ────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_tarefa_criada_com_sucesso(materia):
    tarefa = Tarefa.objects.create(titulo="Estudar integrais", materia=materia)
    assert tarefa.pk is not None
    assert tarefa.status == "pendente"
    assert tarefa.prioridade == "media"


@pytest.mark.django_db
def test_tarefa_str(materia):
    tarefa = Tarefa.objects.create(titulo="Lista de exercícios", materia=materia)
    assert str(tarefa) == "Lista de exercícios"


@pytest.mark.django_db
def test_tarefa_sem_materia():
    """Tarefa pode ser criada sem matéria vinculada."""
    tarefa = Tarefa.objects.create(titulo="Tarefa geral")
    assert tarefa.materia is None
    assert tarefa.pk is not None


@pytest.mark.django_db
def test_tarefa_nao_atrasada_sem_prazo(materia):
    tarefa = Tarefa.objects.create(titulo="Sem prazo", materia=materia)
    assert tarefa.esta_atrasada() is False


@pytest.mark.django_db
def test_tarefa_nao_atrasada_prazo_futuro(materia):
    prazo_futuro = date.today() + timedelta(days=7)
    tarefa = Tarefa.objects.create(titulo="Com prazo futuro", materia=materia, prazo=prazo_futuro)
    assert tarefa.esta_atrasada() is False


@pytest.mark.django_db
def test_tarefa_atrasada_prazo_passado(materia):
    prazo_passado = date.today() - timedelta(days=3)
    tarefa = Tarefa.objects.create(
        titulo="Atrasada", materia=materia, prazo=prazo_passado, status="pendente"
    )
    assert tarefa.esta_atrasada() is True


@pytest.mark.django_db
def test_tarefa_concluida_nao_considerada_atrasada(materia):
    prazo_passado = date.today() - timedelta(days=5)
    tarefa = Tarefa.objects.create(
        titulo="Concluída", materia=materia, prazo=prazo_passado, status="concluido"
    )
    assert tarefa.esta_atrasada() is False


@pytest.mark.django_db
def test_tarefa_status_choices(materia):
    for status in ["pendente", "em_andamento", "concluido"]:
        tarefa = Tarefa.objects.create(titulo=f"Tarefa {status}", status=status)
        assert tarefa.status == status


@pytest.mark.django_db
def test_tarefa_prioridade_alta(materia):
    tarefa = Tarefa.objects.create(titulo="Urgente", materia=materia, prioridade="alta")
    assert tarefa.prioridade == "alta"


# ── Modelo: SessaoEstudo ──────────────────────────────────────────────────────

@pytest.mark.django_db
def test_sessao_criada_com_sucesso(materia):
    sessao = SessaoEstudo.objects.create(
        materia=materia,
        dia_semana="seg",
        hora_inicio=time(8, 0),
        hora_fim=time(10, 0),
    )
    assert sessao.pk is not None


@pytest.mark.django_db
def test_sessao_duracao_minutos(materia):
    sessao = SessaoEstudo.objects.create(
        materia=materia,
        dia_semana="ter",
        hora_inicio=time(14, 0),
        hora_fim=time(16, 30),
    )
    assert sessao.duracao_minutos() == 150


@pytest.mark.django_db
def test_sessao_str(materia):
    sessao = SessaoEstudo.objects.create(
        materia=materia,
        dia_semana="qua",
        hora_inicio=time(9, 0),
        hora_fim=time(11, 0),
    )
    assert "Matemática" in str(sessao)
    assert "Quarta" in str(sessao)


# ── Formulários ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_tarefa_form_valido(materia):
    form = TarefaForm(data={
        "titulo": "Resolver exercícios do cap. 3",
        "descricao": "",
        "materia": materia.pk,
        "status": "pendente",
        "prioridade": "alta",
        "prazo": "",
    })
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_tarefa_form_titulo_vazio():
    form = TarefaForm(data={
        "titulo": "",
        "status": "pendente",
        "prioridade": "media",
    })
    assert not form.is_valid()
    assert "titulo" in form.errors


@pytest.mark.django_db
def test_materia_form_valido():
    form = MateriaForm(data={"nome": "Biologia", "cor": "#22d3a0"})
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_materia_form_nome_vazio():
    form = MateriaForm(data={"nome": "", "cor": "#6366f1"})
    assert not form.is_valid()
    assert "nome" in form.errors


@pytest.mark.django_db
def test_sessao_form_hora_fim_antes_inicio(materia):
    form = SessaoEstudoForm(data={
        "materia": materia.pk,
        "dia_semana": "seg",
        "hora_inicio": "10:00",
        "hora_fim": "09:00",
        "descricao": "",
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_sessao_form_valido(materia):
    form = SessaoEstudoForm(data={
        "materia": materia.pk,
        "dia_semana": "sex",
        "hora_inicio": "08:00",
        "hora_fim": "10:00",
        "descricao": "Revisão",
    })
    assert form.is_valid(), form.errors


# ── Views ─────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_dashboard_acessivel(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_tarefa_lista_acessivel(client):
    response = client.get("/tarefas/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_materia_lista_acessivel(client):
    response = client.get("/materias/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_sessao_lista_acessivel(client):
    response = client.get("/sessoes/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_criar_tarefa_via_post(client, materia):
    response = client.post("/tarefas/nova/", {
        "titulo": "Tarefa criada via teste",
        "descricao": "",
        "materia": materia.pk,
        "status": "pendente",
        "prioridade": "media",
        "prazo": "",
    })
    assert response.status_code == 302
    assert Tarefa.objects.filter(titulo="Tarefa criada via teste").exists()


@pytest.mark.django_db
def test_criar_materia_via_post(client):
    response = client.post("/materias/nova/", {
        "nome": "História",
        "cor": "#f5a524",
    })
    assert response.status_code == 302
    assert Materia.objects.filter(nome="História").exists()


@pytest.mark.django_db
def test_concluir_tarefa(client, materia):
    tarefa = Tarefa.objects.create(titulo="Para concluir", materia=materia, status="pendente")
    response = client.post(f"/tarefas/{tarefa.pk}/concluir/")
    assert response.status_code == 302
    tarefa.refresh_from_db()
    assert tarefa.status == "concluido"


@pytest.mark.django_db
def test_excluir_tarefa(client, materia):
    tarefa = Tarefa.objects.create(titulo="Para excluir", materia=materia)
    response = client.post(f"/tarefas/{tarefa.pk}/excluir/")
    assert response.status_code == 302
    assert not Tarefa.objects.filter(pk=tarefa.pk).exists()


@pytest.mark.django_db
def test_excluir_materia(client, materia):
    pk = materia.pk
    response = client.post(f"/materias/{pk}/excluir/")
    assert response.status_code == 302
    assert not Materia.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_filtro_tarefas_por_status(client, materia):
    Tarefa.objects.create(titulo="Pendente", materia=materia, status="pendente")
    Tarefa.objects.create(titulo="Concluida", materia=materia, status="concluido")
    response = client.get("/tarefas/?status=pendente")
    assert response.status_code == 200
    assert b"Pendente" in response.content
