from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Note, Book

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'avatar')
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
            'email': 'email',
            'avatar': 'Аватарка',
        }

    bio = forms.CharField(required=False, widget=forms.Textarea, label='О себе')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['username'].help_text = 'Обязательное. До 150 символов. Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = 'Пароль должен содержать минимум 8 символов и не быть слишком простым.'
        self.fields['password2'].help_text = 'Введите тот же пароль для подтверждения.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.bio = self.cleaned_data['bio']
        if commit:
            user.save()
        return user

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напиши заметку...'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'status', 'description', 'read_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3,
                                                'placeholder': 'Краткое описание книги...'}),
            'read_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):

        hide_fields = kwargs.pop('hide_fields', [])
        super().__init__(*args, **kwargs)
        for field_name in hide_fields:
            if field_name in self.fields:
                self.fields.pop(field_name)
