import pytest
from django.contrib.auth import get_user_model
from library.models import Book, Note
from library.services.note_service import create_note

User = get_user_model()

@pytest.mark.django_db
def test_create_note():
    user = User.objects.create_user(username="u1")

    book = Book.objects.create(
        title="Test book",
        user=user,
    )

    note = create_note(
        user,
        book,
        {"text": "My first note"}
    )

    assert Note.objects.count() == 1
    assert note.note == "My first note"
    assert note.book == book
    assert note.user == user


@pytest.mark.django_db
def test_note_belongs_to_user():
    user = User.objects.create_user(username="u1")
    book = Book.objects.create(title="HP", user=user)

    note = create_note(
        user=user,
        book=book,
        data={"text": "hello"}
    )

    assert note.user == user
