from django.urls import path
from . import views

urlpatterns = [
    path('', views.twit_list, name="twit_list"),
    path('create/', views.twit_create, name="twit_create"),
    path('<int:twit_id>/edit/', views.twit_edit, name="twit_edit"),
    path('<int:twit_id>/delete/', views.twit_delete, name="twit_delete"),
    path('search/', views.search_twit, name="search_twit"),
    path('register/', views.register, name="register"),
] 
