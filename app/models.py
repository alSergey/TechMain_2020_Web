from django.db import models
from django.contrib.auth.models import User


def avatar_upload_to(instance, filename):
    return 'uploads/avatars/{}/{}'.format(instance.user.id, filename)


class ProfileManager(models.Manager):
    def popular_users(self):
        return self.order_by('-count')[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to=avatar_upload_to, verbose_name='Аватар')
    count = models.IntegerField(default=0, verbose_name='Количество вопросов и ответов у пользователя')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TagManager(models.Manager):
    def popular_tags(self):
        return self.order_by('-count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    count = models.IntegerField(default=0, verbose_name='Количество вопросов по тегу')

    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-rating')

    def tags(self, tag):
        return self.filter(tags__name=tag)

    def question(self, id):
        return self.filter(id=id)


class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def answers_count(self):
        return Answer.objects.answers_count(self.id)

    def all_tags(self):
        return self.tags.all()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def answers(self, question_id):
        return self.filter(question__id=question_id)

    def answers_count(self, question_id):
        return self.filter(question__id=question_id).count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(default=False, verbose_name='Корректность ответа')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = AnswerManager()

    def __str__(self):
        return 'Ответ на вопрос: {}'.format(self.question.title)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class LikeQuestion(models.Manager):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь, который поставил отметку')
    state = models.NullBooleanField(default=None, verbose_name='Состояние отметки')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')


class LikeAnswer(models.Manager):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь, который поставил отметку')
    state = models.NullBooleanField(default=None, verbose_name='Состояние отметки')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
