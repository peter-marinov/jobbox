from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms as auth_forms

from jobbox.common.models import ProfileHR
from jobbox.common.validators import check_if_only_letters

UserModel = get_user_model()


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class CustomClearableFileInputProfilePicture(forms.ClearableFileInput):
    # template_name = 'custom_clearable_file_input.html'
    pass


class RegisterUserHRForm(auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LEN = ProfileHR.FIRST_NAME_MAX_LEN
    COMPANY_NAME_MAX_LEN = ProfileHR.COMPANY_NAME_MAX_LEN

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        strip=False,
    )

    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        strip=False,
    )

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[check_if_only_letters],
    )

    company_name = forms.CharField(
            max_length=COMPANY_NAME_MAX_LEN,
            widget=forms.TextInput(attrs={'class': 'form-control'})
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
    class Meta:
        model = ProfileHR
        exclude = ['user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': CustomClearableFileInputProfilePicture(attrs={
                'class': 'form-control',
                'clear_checkbox_label': None
            }),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # profile_picture = forms.ImageField(
    #     widget=CustomClearableFileInputProfilePicture
    # )
    #
    # class Meta:
    #     model = ProfileHR
    #     exclude = ['user']
