from django import forms
from .models import Submission, Task


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'rows': 10}),
        }
        


class TaskForm(forms.ModelForm):
    name = forms.CharField(label='Название')
    description = forms.CharField(label='Описание',widget=forms.Textarea(attrs={'rows': 10}))
    input = forms.CharField(label='Тест№1. Ввод',)
    output = forms.CharField(label='Тест№1. Вывод',)
    input1 = forms.CharField(label='Тест№2. Ввод',)
    output1 = forms.CharField(label='Тест№2. Вывод',)
    input2 = forms.CharField(label='Тест№3. Ввод',)
    output2 = forms.CharField(label='Тест№3. Вывод')
    
    class Meta:
       model = Task 
       fields = ['name', 'description', 'input', 'output','input1', 'output1','input2', 'output2']
       