from django.urls import path
from . import views

urlpatterns = [
    path("menu-items/", views.menu_items, name="menu-items"),
    path("menu-items/<int:id>/", views.single_item, name="single-item-view"),
    path("category/<int:pk>/" , views.category_detail, name='category-detail'),
    path("menu/", views.menu, name=""),
    path("welcome/", views.welcome,  name="")
]
