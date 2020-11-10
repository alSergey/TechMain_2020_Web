from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Question, Answer

user = True


def pagination(object_list, request, per_page=10):
    p = request.GET.get('page')
    paginator = Paginator(object_list, per_page)

    try:
        content = paginator.page(p)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return content


def index(request):
    return render(request, 'index.html', {
        'title': 'New questions',
        'user_login': user,
        'questions': pagination(Question.objects.new(), request),
    })


def hot_questions(request):
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'user_login': user,
        'questions': pagination(Question.objects.hot(), request),
    })


def new_question(request):
    return render(request, 'new_question_page.html', {
        'title': 'New question',
        'user_login': user,
    })


def question(request, id):
    return render(request, 'question_page.html', {
        'title': f'Question {id}',
        'user_login': user,
        'questions': Question.objects.question(id),
        'answers': pagination(Answer.objects.answers(id), request, per_page=3),
    })


def tag(request, tag):
    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'user_login': user,
        'questions': pagination(Question.objects.tags(tag=tag), request),
    })


def settings(request):
    return render(request, 'settings_page.html', {
        'title': 'Settings',
        'user_login': True,
    })


def sing_in(request):
    return render(request, 'sing_in_page.html', {
        'title': 'Sing In',
        'user_login': False,
    })


def sing_up(request):
    return render(request, 'sing_up_page.html', {
        'title': 'Sing Up',
        'user_login': False,
    })
