from django import forms
from jobbox.job.models import Job, UploadCV


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

