# Di dalam core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Komentar

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Wajib. Format: nama@domain.com')
    class Meta:
        model = User
        fields = ('username', 'email')

class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ('isi',)
        widgets = {
            'isi': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tulis komentar Anda...'}),
        }
        labels = {
            'isi': '' # Hapus label default
        }