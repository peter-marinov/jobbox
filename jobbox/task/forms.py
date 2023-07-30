from django import forms

from jobbox.task.models import HRTask


class HRTaskForm(forms.ModelForm):
    class Meta:
        model = HRTask
        fields = ['task', 'status']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }