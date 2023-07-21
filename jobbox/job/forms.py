from django import forms
from jobbox.job.models import Job


class CreateJobFrom(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
                'hr': forms.HiddenInput()
            }


class EditJobFrom(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_logo', 'programming_language', 'salary', 'description']




