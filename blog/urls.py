from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

]


