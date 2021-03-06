# Generated by Django 3.1.3 on 2020-12-01 22:55

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('text', models.TextField(verbose_name='Text')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct answer')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='/avatars/avatar.png', upload_to=app.models.avatar_upload_to, verbose_name='Avatar')),
                ('count', models.IntegerField(default=0, verbose_name='Author rating')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('text', models.TextField(verbose_name='Text')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('count', models.IntegerField(default=1, verbose_name='Number of questions by tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='VoteQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(null=True, verbose_name='Vote')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Voted user')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Question vote',
                'verbose_name_plural': 'Questions votes',
            },
        ),
        migrations.CreateModel(
            name='VoteAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(null=True, verbose_name='Vote')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer', verbose_name='Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Voted user')),
            ],
            options={
                'verbose_name': 'Answer vote',
                'verbose_name_plural': 'Answers votes',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Question'),
        ),
    ]
