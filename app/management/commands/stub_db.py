from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Profile
from django.contrib.auth.models import User
import random

users_count = 25
tags_count = 15
questions_count = 30


class Command(BaseCommand):
    help = 'Filling the database with some values'

    def stub_users(self):
        print('Filling users')

        for i in range(0, users_count):
            username = 'user' + str(i)
            first_name = 'first' + str(i)
            last_name = 'last' + str(i)
            email = 'email' + str(i) + '@mail.ru'
            password = 'passUsername' + str(i)
            User.objects.create(username=username,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                email=email)

    def stub_profiles(self):
        print('Filling profiles')

        for i in range(0, users_count):
            user = User.objects.get(username='user' + str(i))
            count = i
            Profile.objects.create(user=user,
                                   count=count)

    def stub_tags(self):
        print('Filling tags')

        for i in range(0, tags_count):
            Tag.objects.create(name='tag' + str(i))

    def stub_questions(self):
        print('Filling questions')

        for i in range(0, questions_count):
            title = 'title' + str(i)
            author = Profile.objects.get(user__username='user' + str(i % users_count))
            text = str(
                i) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            rating = random.randint(0, 50)
            q = Question.objects.create(title=title,
                                        author=author,
                                        text=text,
                                        rating=rating)

            for i in range(0, random.randint(0, 7)):
                t = Tag.objects.get(name='tag' + str(random.randint(0, tags_count - 1)))
                Tag.objects.filter(name='tag' + str(random.randint(0, tags_count - 1))).update(count=t.count + 1)
                q.tags.add(t)

            q.save()

    def stub_answers(self):
        print('Filling answers')
        for i in range(0, questions_count):
            question = Question.objects.get(title='title' + str(i))

            for i in range(0, random.randint(0, 10)):
                author = Profile.objects.get(user__username='user' + str(random.randint(0, users_count - 1)))
                text = "Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus."
                rating = random.randint(0, 30)
                Answer.objects.create(question=question,
                                      author=author,
                                      text=text,
                                      rating=rating)

    def handle(self, *args, **options):
        self.stub_users()
        self.stub_profiles()
        self.stub_tags()
        self.stub_questions()
        self.stub_answers()
