from django import forms

from .models import Materia, SessaoEstudo, Tarefa


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ["nome", "cor"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ex: Matemática"}),
            "cor": forms.TextInput(attrs={"type": "color", "class": "form-color"}),
        }
        labels = {
            "nome": "Nome da Matéria",
            "cor": "Cor",
        }


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "materia", "status", "prioridade", "prazo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-input", "placeholder": "Título da tarefa"}),
            "descricao": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "Descrição (opcional)"}),
            "materia": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "prioridade": forms.Select(attrs={"class": "form-select"}),
            "prazo": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
        }
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "materia": "Matéria",
            "status": "Status",
            "prioridade": "Prioridade",
            "prazo": "Prazo",
        }


class SessaoEstudoForm(forms.ModelForm):
    class Meta:
        model = SessaoEstudo
        fields = ["materia", "dia_semana", "hora_inicio", "hora_fim", "descricao"]
        widgets = {
            "materia": forms.Select(attrs={"class": "form-select"}),
            "dia_semana": forms.Select(attrs={"class": "form-select"}),
            "hora_inicio": forms.TimeInput(attrs={"class": "form-input", "type": "time"}),
            "hora_fim": forms.TimeInput(attrs={"class": "form-input", "type": "time"}),
            "descricao": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ex: Revisão de fórmulas"}),
        }
        labels = {
            "materia": "Matéria",
            "dia_semana": "Dia da Semana",
            "hora_inicio": "Hora de Início",
            "hora_fim": "Hora de Fim",
            "descricao": "Descrição",
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")
        if hora_inicio and hora_fim and hora_fim <= hora_inicio:
            raise forms.ValidationError("A hora de fim deve ser posterior à hora de início.")
        return cleaned_data
