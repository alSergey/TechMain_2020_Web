from django import forms
from app.models import Question, Tag, Answer
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class SingInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SingUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']


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
        answer.question = self.question

        if commit:
            answer.save()

        return answer
