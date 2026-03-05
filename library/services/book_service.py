from ..models import Book
from django.shortcuts import get_object_or_404
from django.db.models.functions import Lower



def get_user_book(user, book_id):
    return get_object_or_404(Book, id=book_id, user=user)

def get_user_books(user, filters: dict):
    books = Book.objects.filter(user=user).prefetch_related("genres")

    status = filters.get("status")
    if status in ["read", "unread", "reading"]:
        books = books.filter(status=status)

    title = filters.get("title")
    if title:
        books = books.filter(title__iregex=title)

    author = filters.get("author")
    if author:
        books = books.filter(author__iregex=author)

    genre = filters.get("genre")
    if genre:
        books = books.filter(genres__name__iregex=genre).distinct()

    return books


def create_book(user, data):
    genres = data.pop("genres", [])

    book = Book.objects.create(
        user=user,
        **data
    )

    if genres:
        book.genres.set(genres)

    return book



def update_book(book, data):
    genres = data.pop("genres", None)

    for field, value in data.items():
        setattr(book, field, value)

    book.save()
    if genres is not None:
        book.genres.set(genres)

    return book



def mark_book_as_read(book):
    book.status = "read"
    book.save()
    return book

