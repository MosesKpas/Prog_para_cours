from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('order/<int:book_id>/', views.order_book, name='order_book'),
]
