from django import forms
from django.contrib.auth import get_user_model

from jobbox.app_auth.models import AppUser
from jobbox.job.models import Job, UploadCV

UserModel = get_user_model()

class CreateJobFrom(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
                'hr': forms.HiddenInput(),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'programming_language': forms.TextInput(attrs={'class': 'form-control'}),
                'salary': forms.NumberInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            }


class CreateEditJobFromAdmin(CreateJobFrom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile_choices = [(user.pk, user) for user in AppUser.objects.all()]
        self.fields['hr'].choices = profile_choices
        self.fields['hr'].widget.attrs['class'] = 'form-control'

    class Meta(CreateJobFrom.Meta):
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'programming_language': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            }



class EditJobFrom(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_logo', 'programming_language', 'salary', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'programming_language': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class UploadCVForm(forms.ModelForm):
    class Meta:
        model = UploadCV
        fields = '__all__'
        widgets = {
            'job_id': forms.HiddenInput(),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

