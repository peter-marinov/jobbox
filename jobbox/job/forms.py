from django import forms
from jobbox.job.models import Job, UploadCV
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInputCompanyLogo(ClearableFileInput):
    clear_checkbox_label = ''


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


class EditJobFrom(forms.ModelForm):
    company_logo = forms.ImageField(
        widget=CustomClearableFileInputCompanyLogo
    )
    class Meta:
        model = Job
        fields = ['title', 'company_logo', 'programming_language', 'salary', 'description']


class UploadCVForm(forms.ModelForm):
    class Meta:
        model = UploadCV
        fields = '__all__'
        widgets = {
            'job_id': forms.HiddenInput(),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

