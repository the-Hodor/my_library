from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Genre

@receiver(post_migrate)
def create_default_genres(sender, **kwargs):
    default_genres = ['Фантастика', 'Детектив', 'Роман', 'Научная литература']
    for name in default_genres:
        Genre.objects.get_or_create(name=name)