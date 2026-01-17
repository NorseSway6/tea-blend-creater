from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import MyUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_(' Почта'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )
    
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Придумайте имя пользователя')
        })
    )
    
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите пароль')
        })
    )
    
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Повторите пароль')
        })
    )
    
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Пользователь с таким email уже существует'))
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Имя пользователя или Email'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите имя пользователя или email')
        })
    )
    
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите пароль')
        })
    )


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('Имя'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label=_('Почта'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = MyUser
        fields = ('first_name', 'email')