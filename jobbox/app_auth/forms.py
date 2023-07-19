from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _

from jobbox.app_auth.models import AppUser
from jobbox.common.models import Profile, ProfileHR

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LEN = 30

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        required=True,
    )

    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Repeat password, please"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'it works'

    def save(self, commit=True):
        user = super().save(commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            user=user,
        )

        print('=' * 20)
        print(f'Regular user {profile}')
        print('=' * 20)

        if commit:
            profile.save()

        return user

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )


class RegisterUserHRForm(auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LEN = 30
    COMPANY_NAME_MAX_LEN = 30

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        required=True,
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

        print('*' * 20)
        print(f'HR user {profile_hr}')
        print('*' * 20)

        if commit:
            profile_hr.save()

        return user_hr

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class EditUserHRForm(forms.Form):
    first_name = forms.CharField(
        max_length=RegisterUserHRForm.FIRST_NAME_MAX_LEN
    )

    company_name = forms.CharField(
        max_length=RegisterUserHRForm.COMPANY_NAME_MAX_LEN
    )


class EditUserForm(forms.Form):
    first_name = forms.CharField(
        max_length=RegisterUserForm.FIRST_NAME_MAX_LEN
    )

