from django.urls import path
from . import views

urlpatterns = [
    path("menu-items/", views.MenuItemsViewSet.as_view({'get' : 'list'}), name="menu-items"),
    path("menu-items/<int:pk>/", views.MenuItemsViewSet.as_view({'get' : 'retrieve'}), name="single-item-view"),
    path("category/<int:pk>/" , views.category_detail, name='category-detail'),
    path("menu/", views.menu, name=""),
    path("welcome/", views.welcome,  name=""),
]
