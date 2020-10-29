from django.shortcuts import render

tags_users = {
    'tags': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8'],
    'users': ['mr greeman', 'dr house', 'bender', 'queen victoria', 'pupkin'],
}

questions = []
for i in range(1, 20):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'answer': str(i),
        'tags': ['tag' + str(i), 'tag' + str(i + 1)],
        'rating': str(i),
        'text': 'text ' + str(i)
    })

questions.append(({
    'title': 'title ' + str(21),
    'id': 21,
    'answer': str(21),
    'tags': ['tag1'],
    'rating': str(21),
    'text': 'text ' + str(21)
}))

questions.append(({
    'title': 'title ' + str(22),
    'id': 22,
    'answer': str(22),
    'tags': ['tag1'],
    'rating': str(22),
    'text': 'text ' + str(22)
}))

questions.append(({
    'title': 'title ' + str(23),
    'id': 23,
    'answer': str(23),
    'tags': ['tag1'],
    'rating': str(23),
    'text': 'text ' + str(23)
}))

questions.append(({
    'title': 'title ' + str(24),
    'id': 24,
    'answer': str(24),
    'tags': ['tag2'],
    'rating': str(24),
    'text': 'text ' + str(24)
}))

questions.append(({
    'title': 'title ' + str(25),
    'id': 25,
    'answer': str(25),
    'tags': ['tag3'],
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
    print(val)
    print(id)
    for question in val:
        if question['id'] == id:
            content.append(question)

    print(content)
    return content


def index(request):
    return render(request, 'index.html', {
        'title': 'New questions',
        'questions': questions,
        **tags_users
    })


def hot_questions(request):
    return render(request, 'index.html', {
        'title': 'Hot questions',
        'questions': questions,
        **tags_users
    })


def new_question(request):
    return render(request, 'new_question_page.html', {
        'title': 'New question',
        **tags_users
    })


def question(request, id):
    print(id)
    return render(request, 'question_page.html', {
        'title': f'question {id}',
        'questions': findId(questions, id),
        **tags_users
    })


def tag(request, tag):
    return render(request, 'index.html', {
        'title': f'Tag: {tag}',
        'questions': findTag(questions, tag),
        **tags_users
    })


def settings(request):
    return render(request, 'settings_page.html', {
        'title': 'Settings',
        **tags_users
    })


def sing_in(request):
    return render(request, 'sing_in_page.html', {
        'title': 'Sing In',
        **tags_users
    })


def sing_up(request):
    return render(request, 'sing_up_page.html', {
        'title': 'Sing Up',
        **tags_users
    })
