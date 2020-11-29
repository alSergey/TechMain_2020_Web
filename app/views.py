from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect, reverse
from app.models import Question, Answer, Profile
from app.forms import SingInForm, SingUpForm, QuestionForm, AnswerForm, ProfileForm


def pagination(object_list, request, per_page=10):
    p = request.GET.get('page')
    paginator = Paginator(object_list, per_page)

    if p == 'last':
        return paginator.get_page(paginator.num_pages)

    return paginator.get_page(p)


def index(request):
    questions = pagination(Question.objects.new(), request)

    return render(request, 'index.html', {
        'title': 'New questions',
        'questions': questions,
    })


def hot_questions(request):
    questions = pagination(Question.objects.hot(), request)

    return render(request, 'index.html', {
        'title': 'Hot questions',
        'questions': questions,
    })


@login_required
def new_question(request):
    if request.method == 'POST':
        form = QuestionForm(profile=request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            Profile.objects.filter(id=question.author_id).update(count=F('count') + 1)
            return redirect(reverse('question', kwargs={'id': question.id}))

    else:
        form = QuestionForm(None)

    return render(request, 'new_question_page.html', {
        'title': 'New question',
        'form': form
    })


def question(request, id):
    last_id = Question.objects.latest('id').pk
    if id > last_id:
        id = last_id

    question = get_object_or_404(Question, id=id)
    answers = pagination(Answer.objects.answers(id), request, per_page=3)

    if request.method == 'POST':
        form = AnswerForm(profile=request.user.profile, question=question, data=request.POST)
        if form.is_valid():
            answer = form.save()
            Profile.objects.filter(id=answer.author_id).update(count=F('count') + 1)
            return redirect(reverse('question', kwargs={'id': id}) + '?page=last')

    else:
        form = AnswerForm(None, None)

    return render(request, 'question_page.html', {
        'title': f'Question {id}',
        'question': question,
        'answers': answers,
        'form': form
    })


def tag(request, tag):
    questions = pagination(Question.objects.tags(tag=tag), request)

    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'questions': questions,
    })


@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.FILES.get('avatar'):
                profile = Profile.objects.get(user_id=request.user.pk)
                profile.avatar = request.FILES['avatar']
                profile.save()

            return redirect(reverse('settings'))

    else:
        user_data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        form = ProfileForm(initial=user_data)

    return render(request, 'settings_page.html', {
        'title': 'Settings',
        'form': form
    })


def sing_in(request):
    if request.method == 'POST':
        next_page = request.session.pop('next_page', '/')
        form = SingInForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(next_page)

    else:
        form = SingInForm()
        if request.GET.get('next') is not None:
            request.session['next_page'] = request.GET.get('next')

    return render(request, 'sing_in_page.html', {
        'title': 'Sing In',
        'form': form
    })


def sing_up(request):
    if request.method == 'POST':
        next_page = request.session.pop('next_page', '/')
        form = SingUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if request.FILES.get('avatar'):
                Profile.objects.create(user_id=user.pk, avatar=request.FILES['avatar'])
            else:
                Profile.objects.create(user_id=user.pk)

            auth_data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password1'],
            }

            user = auth.authenticate(request, **auth_data)
            if user is not None:
                auth.login(request, user)
                return redirect(next_page)

    else:
        form = SingUpForm()
        if request.GET.get('next') is not None:
            request.session['next_page'] = request.GET.get('next')

    return render(request, 'sing_up_page.html', {
        'title': 'Sing Up',
        'form': form
    })


def logout(request):
    auth.logout(request)

    return redirect(request.GET.get('next', '/'))
