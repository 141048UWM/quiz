from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse


from main.models import QuizResult, Quiz, Question, Category
from main.serializers import (
    UserSerializer,
    QuizResultSerializer,
    QuizSerializer,
    QuizAnswerSerializer,
    QuestionSerializer,
    CategorySerializer,
)
from main.filters import (
    UserFilter,
    QuizFilter,
    QuizResultFilter
)
from main.permissions import IsOwner


#widoki po generic api view odbywa się za pomocą model view set


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    #kazdy ma dostep do metody get
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
    #do innych metod tylko administrator ma dostęp 
            permission_classes = [permissions.IsAdminUser]
        return [pc() for pc in permission_classes]

#widoki po generic api view odbywa się za pomocą model view set
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    #rozszerzenie filtru o dodatkowe funkcje z pliku filters.py
    filterse_class = QuizFilter

    def perform_create(self, serializer):
        #nadpisany użytkownik jako twórca quizu
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        #kazdy może tworzyć
        if self.request.method in ['GET', 'POST']:
            permission_classes = [permissions.IsAuthenticated]
        else:
        #ale administrator lub właściciel może zmieniać
            permission_classes = [permissions.IsAdminUser|IsOwner]
        return [pc() for pc in permission_classes]

#widoki po generic api view odbywa się za pomocą model view set
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = ['text', 'category']
    search_fields = ['text']

    def perform_create(self, serializer):
        #nadpisany użytkownik jako twórca pytania
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        #kazdy może tworzyć
        if self.request.method in ['GET', 'POST']:
            permission_classes = [permissions.IsAuthenticated]
        else:
        #ale administrator lub właściciel może zmieniać
            permission_classes = [permissions.IsAdminUser|IsOwner]
        return [pc() for pc in permission_classes]

#widoki po generic api view odbywa się za pomocą model view set
#ReadOnlyModelViewSet powoduje, że widok jest tylko od odczytu
#modyfikacja jest wyłączona
class QuizResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuizResult.objects.all() #odwolanie do modyfikacji
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['user', 'quiz']
    #rozszerzenie filtru o dodatkowe funkcje z pliku filters.py
    filterset_class = QuizResultFilter

#widoki po generic api view odbywa się za pomocą model view set
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #tylko admin może przeglądać endpoint
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['id', 'username', 'email']
    search_fields = ['username', 'email']
    #rozszerzenie filtru o dodatkowe funkcje z pliku filters.py
    filterset_class = UserFilter


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def answer(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    serializer = QuizAnswerSerializer(quiz=quiz, user=request.user, data=request.data)
    if serializer.is_valid():
        quiz_result = serializer.save()
        return redirect(reverse(
            'quizresult-detail',
            args=[quiz_result.id],
            request=request
        ))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
