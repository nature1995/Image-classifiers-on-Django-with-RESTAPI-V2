from django.shortcuts import render,  render_to_response


def home(request):
    return render(request, 'home.html')


def page_not_found(request):
    return render_to_response('home.html')


def page_error(request):
    return render_to_response('home.html')








