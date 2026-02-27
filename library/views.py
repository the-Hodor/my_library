from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .forms import MyUserCreationForm, NoteForm, BookForm
from .models import Book, Genre, Note, MyUser
from .services.book_service import create_book, update_book, get_user_books
from .services.note_service import create_note


@login_required
def main(request):
    books = get_user_books(request.user, request.GET)

    paginator = Paginator(books, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    genres = Genre.objects.all()

    return render(request, "library/main.html", {
        "books": page_obj,
        "genres": genres,
        "page_obj": page_obj,
    })

class RegisterView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'library/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        return super().form_valid(form)

@login_required
def profile_view(request):
    profile = get_object_or_404(MyUser, username=request.user)
    return render(request, "library/profile.html", {"profile": profile})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    notes = Note.objects.filter(book=book, user=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            create_note(request.user, book, form.cleaned_data)
            return redirect('book_detail', pk=pk)
    else:
        form = NoteForm()

    return render(request, "library/book_detail.html", {
        "book": book,
        "notes": notes,
        "form": form,
    })

@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            create_book(request.user, form.cleaned_data)
            return redirect("main")
    else:
        form = BookForm(hide_fields=['read_date'])

    return render(request, 'library/book_form.html', {'form': form, 'title': 'Добавить книгу'})

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            update_book(book, form.cleaned_data)
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {'form': form, 'title': 'Редактировать книгу'})
