from django.contrib.auth.models import User

from rest_framework import serializers

from main import models, queries, core


class UserSerializer(serializers.ModelSerializer):
    quizzes = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        many=True,
        view_name='quiz-detail'
    )
    #odczytanie pytan i rezultatów powiązanych z question-detail
    # i quizresult-detail
    questions = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='question-detail'
    )
    quiz_results = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='quizresult-detail'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined',
                  'quizzes', 'questions', 'quiz_results']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    #odczytanie pytan powiązanych z question-detail
    questions = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='question-detail'
    )

    class Meta:
        model = models.Category
        fields = ['name', 'questions']


class QuizSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
        #odczytanie pytan i rezultatów powiązanych z question-detail
        # i quizresult-detail
    questions = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='question-detail'
    )
    quiz_results = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='quizresult-detail'
    )

    class Meta:
        model = models.Quiz
        fields = ['name', 'owner', 'questions', 'quiz_results']


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    quiz = serializers.SlugRelatedField(
        queryset=models.Quiz.objects.all(),
        slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Question
        fields = ['id', 'owner', 'quiz', 'text', 'category', 'right_answer',
                  'answer_1', 'answer_2', 'answer_3', 'answer_4']

    def _get_answer(self, instance):
        user = self.context['request'].user
        if user.is_staff or user.id == instance.owner_id:
            return instance.right_answer
        return 'Hidden'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            if 'right_answer' in r:
                r['right_answer'] = self._get_answer(instance)
        return r


class QuizResultSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=models.User.objects.all(),
        slug_field='username'
    )
    quiz = serializers.SlugRelatedField(
        queryset=models.Quiz.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.QuizResult
        fields = ['quiz', 'user', 'score']


class AnswerSerializer(serializers.Serializer):
    answer = serializers.ChoiceField(choices=models.Question.ANSWERS)
    question_id = serializers.IntegerField(required=True)


class QuizAnswerSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=True)

    def __init__(self, *args, quiz, user, **kwargs):
        super().__init__(*args, **kwargs)
        self._quiz = quiz
        self._questions_answers = None
        self._user = user

    def validate(self, data):
        data = super().validate(data)

        if queries.get_quiz_result(self._quiz.id, self._user.id) is not None:
            raise serializers.ValidationError('The quiz has already been solved before')

        if not data['answers']:
            raise serializers.ValidationError('Required answers')

        self._questions_answers = queries.get_quiz_questions_answers(self._quiz.id)

        for answer_data in data['answers']:
            question_id = answer_data['question_id']
            if question_id not in self._questions_answers:
                raise serializers.ValidationError('Invalid question_id: {}'.format(question_id))

        user_answers = self._user_answers_to_dict(data['answers'])
        #wiecej niz trzeba odpowiedzi na to samo pytanie
        if len(user_answers) != len(data['answers']):
            raise serializers.ValidationError('Detected more answers for the same question')

        return user_answers

    def save(self, **kwargs):
        if self._questions_answers is None:
            raise Exception('Invoke validate before save')
        #tworzenie quiz result
        return models.QuizResult.objects.create(
            quiz=self._quiz,
            user=self._user,
            score=core.calculate_quiz_score(
                quiz_answers=self._questions_answers,
                user_answers=self.validated_data
            )
        )

    def _user_answers_to_dict(self, answers):
        return {a['question_id']: a['answer'] for a in answers}
