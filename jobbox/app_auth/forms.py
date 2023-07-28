from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ClearableFileInput

from jobbox.app_auth.models import AppUser
from jobbox.common.models import ProfileHR

UserModel = get_user_model()


class CustomClearableFileInputProfilePicture(ClearableFileInput):
    clear_checkbox_label = ''


class RegisterUserHRForm(auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LEN = 30
    COMPANY_NAME_MAX_LEN = 30

    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Repeat password, please"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'it works'

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LEN
    )

    company_name = forms.CharField(
            max_length=15,
        )

    def save(self, commit=True):
        user_hr = super().save(commit)
        profile_hr = ProfileHR(
            first_name=self.cleaned_data['first_name'],
            company_name=self.cleaned_data['company_name'],
            user=user_hr,
        )

        if commit:
            profile_hr.save()

        return user_hr

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)




class EditUserHRForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        widget=CustomClearableFileInputProfilePicture
    )

    class Meta:
        model = ProfileHR
        exclude = ['user']
