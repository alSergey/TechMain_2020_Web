from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.template.defaulttags import register
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.models import Question, Answer, VoteQuestion, VoteAnswer
from app.forms import SingInForm, SingUpForm, SettingsForm, \
    QuestionForm, AnswerForm, \
    VoteQuestionForm, VoteAnswerForm, CorrectForm


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def pagination(object_list, request, per_page=10):
    p = request.GET.get('page')
    paginator = Paginator(object_list, per_page)

    if p == 'last':
        return paginator.get_page(paginator.num_pages)

    return paginator.get_page(p)


def index(request):
    questions = pagination(Question.objects.new(), request)

    votes = {}
    if request.user.is_authenticated:
        votes = VoteQuestion.objects.reaction(qlist=list(questions.object_list.values_list('id', flat=True)),
                                              aid=request.user.profile)

    return render(request, 'index.html', {
        'votes': votes,
        'title': 'New questions',
        'questions': questions,
    })


def hot_questions(request):
    questions = pagination(Question.objects.hot(), request)

    votes = {}
    if request.user.is_authenticated:
        votes = VoteQuestion.objects.reaction(qlist=list(questions.object_list.values_list('id', flat=True)),
                                              aid=request.user.profile)

    return render(request, 'index.html', {
        "votes": votes,
        'title': 'Hot questions',
        'questions': questions,
    })


@login_required
def new_question(request):
    if request.method == 'POST':
        form = QuestionForm(data=request.POST, profile=request.user.profile)
        if form.is_valid():
            question = form.save()
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

    answers_votes = {}
    question_vote = {}
    if request.user.is_authenticated:
        answers_votes = VoteAnswer.objects.reaction(alist=list(answers.object_list.values_list('id', flat=True)),
                                                    aid=request.user.profile)

        question_vote = VoteQuestion.objects.reaction(qlist=[question.id, ],
                                                      aid=request.user.profile)

    if request.method == 'POST':
        form = AnswerForm(data=request.POST, profile=request.user.profile, question=question)
        if form.is_valid():
            form.save()
            # return redirect(reverse('question', kwargs={'id': id}) + '?page=last')
            return redirect(reverse('question', kwargs={'id': id}))

    else:
        form = AnswerForm(None, None)

    return render(request, 'question_page.html', {
        'title': f'Question {id}',
        'answers_votes': answers_votes,
        'votes': question_vote,
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
        form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect(reverse('settings'))

    else:
        user_data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        form = SettingsForm(initial=user_data)

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
        form = SingUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

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


@require_POST
@login_required
def vote(request):
    data = request.POST

    if data['vote'] == 'like':
        vote = True
    else:
        vote = False

    vote_data = {
        'author': request.user.profile,
        'state': vote,
        data['class']: data['id']
    }

    if data['class'] == 'question':
        form = VoteQuestionForm(data=vote_data, action=data['action'])
    else:
        form = VoteAnswerForm(data=vote_data, action=data['action'])

    if form.is_valid():
        form.save()

    if data['class'] == 'question':
        rating = Question.objects.get(id=data['id']).rating
    else:
        rating = Answer.objects.get(id=data['id']).rating

    return JsonResponse({'rating': rating})


@require_POST
@login_required
def correct(request):
    data = request.POST

    form = CorrectForm(data=data)
    if form.is_valid():
        answer = form.save()

    return JsonResponse({'correct': answer.is_correct})
