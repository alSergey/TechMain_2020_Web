from django import forms
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.models import Question, Tag, Answer, Profile, VoteQuestion, VoteAnswer


class SingInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SingUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar']

    def save(self, commit=False):
        user = super().save(commit=True)

        if self.files.get('avatar'):
            Profile.objects.create(user_id=user.pk, avatar=self.files.get('avatar'))
        else:
            Profile.objects.create(user_id=user.pk)

        if commit:
            user.save()

        return user


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']

    def save(self, commit=False):
        user = super().save(commit=True)

        if self.files.get('avatar'):
            profile = Profile.objects.get(user_id=user.id)
            profile.avatar = self.files.get('avatar')
            profile.save()

        if commit:
            user.save()

        return user


class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 6})
        }

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = super().save(commit=False)
        question.author = self.profile
        Profile.objects.filter(id=question.author_id).update(count=F('count') + 1)

        if commit:
            question.save()
            for tag in self.cleaned_data['tags'].split(' '):
                try:
                    id = Tag.objects.get(name=tag).id
                    Tag.objects.filter(id=id).update(count=F('count') + 1)
                except Tag.DoesNotExist:
                    id = Tag.objects.create(name=tag).id
                question.tags.add(id)

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, question, profile, *args, **kwargs):
        self.question = question
        self.profile = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.author = self.profile
        Profile.objects.filter(id=answer.author_id).update(count=F('count') + 1)
        answer.question = self.question

        if commit:
            answer.save()

        return answer


class VoteQuestionForm(forms.ModelForm):
    class Meta:
        model = VoteQuestion
        fields = ['author', 'state', 'question']

    def __init__(self, action, *args, **kwargs):
        self.action = action
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        if self.action == 'create':
            vote = VoteQuestion.objects.create(question_id=self.cleaned_data['question'].id,
                                               author_id=self.cleaned_data['author'].id,
                                               state=self.cleaned_data['state'])

            if self.cleaned_data['state']:
                count = 1
            else:
                count = -1

        elif self.action == 'update':
            vote = VoteQuestion.objects.get(question_id=self.cleaned_data['question'].id,
                                            author_id=self.cleaned_data['author'].id)
            vote.state = self.cleaned_data['state']
            vote.save()

            if self.cleaned_data['state']:
                count = 2
            else:
                count = -2

        else:
            vote = VoteQuestion.objects.filter(question_id=self.cleaned_data['question'].id,
                                               author_id=self.cleaned_data['author'].id).delete()

            if self.cleaned_data['state']:
                count = -1
            else:
                count = 1

        Question.objects.filter(id=self.cleaned_data['question'].id).update(rating=F('rating') + count)

        return vote


class VoteAnswerForm(forms.ModelForm):
    class Meta:
        model = VoteAnswer
        fields = ['author', 'state', 'answer']

    def __init__(self, action, *args, **kwargs):
        self.action = action
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        if self.action == 'create':
            vote = VoteAnswer.objects.create(answer_id=self.cleaned_data['answer'].id,
                                             author_id=self.cleaned_data['author'].id,
                                             state=self.cleaned_data['state'])

            if self.cleaned_data['state']:
                count = 1
            else:
                count = -1

        elif self.action == 'update':
            vote = VoteAnswer.objects.get(answer_id=self.cleaned_data['answer'].id,
                                          author_id=self.cleaned_data['author'].id)
            vote.state = self.cleaned_data['state']
            vote.save()

            if self.cleaned_data['state']:
                count = 2
            else:
                count = -2

        else:
            vote = VoteAnswer.objects.filter(answer_id=self.cleaned_data['answer'].id,
                                             author_id=self.cleaned_data['author'].id).delete()

            if self.cleaned_data['state']:
                count = -1
            else:
                count = 1

        Answer.objects.filter(id=self.cleaned_data['answer'].id).update(rating=F('rating') + count)

        return vote


class CorrectForm(forms.Form):
    id = forms.IntegerField()
    checked = forms.BooleanField(required=False)

    def save(self):
        answer = Answer.objects.get(id=self.cleaned_data['id'])
        answer.is_correct = self.cleaned_data['checked']
        answer.save()

        return answer
