# Generated by Django 5.1.2 on 2024-11-16 23:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, unique=True, verbose_name='tag')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='avatar/%y/%m/%d')),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('answer_count', models.IntegerField(default=0)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='author')),
                ('tags', models.ManyToManyField(to='app.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='author')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='question')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True)),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer', verbose_name='answer')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='author')),
            ],
            options={
                'unique_together': {('profile_id', 'answer_id')},
            },
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True)),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='author')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='question')),
            ],
            options={
                'unique_together': {('profile_id', 'question_id')},
            },
        ),
    ]
