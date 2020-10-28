from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def new_question(request):
    return render(request, 'new_question_page.html', {})


def question(request):
    return render(request, 'question_page.html', {})


def tag(request):
    return render(request, 'tag_page.html', {})


def settings(request):
    return render(request, 'settings_page.html', {})


def sing_in(request):
    return render(request, 'sing_in_page.html', {})


def sing_up(request):
    return render(request, 'sing_up_page.html', {})
