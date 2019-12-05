from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def handler404(request, exception):
    return render(None, 'home.html')


def handler500(request):
    return render(None, 'home.html')








