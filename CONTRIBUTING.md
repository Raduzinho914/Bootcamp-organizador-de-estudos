# Contribuindo com o FocusFlow

Obrigado pelo interesse em contribuir! Siga as orientações abaixo.

## Como contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Faça suas alterações e commit: `git commit -m "feat: descrição da mudança"`
4. Envie para o seu fork: `git push origin feature/minha-feature`
5. Abra um Pull Request para a branch `main`

## Padrões de código

- Use `ruff check .` para verificar o estilo antes de commitar
- Escreva testes para novas funcionalidades
- Siga o padrão de mensagens de commit (feat, fix, docs, test, refactor)

## Rodando localmente

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
