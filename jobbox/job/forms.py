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
                'hr': forms.HiddenInput()
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
            'job_id': forms.HiddenInput()
        }

