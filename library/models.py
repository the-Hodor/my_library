from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class MyUser(AbstractUser):

    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField("Аватарка", upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)

    def __str__(self):
        return self.username


class Book(models.Model):

    STATUS_CHOICES = [
        ('read', 'Прочитана'),
        ('unread', 'Не прочитана'),
        ('reading', 'В процессе'),
    ]

    title = models.CharField("Название", max_length=30)
    author = models.CharField("Автор", max_length=20)
    genres = models.ManyToManyField('Genre', related_name='book', verbose_name="Жанры")
    read_date = models.DateField("Дата прочтения",blank=True, null=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='unread')
    description = models.TextField("Описание", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return self.title

class Genre(models.Model):

    name = models.CharField("Название", max_length=20)

    def __str__(self):
        return self.name


class Note(models.Model):
    note = models.TextField("Текст заметки")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f'Заметка к {self.book.title}'



