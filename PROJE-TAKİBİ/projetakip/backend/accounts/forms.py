from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm

from .models import User


_input = {'class': 'form-control'}
_check = {'class': 'form-check-input'}


class StudentForm(forms.ModelForm):
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs=_input),
        required=False,
        help_text='Boş bırakılırsa mevcut şifre korunur.',
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'student_number', 'phone')
        widgets = {f: forms.TextInput(attrs=_input) for f in ('username', 'first_name', 'last_name', 'email', 'student_number', 'phone')}
        labels = {
            'username': 'Kullanıcı adı',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta',
            'student_number': 'Öğrenci no',
            'phone': 'Telefon',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Bu e-posta zaten kayıtlı.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-posta', widget=forms.EmailInput(attrs=_input))
    first_name = forms.CharField(required=True, label='Ad', widget=forms.TextInput(attrs=_input))
    last_name = forms.CharField(required=True, label='Soyad', widget=forms.TextInput(attrs=_input))
    role = forms.ChoiceField(
        choices=[(User.Role.TEACHER, 'Öğretmen'), (User.Role.STUDENT, 'Öğrenci')],
        label='Rol',
        widget=forms.Select(attrs=_input),
    )
    student_number = forms.CharField(required=False, label='Öğrenci no', widget=forms.TextInput(attrs=_input))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'student_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs=_input),
            'password1': forms.PasswordInput(attrs=_input),
            'password2': forms.PasswordInput(attrs=_input),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta zaten kayıtlı.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Kullanıcı adı veya e-posta', widget=forms.TextInput(attrs=_input))
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput(attrs=_input))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.filter(email=username).first()
            if user and user.check_password(password):
                self.user_cache = user
                return self.cleaned_data
        return super().clean()


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        return User.objects.filter(email__iexact=email, is_active=True)
