from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from random import sample

class ProfileManager(models.Manager):
    def popular_users(self):
        return self.annotate(question_count=Count('question'), answer_count=Count('answer')).order_by('-question_count', '-answer_count')[:5]

    
class QuestionManager(models.Manager):
    def all(self):
        return self.order_by('-created_at')

    def by_tag(self, tag):
        return self.filter(tags__tag=tag).order_by('-rating', '-created_at')

    def hot(self):
        return self.order_by('-rating', '-created_at')

class TagManager(models.Manager):
    def popular_tags(self):
        return self.all().order_by('-rating')[:10]


class AnswerManager(models.Manager):
    def by_question(self, pk):
        return self.filter(question_id=pk).order_by('-rating', 'created_at')

class Tag(models.Model):
    tag = models.CharField(unique=True, max_length=32, verbose_name='tag')
    rating = models.IntegerField(default=0, verbose_name='rating')

    objects = TagManager()

    def __str__(self):
        return self.tag

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='profile')
    avatar = models.ImageField(upload_to='avatar/%y/%m/%d')

    objects = ProfileManager()

    def __str__(self):
        return self.user_id.get_username()

class Question(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='author')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return self.title

class QuestionLike(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='author')
    is_like = models.BooleanField(default=True)

    def __str__(self):
        action = 'liked' if self.is_like else 'disliked'
        return f'{self.profile_id.user_id.get_username()} {action} question "{self.question_id.title}"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.question_id.rating += 1
            else:
                self.question_id.rating -= 1
            self.question_id.save()
        super(QuestionLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.question_id.rating -= 1
        else:
            self.question_id.rating += 1
        self.question_id.save()
        super(QuestionLike, self).delete(*args, **kwargs)
    
    class Meta:
        unique_together = ['profile_id', 'question_id']
    

class Answer(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='author')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    objects = AnswerManager()

    def __str__(self):
        return self.question_id.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.question_id.answer_count += 1
            self.question_id.save()
        super(Answer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question_id.answer_count -= 1
        self.question_id.save()
        super(Answer, self).delete(*args, **kwargs)

class AnswerLike(models.Model):
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='answer')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='author')
    is_like = models.BooleanField(default=True)

    def __str__(self):
        action = 'liked' if self.is_like else 'disliked'
        return f'{self.profile_id.user_id.get_username()} {action} answer "{self.answer_id.content}"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.answer_id.rating += 1
            else:
                self.answer_id.rating -= 1
            self.answer_id.save()
        super(AnswerLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.answer_id.rating -= 1
        else:
            self.answer_id.rating += 1
        self.answer_id.save()
        super(AnswerLike, self).delete(*args, **kwargs)
    

    class Meta:
        unique_together = ['profile_id', 'answer_id']
