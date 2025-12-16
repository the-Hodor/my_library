from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import MyUserCreationForm, NoteForm, BookForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Book, Genre, Note, MyUser
from django.core.paginator import Paginator
# Create your views here.
@login_required
def main(request):
    books = Book.objects.filter(user=request.user).prefetch_related("genres")

    # фильтр по статусу
    status = request.GET.get("status")
    if status in ["read", "unread", "reading"]:
        books = books.filter(status=status)

    # фильтр по названию
    title = request.GET.get("title")
    if title:
        books = books.filter(title__icontains=title)

    # фильтр по автору
    author = request.GET.get("author")
    if author:
        books = books.filter(author__icontains=author)

    # фильтр по жанру (по имени, а не id)
    genre = request.GET.get("genre")
    if genre:
        books = books.filter(genres__name__icontains=genre).distinct()

    paginator = Paginator(books, 36)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    genres = Genre.objects.all()


    if request.GET.get("page") == None:
        page_number = '1'
    return render(request, "library/main.html", {
        "books": page_obj,
        "genres": genres,
        "page_number": page_number,
        "page_obj": page_obj,
        "previous_page_number": page_obj.number-1 if page_obj.has_previous else None,
        "next_page_number": page_obj.number+1 if page_obj.has_next else None,
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
            note = form.save(commit=False)
            note.book = book
            note.user = request.user
            note.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = NoteForm()

    return render(request, "library/book_detail.html", {
        "book": book,
        "notes": notes,
        "form": form,
        })


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            form.save_m2m()
            return redirect('main')
    else:
        form = BookForm(hide_fields=['read_date'])
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Добавить книгу'})


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Редактировать книгу'})
