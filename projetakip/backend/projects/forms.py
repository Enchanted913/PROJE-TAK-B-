from django import forms

from accounts.models import User

from .models import Project, ProjectGrade, Task

_input = {'class': 'form-control'}


class ProjectForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.STUDENT),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Öğrenciler',
    )

    class Meta:
        model = Project
        fields = ('title', 'description', 'students')
        widgets = {
            'title': forms.TextInput(attrs=_input),
            'description': forms.Textarea(attrs={**_input, 'rows': 3}),
        }
        labels = {
            'title': 'Proje adı',
            'description': 'Açıklama',
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Proje adı en az 3 karakter olmalı.')
        return title


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'order')
        widgets = {
            'title': forms.TextInput(attrs=_input),
            'description': forms.Textarea(attrs={**_input, 'rows': 2}),
            'order': forms.NumberInput(attrs=_input),
        }
        labels = {
            'title': 'Görev adı',
            'description': 'Açıklama',
            'due_date': 'Son tarih',
            'order': 'Sıra',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = ProjectGrade
        fields = ('score', 'note')
        widgets = {
            'score': forms.NumberInput(attrs=_input),
            'note': forms.Textarea(attrs={**_input, 'rows': 2}),
        }
        labels = {
            'score': 'Puan (0-100)',
            'note': 'Öğretmen notu',
        }

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 100:
            raise forms.ValidationError('Puan 0-100 arasında olmalı.')
        return score
