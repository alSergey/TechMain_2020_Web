from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer
from django.contrib.auth.models import User
from random import randint, choice, choices
from itertools import islice
from faker import Faker

f = Faker()

test = [5, 10, 15, 50, 25, 35]
small = [100, 100, 1000, 10000, 5000, 15000]
medium = [1000, 1000, 10000, 100000, 50000, 150000]
large = [10000, 10000, 100000, 1000000, 500000, 1500000]


class Command(BaseCommand):
    help = 'Filling the database with some values'

    def add_arguments(self, parser):
        parser.add_argument('--db_size', type=str, help="DB size: small, medium, large")
        parser.add_argument('--users', type=int, help='Users count')
        parser.add_argument('--tags', type=int, help='Tags count')
        parser.add_argument('--questions', type=int, help='Questions count')
        parser.add_argument('--answers', type=int, help='Answers count')
        parser.add_argument('--likes_questions', type=int, help='Questions likes count')
        parser.add_argument('--likes_answers', type=int, help='Answers likes count')

    def bulk_create(self, Obj, objs):
        batch_size = 10000

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Obj.objects.bulk_create(batch, batch_size)

    def fill_users(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} users'.format(cnt))
        objs = (
            User(username=f.name() + str(i), email=f.email())
            for i in range(cnt)
        )
        self.bulk_create(User, objs)
        print('End filling users')

        print('Start filling {} profiles'.format(cnt))
        users_id = list(User.objects.values_list('id', flat=True))
        objs = (
            Profile(user_id=users_id[i])
            for i in range(cnt)
        )
        self.bulk_create(Profile, objs)
        print('End filling profiles')

    def fill_tags(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} tags'.format(cnt))
        objs = (
            Tag(name=f.word() + str(i))
            for i in range(cnt)
        )
        self.bulk_create(Tag, objs)
        print('End filling tags')

    def fill_questions(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} questions'.format(cnt))
        authors_id = list(Profile.objects.values_list('id', flat=True))
        objs = (
            Question(title=f.sentence()[:128], author_id=choice(authors_id), text=f.text())
            for i in range(cnt)
        )
        self.bulk_create(Question, objs)
        print('End filling questions')

        print('Start filling {} question tags'.format(cnt))
        tags_id = list(Tag.objects.values_list('id', flat=True))
        tags_count = dict.fromkeys(tags_id, 0)

        for item in Question.objects.all():
            for j in set(choices(tags_id, k=randint(1, 7))):
                tags_count[j] += 1
                item.tags.add(j)

        print('End filling question tags')

        print('Start updating {} tags'.format(len(tags_id)))
        tags = list(Tag.objects.all())
        for tag in tags:
            tag.count = tags_count[tag.pk]

        Tag.objects.bulk_update(tags, ['count'])
        print('End updating tags')

    def fill_answers(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} answers'.format(cnt))
        questions_id = list(Question.objects.values_list('id', flat=True))
        authors_id = list(Profile.objects.values_list('id', flat=True))
        authors_rand = choices(authors_id, k=cnt)
        objs = (
            Answer(question_id=choice(questions_id), author_id=authors_rand[i], text=f.text())
            for i in range(cnt)
        )
        self.bulk_create(Answer, objs)
        print('End filling answers')

        print('Start updating {} authors'.format(len(authors_id)))
        authors_count = dict.fromkeys(authors_id, 0)
        for i in authors_rand:
            authors_count[i] += 1

        authors = list(Profile.objects.all())
        for author in authors:
            author.count = authors_count[author.pk]

        Profile.objects.bulk_update(authors, ['count'])
        print('End updating authors')

    def fill_likes_questions(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} questions likes'.format(cnt))
        authors_id = list(Profile.objects.values_list('id', flat=True))
        questions_id = list(Question.objects.values_list('id', flat=True))
        questions_rand = choices(questions_id, k=cnt)
        mark_rand = choices([True, True, True, True, False], k=cnt)
        objs = (
            LikeQuestion(user_id=choice(authors_id), state=mark_rand[i], question_id=questions_rand[i])
            for i in range(cnt)
        )
        self.bulk_create(LikeQuestion, objs)
        print('End filling questions likes')

        print('Start updating {} questions rating'.format(len(questions_id)))
        questions_count = dict.fromkeys(questions_id, 0)
        for i in range(len(questions_rand)):
            if mark_rand[i]:
                questions_count[questions_rand[i]] += 1
            else:
                questions_count[questions_rand[i]] -= 1

        questions = list(Question.objects.all())
        for question in questions:
            question.rating = questions_count[question.pk]

        Question.objects.bulk_update(questions, ['rating'])
        print('End updating questions rating')

    def fill_likes_answers(self, cnt):
        if cnt is None:
            return False

        print('Start filling {} answers likes'.format(cnt))
        authors_id = list(Profile.objects.values_list('id', flat=True))
        answers_id = list(Answer.objects.values_list('id', flat=True))
        answers_rand = choices(answers_id, k=cnt)
        mark_rand = choices([True, True, True, True, False], k=cnt)
        objs = (
            LikeAnswer(user_id=choice(authors_id), state=mark_rand[i], answer_id=answers_rand[i])
            for i in range(cnt)
        )
        self.bulk_create(LikeAnswer, objs)
        print('End filling answers likes')

        print('Start updating {} answers rating'.format(len(answers_id)))
        answers_count = dict.fromkeys(answers_id, 0)
        for i in range(len(answers_rand)):
            if mark_rand[i]:
                answers_count[answers_rand[i]] += 1
            else:
                answers_count[answers_rand[i]] -= 1

        answers = list(Answer.objects.all())
        for answer in answers:
            answer.rating = answers_count[answer.pk]

        Answer.objects.bulk_update(answers, ['rating'])
        print('End updating answers rating')

    def handle(self, *args, **options):
        current = [options.get('users'),
                   options.get('tags'),
                   options.get('questions'),
                   options.get('answers'),
                   options.get('likes_questions'),
                   options.get('likes_answers')]

        if options.get('db_size') == 'test':
            current = test
        elif options.get('db_size') == 'small':
            current = small
        elif options.get('db_size') == 'medium':
            current = medium
        elif options.get('db_size') == 'large':
            current = large

        self.fill_users(current[0])
        self.fill_tags(current[1])
        self.fill_questions(current[2])
        self.fill_answers(current[3])
        self.fill_likes_questions(current[4])
        self.fill_likes_answers(current[5])
