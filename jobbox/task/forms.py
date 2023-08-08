from django import forms

from jobbox.app_auth.models import AppUser
from jobbox.task.models import HRTask


class HRTaskForm(forms.ModelForm):
    class Meta:
        model = HRTask
        fields = ['task', 'status']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class HRTaskFormAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile_choices = [(user.pk, user) for user in AppUser.objects.all()]
        self.fields['user_id'].choices = profile_choices
        self.fields['user_id'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = HRTask
        fields = '__all__'
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
