
from django.shortcuts import render
from posts.models import Post


def HomePage(request):
    data = Post.objects.all()
    return render(request, 'home.html', {'data': data})


def AboutPage(request):
    return render(request, 'about.html')


def ContactPage(request):
    return render(request, 'contact.html')
