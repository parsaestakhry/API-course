from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.books, name="books"),
    path("book/<int:pk>/", views.BookView.as_view(), name="")
]
