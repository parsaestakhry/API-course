from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    #path("menu-items/", views.MenuItemsViewSet.as_view({'get' : 'list'}), name="menu-items"),
    #path("menu-items/<int:pk>/", views.MenuItemsViewSet.as_view({'get' : 'retrieve'}), name="single-item-view"),
    path("category/<int:pk>/" , views.category_detail, name='category-detail'),
    path("menu/", views.menu, name=""),
    path("welcome/", views.welcome,  name=""),
    path("secret/", views.secret, name="secret"),
    path('api-token-auth/' ,obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle/', views.throttle_check),
    path('throttle-auth/', views.throttle_check_auth),
    path('menu-items/', views.MenuItemViewSet.as_view({'get' : 'list'})),
    path("menu-item/<int:pk>", views.MenuItemViewSet.as_view({'get' : 'retrieve'}), name=""),
    path("groups/manager/users/", views.managers)
]
