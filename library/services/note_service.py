from ..models import Note


def create_note(user, book, data: dict):
    return Note.objects.create(
        user=user,
        book=book,
        note=data["text"]
    )
