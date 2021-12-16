from django.urls import path, include
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'quiz-results', views.QuizResultViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('answer/<int:quiz_id>', views.answer),
]
