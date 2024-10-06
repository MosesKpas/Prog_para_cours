from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Book, Order
from .tasks import send_welcome_email, send_order_notification

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        login(request, user)
        send_welcome_email.delay(user.email)
        return redirect('index')
    return render(request, 'register.html')

def order_book(request, book_id):
    book = Book.objects.get(id=book_id)
    order = Order.objects.create(user=request.user, book=book)
    send_order_notification.delay(request.user.email, book.title)
    return redirect('index')

def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})
