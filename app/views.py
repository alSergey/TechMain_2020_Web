from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

tags_users = {
    'tags': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8'],
    'users': ['mr greeman', 'dr house', 'bender', 'queen victoria', 'pupkin'],
}

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


questions = []
for i in range(1, 20):
    questions.append({
        'title': 'Title ' + str(i),
        'author': 'author ' + str(i),
        'date': 'date ' + str(i),
        'id': i,
        'answer': str(i),
        'tags': ['tag' + str(i), 'tag' + str(i + 1)],
        'answers': [i + 1, i + 2],
        'rating': str(i),
        'text': 'text ' + str(i)
    })

questions.append(({
    'title': 'Title ' + str(21),
    'author': 'author ' + str(21),
    'date': 'date ' + str(21),
    'id': 21,
    'answer': str(21),
    'tags': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9', 'tag10', 'tag11', 'tag12', 'tag13',
             'tag14', 'tag15', 'tag16', 'tag17', 'tag18'],
    'answers': [18, 19, 20, 22, 23, 24, 25],
    'rating': str(21),
    'text': 'text ' + str(21)
}))

questions.append(({
    'title': 'Title ' + str(22),
    'author': 'author ' + str(22),
    'date': 'date ' + str(22),
    'id': 22,
    'answer': str(22),
    'tags': ['tag1'],
    'answers': [23],
    'rating': str(22),
    'text': 'text ' + str(22)
}))

questions.append(({
    'title': 'Title ' + str(23),
    'author': 'author ' + str(23),
    'date': 'date ' + str(23),
    'id': 23,
    'answer': str(23),
    'tags': ['tag1'],
    'answers': [24],
    'rating': str(23),
    'text': 'text ' + str(23)
}))

questions.append(({
    'title': 'Title ' + str(24),
    'author': 'author ' + str(24),
    'date': 'date ' + str(24),
    'id': 24,
    'answer': str(24),
    'tags': ['tag2'],
    'answers': [25],
    'rating': str(24),
    'text': 'text ' + str(24)
}))

questions.append(({
    'title': 'Title ' + str(25),
    'author': 'author ' + str(25),
    'date': 'date ' + str(25),
    'id': 25,
    'answer': str(25),
    'tags': ['tag3'],
    'answers': [26],
    'rating': str(25),
    'text': 'text ' + str(25)
}))


def findTag(val, tag1):
    content = []
    for q in val:
        for ctag in q['tags']:
            if ctag == tag1:
                content.append(q)

    return content


def findId(val, id):
    content = []
    for question in val:
        if question['id'] == id:
            content.append(question)

    return content


def findAnswers(val, id):
    content = []
    for question in val:
        if question['id'] == id:
            for answer_id in question['answers']:
                for answer in val:
                    if answer['id'] == answer_id:
                        content.append(answer)

    return content


def index(request):
    content = pagination(questions, request)
    return render(request, 'index.html', {
        'title': 'New questions',
        'user_login': user,
        'questions': content,
        **tags_users
    })


def hot_questions(request):
    content = pagination(questions, request)
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'user_login': user,
        'questions': content,
        **tags_users
    })


def new_question(request):
    return render(request, 'new_question_page.html', {
        'title': 'New question',
        'user_login': user,
        **tags_users
    })


def question(request, id):
    content = findId(questions, id)
    answer = pagination(findAnswers(questions, id), request, per_page=3)
    return render(request, 'question_page.html', {
        'title': f'Question {id}',
        'user_login': user,
        'questions': content,
        'answers': answer,
        **tags_users
    })


def tag(request, tag):
    content = pagination(findTag(questions, tag), request)
    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'user_login': user,
        'questions': content,
        **tags_users
    })


def settings(request):
    return render(request, 'settings_page.html', {
        'title': 'Settings',
        'user_login': True,
        **tags_users
    })


def sing_in(request):
    return render(request, 'sing_in_page.html', {
        'title': 'Sing In',
        'user_login': False,
        **tags_users
    })


def sing_up(request):
    return render(request, 'sing_up_page.html', {
        'title': 'Sing Up',
        'user_login': False,
        **tags_users
    })
