from django import forms

from jobbox.common.models import ContactUs


class ContactUsFrom(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = ContactUs
        fields = '__all__'