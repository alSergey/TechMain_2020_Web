from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer
from django.contrib.auth.models import User
from random import randint, choice, choices
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

    def fill_users(self, cnt):
        if cnt is None:
            return False

        print('Filling {} users'.format(cnt))

        for i in range(cnt):
            user = User.objects.create(username=f.name() + str(i), email=f.email())
            Profile.objects.create(user=user)

    def fill_tags(self, cnt):
        if cnt is None:
            return False

        print('Filling {} tags'.format(cnt))

        for i in range(cnt):
            Tag.objects.create(name=f.word() + str(i))

    def fill_questions(self, cnt):
        if cnt is None:
            return False

        print('Filling {} questions'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('id', flat=True))
        tags_count = dict.fromkeys(tags, 0)

        for i in range(cnt):
            question = Question.objects.create(title=f.sentence()[:128],
                                               author_id=choice(authors),
                                               text=f.text())

            for i in set(choices(tags, k=randint(1, 7))):
                tags_count[i] += 1
                question.tags.add(i)

            question.save()

        for tag, count in tags_count.items():
            if count != 0:
                Tag.objects.filter(pk=tag).update(count=count)

    def fill_answers(self, cnt):
        if cnt is None:
            return False

        print('Filling {} answers'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        authors_count = dict.fromkeys(authors, 0)

        for i in range(cnt):
            author = choice(authors)
            Answer.objects.create(question_id=choice(questions),
                                  author_id=author,
                                  text=f.text())

            authors_count[author] += 1

        for author, count in authors_count.items():
            if count != 0:
                Profile.objects.filter(pk=author).update(count=count)

    def fill_likes_questions(self, cnt):
        if cnt is None:
            return False

        print('Filling {} questions likes'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        question_rating = dict.fromkeys(questions, 0)

        for i in range(cnt):
            author = choice(authors)
            question = choice(questions)
            mark = choice([True, True, True, True, False])
            LikeQuestion.objects.create(user_id=author,
                                        state=mark,
                                        question_id=question)
            if mark:
                question_rating[question] += 1
            else:
                question_rating[question] -= 1

        for question, rating in question_rating.items():
            if rating != 0:
                Question.objects.filter(pk=question).update(rating=rating)

    def fill_likes_answers(self, cnt):
        if cnt is None:
            return False

        print('Filling {} answers likes'.format(cnt))

        authors = list(Profile.objects.values_list('id', flat=True))
        answers = list(Answer.objects.values_list('id', flat=True))
        answers_rating = dict.fromkeys(answers, 0)

        for i in range(cnt):
            author = choice(authors)
            answer = choice(answers)
            mark = choice([True, True, True, True, False])
            LikeAnswer.objects.create(user_id=author,
                                      state=mark,
                                      answer_id=answer)
            if mark:
                answers_rating[answer] += 1
            else:
                answers_rating[answer] -= 1

        for answer, rating in answers_rating.items():
            if rating != 0:
                Answer.objects.filter(pk=answer).update(rating=rating)

    def handle(self, *args, **options):
        users_count = options.get('users')
        tags_count = options.get('tags')
        questions_count = options.get('questions')
        answers_count = options.get('answers')
        like_questions_count = options.get('likes_questions')
        like_answers_count = options.get('likes_answers')

        if options.get('db_size') == 'test':
            users_count = test[0]
            tags_count = test[1]
            questions_count = test[2]
            answers_count = test[3]
            like_questions_count = test[4]
            like_answers_count = test[5]
        elif options.get('db_size') == 'small':
            users_count = small[0]
            tags_count = small[1]
            questions_count = small[2]
            answers_count = small[3]
            like_questions_count = small[4]
            like_answers_count = small[5]
        elif options.get('db_size') == 'medium':
            users_count = medium[0]
            tags_count = medium[1]
            questions_count = medium[2]
            answers_count = medium[3]
            like_questions_count = medium[4]
            like_answers_count = medium[5]
        elif options.get('db_size') == 'large':
            users_count = large[0]
            tags_count = large[1]
            questions_count = large[2]
            answers_count = large[3]
            like_questions_count = large[4]
            like_answers_count = large[5]

        self.fill_users(users_count)
        self.fill_tags(tags_count)
        self.fill_questions(questions_count)
        self.fill_answers(answers_count)
        self.fill_likes_questions(like_questions_count)
        self.fill_likes_answers(like_answers_count)
