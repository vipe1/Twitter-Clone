from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('display_name', 'email')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class AccountEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountEditForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=150)
    display_name = forms.CharField(max_length=64)
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        account = CustomUser.objects.exclude(pk=self.user.pk).filter(email=email).first()
        if account is None:
            return email
        raise forms.ValidationError('Given email is already in use')

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('''Username can't contain spaces''')
        account = CustomUser.objects.exclude(pk=self.user.pk).filter(username=username).first()
        if account is None:
            return username
        raise forms.ValidationError('Given username is already in use')

    def save(self):
        account = self.user
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.display_name = self.cleaned_data['display_name']
        account.save()
        return account