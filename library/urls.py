from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('main/', views.main, name='main'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path("profile/", views.profile_view, name="profile"),
    path("book/detail/<int:pk>/", views.book_detail, name="book_detail"),
    path('book/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('add/book/', views.add_book, name='add_book'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
