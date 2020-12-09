from django.db import models
from django.contrib.auth.models import User


def avatar_upload_to(instance, filename):
    return 'avatars/{}/{}'.format(instance.id, filename)


class ProfileManager(models.Manager):
    def popular_users(self):
        return self.order_by('-count')[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    avatar = models.ImageField(default='/avatars/avatar.png', upload_to=avatar_upload_to, verbose_name='Avatar')
    count = models.IntegerField(default=0, verbose_name='Author rating')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class TagManager(models.Manager):
    def popular_tags(self):
        return self.order_by('-count')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Name')
    count = models.IntegerField(default=1, verbose_name='Number of questions by tag')

    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-rating')

    def tags(self, tag):
        return self.filter(tags__name=tag)


class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='Title')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Author')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    text = models.TextField(verbose_name='Text')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Tags')
    rating = models.IntegerField(default=0, verbose_name='Rating')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def answers_count(self):
        return Answer.objects.answers_count(self.id)

    def all_tags(self):
        return self.tags.all()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def answers(self, question_id):
        return self.filter(question__id=question_id)

    def answers_count(self, question_id):
        return self.filter(question__id=question_id).count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Author')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    text = models.TextField(verbose_name='Text')
    is_correct = models.BooleanField(default=False, verbose_name='Is correct answer')
    rating = models.IntegerField(default=0, verbose_name='Rating')

    objects = AnswerManager()

    def __str__(self):
        return 'Ответ на вопрос: {}'.format(self.question.title)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class VoteQuestionManager(models.Manager):
    def reaction(self, qlist, aid):
        votes = {}
        for vote in self.filter(question_id__in=qlist, author_id=aid).all():
            votes[vote.question.id] = vote.state

        return votes


class VoteQuestion(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Voted user')
    state = models.BooleanField(null=True, verbose_name='Vote')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')

    objects = VoteQuestionManager()

    def __str__(self):
        return 'Vote question: {}'.format(self.question.title)

    class Meta:
        verbose_name = 'Question vote'
        verbose_name_plural = 'Questions votes'


class VoteAnswerManager(models.Manager):
    def reaction(self, alist, aid):
        votes = {}
        for vote in self.filter(answer_id__in=alist, author_id=aid).all():
            votes[vote.answer.id] = vote.state

        return votes


class VoteAnswer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Voted user')
    state = models.BooleanField(null=True, verbose_name='Vote')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Answer')

    objects = VoteAnswerManager()

    def __str__(self):
        return 'Vote answer: {}'.format(self.answer.question.title)

    class Meta:
        verbose_name = 'Answer vote'
        verbose_name_plural = 'Answers votes'
