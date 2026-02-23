from django.urls import path
from .views import BookListAPIView, BookUpdateAPIView, NoteCreateAPIView, BookMarkReadAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view()),
    path("update_books/<int:pk>/", BookUpdateAPIView.as_view()),
    path("create_notes/", NoteCreateAPIView.as_view()),
    path("mark_read/", BookMarkReadAPIView.as_view()),
]
