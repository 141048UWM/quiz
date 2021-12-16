from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



#właściciel jako użytkownik wbudowany w Django #1
class Quiz(models.Model):
    name = models.CharField(max_length=50)
    #1
    owner = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
#właściciel jako użytkownik wbudowany w Django #3
class Question(models.Model):
    ANSWERS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    )
    #3
    owner = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name='questions')
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT,
                             related_name='questions')
    text = models.CharField(max_length=180)
    answer_1 = models.CharField(max_length=150)
    answer_2 = models.CharField(max_length=150)
    answer_3 = models.CharField(max_length=150)
    answer_4 = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='questions')
    right_answer = models.IntegerField(choices=ANSWERS)

    def __str__(self):
        return self.text

#właściciel jako użytkownik wbudowany w Django #2
class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT,
                             related_name='quiz_results')
    #2
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='quiz_results')
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
