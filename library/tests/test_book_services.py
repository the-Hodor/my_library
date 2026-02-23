import pytest
from django.contrib.auth import get_user_model
from library.models import Book, Genre
from library.services.book_service import create_book, update_book, get_user_books

User = get_user_model()


@pytest.mark.django_db
def test_create_book_creates_book_for_user():
    user = User.objects.create_user(username="test", password="123")

    data = {
        "title": "Test book",
        "author": "Author",
        "status": "unread",
    }

    book = create_book(user, data)

    assert Book.objects.count() == 1
    assert book.user == user
    assert book.title == "Test book"


@pytest.mark.django_db
def test_update_book_updates_fields():
    user = User.objects.create_user(username="test", password="123")

    book = Book.objects.create(
        user=user,
        title="Old title",
        author="Old author",
        status="unread",
    )

    data = {
        "title": "New title",
        "status": "read",
    }

    updated_book = update_book(book, data)

    updated_book.refresh_from_db()

    assert updated_book.title == "New title"
    assert updated_book.status == "read"


pytestmark = pytest.mark.django_db


def test_get_user_books_returns_only_user_books():
    user1 = User.objects.create_user(username="u1")
    user2 = User.objects.create_user(username="u2")

    Book.objects.create(title="Book 1", user=user1)
    Book.objects.create(title="Book 2", user=user2)

    books = get_user_books(user1, {})

    assert books.count() == 1
    assert books.first().title == "Book 1"


def test_get_user_books_filters_by_status():
    user = User.objects.create_user(username="u1")

    Book.objects.create(title="Read book", user=user, status="read")
    Book.objects.create(title="Unread book", user=user, status="unread")

    books = get_user_books(user, {"status": "read"})

    assert books.count() == 1
    assert books.first().title == "Read book"


def test_get_user_books_filters_by_title():
    user = User.objects.create_user(username="u1")

    Book.objects.create(
        title="Harry Potter",
        author="Rowling",
        user=user,
    )
    Book.objects.create(
        title="Lord of the Rings",
        author="Tolkien",
        user=user,
    )

    books = get_user_books(user, {"title": "harry"})

    assert books.count() == 1
    assert books.first().title == "Harry Potter"


def test_get_user_books_filters_by_author():
    user = User.objects.create_user(username="u1")

    Book.objects.create(
        title="Harry Potter",
        author="Rowling",
        user=user,
    )
    Book.objects.create(
        title="Lord of the Rings",
        author="Tolkien",
        user=user,
    )

    books = get_user_books(user, {"author": "rowling"})

    assert books.count() == 1
    assert books.first().author == "Rowling"


@pytest.mark.django_db
def test_get_user_books_filters_by_genre():
    user = User.objects.create_user(username="u1")

    fantasy = Genre.objects.create(name="Fantasy")
    horror = Genre.objects.create(name="Horror")

    book1 = Book.objects.create(
        title="Harry Potter",
        author="Rowling",
        user=user,
    )
    book1.genres.add(fantasy)

    book2 = Book.objects.create(
        title="Dracula",
        author="Stoker",
        user=user,
    )
    book2.genres.add(horror)

    books = get_user_books(user, {"genre": "fantasy"})

    assert books.count() == 1
    assert books.first().title == "Harry Potter"

def test_get_user_books_ignores_invalid_status():
    user = User.objects.create_user(username="u1")

    Book.objects.create(title="Book 1", status="read", user=user)
    Book.objects.create(title="Book 2", status="unread", user=user)

    books = get_user_books(user, {"status": "abracadabra"})

    assert books.count() == 2

def test_get_user_books_genre_distinct():
    user = User.objects.create_user(username="u1")

    fantasy = Genre.objects.create(name="Fantasy")
    dark_fantasy = Genre.objects.create(name="Dark Fantasy")

    book = Book.objects.create(
        title="Book",
        author="Author",
        user=user,
    )
    book.genres.add(fantasy, dark_fantasy)

    books = get_user_books(user, {"genre": "fantasy"})

    assert books.count() == 1


def test_create_book_creates_book_for_user():
    user = User.objects.create_user(username="u1")

    data = {
        "title": "Dune",
        "author": "Frank Herbert",
        "status": "unread",
    }

    book = create_book(user, data)

    assert Book.objects.count() == 1
    assert book.user == user
    assert book.title == "Dune"
    assert book.author == "Frank Herbert"


def test_create_book_sets_genres():
    user = User.objects.create_user(username="u1")
    genre1 = Genre.objects.create(name="Fantasy")
    genre2 = Genre.objects.create(name="Sci-Fi")

    data = {
        "title": "Dune",
        "author": "Frank Herbert",
        "genres": [genre1, genre2],
    }

    book = create_book(user, data)

    assert book.genres.count() == 2
    assert genre1 in book.genres.all()
    assert genre2 in book.genres.all()


def test_update_book_updates_fields():
    user = User.objects.create_user(username="u1")
    book = Book.objects.create(
        title="Old title",
        author="Old author",
        status="unread",
        user=user,
    )

    data = {
        "title": "New title",
        "author": "New author",
        "status": "read",
    }

    updated = update_book(book, data)

    book.refresh_from_db()

    assert updated.id == book.id
    assert book.title == "New title"
    assert book.author == "New author"
    assert book.status == "read"


def test_update_book_updates_genres():
    user = User.objects.create_user(username="u1")
    genre1 = Genre.objects.create(name="Fantasy")
    genre2 = Genre.objects.create(name="Sci-Fi")
    genre3 = Genre.objects.create(name="Drama")

    book = Book.objects.create(title="Book", user=user)
    book.genres.set([genre1])

    data = {
        "genres": [genre2, genre3]
    }

    update_book(book, data)

    book.refresh_from_db()

    assert book.genres.count() == 2
    assert genre2 in book.genres.all()
    assert genre3 in book.genres.all()
    assert genre1 not in book.genres.all()

def test_get_user_books_filters_by_title():
    user = User.objects.create_user(username="u1")

    Book.objects.create(title="Harry Potter", user=user)
    Book.objects.create(title="Django Guide", user=user)

    books = get_user_books(user, {"title": "harry"})

    assert books.count() == 1
    assert books.first().title == "Harry Potter"


def test_get_user_books_returns_only_user_books():
    user1 = User.objects.create_user(username="u1")
    user2 = User.objects.create_user(username="u2")

    Book.objects.create(title="User1 book", user=user1)
    Book.objects.create(title="User2 book", user=user2)

    books = get_user_books(user1, {})

    assert books.count() == 1
    assert books.first().title == "User1 book"

def test_get_user_books_filter_by_genre_distinct():
    user = User.objects.create_user(username="u1")

    genre = Genre.objects.create(name="Fantasy")

    book = Book.objects.create(title="HP", user=user)
    book.genres.add(genre)

    books = get_user_books(user, {"genre": "fantasy"})

    assert books.count() == 1
