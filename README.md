# FocusFlow — Organizador de Estudos

[![CI](https://github.com/seu-usuario/focusflow/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/focusflow/actions/workflows/ci.yml)

---

## Descrição do Problema

Muitos estudantes do ensino médio e superior enfrentam dificuldades para organizar sua rotina de estudos. A falta de planejamento leva à procrastinação, ao esquecimento de prazos, ao acúmulo de conteúdo e ao estresse antes de provas. Esse problema é especialmente acentuado em estudantes com dificuldades de atenção, rotina irregular ou excesso de disciplinas.

## Proposta de Solução

O **FocusFlow** é uma aplicação web simples, construída com Django, que permite ao estudante centralizar sua rotina de estudos em um único lugar. Com ela, é possível cadastrar matérias, criar tarefas com prazo e prioridade, montar uma grade semanal de sessões de estudo e acompanhar o progresso pelo dashboard.

## Público-alvo

Estudantes do ensino médio e superior com dificuldade de organizar a rotina de estudos, especialmente aqueles com múltiplas disciplinas, prazos simultâneos ou que precisam de apoio visual para planejar o tempo.

## Funcionalidades

- **Dashboard** com resumo de tarefas pendentes, concluídas e atrasadas
- **Matérias**: cadastrar, editar e remover matérias com cor personalizável
- **Tarefas**: criar tarefas com título, descrição, matéria, status, prioridade e prazo
- **Filtrar tarefas** por status, matéria ou prioridade
- **Marcar tarefa como concluída** com um clique
- **Detecção automática de tarefas atrasadas**
- **Grade Semanal**: montar o cronograma semanal de sessões de estudo por dia e horário
- **Cálculo automático** de duração de cada sessão

## Tecnologias Utilizadas

- Python 3.11
- Django 4.2
- SQLite (banco de dados embutido)
- pytest / pytest-django (testes automatizados)
- ruff (lint / análise estática)
- GitHub Actions (CI)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/focusflow.git
cd focusflow

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate
```

## Execução

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Testes

```bash
pytest
```

## Lint

```bash
ruff check .
```

## Versão

1.0.0

## Autor

Seu Nome — [github.com/seu-usuario](https://github.com/seu-usuario)

## Repositório

[github.com/seu-usuario/focusflow](https://github.com/seu-usuario/focusflow)

# Bootcamp-etapa-inicial
Aplicação web em Django para organizar rotinas de estudo, ajudando estudantes a gerenciar tarefas, acompanhar o progresso e manter consistência de forma simples e intuitiva.
