import django_filters as filters
from main.models import User, QuizResult, Quiz

#data od-do
class UserFilter(filters.FilterSet):
    start_date_joined = filters.DateFilter(field_name="date_joined", lookup_expr="gte")
    end_date_joined = filters.DateFilter(field_name="date_joined", lookup_expr="lte")

    class Meta:
        model = User
        fields = ['start_date_joined', 'end_date_joined']
#data od-do
class QuizFilter(filters.FilterSet):
    start_date = filters.DateFilter('created_at', lookup_expr="gte")
    end_date = filters.DateFilter('created_at', lookup_expr="lte")

    class Meta:
        model = Quiz
        fields = ['start_date', 'end_date']


#zliczanie punktow i data od-do

class QuizResultFilter(filters.FilterSet):
    start_date = filters.DateFilter('created_at', lookup_expr="gte")
    end_date = filters.DateFilter('created_at', lookup_expr="lte")
    min_score = filters.NumberFilter('score', lookup_expr="gte")
    max_score = filters.NumberFilter('score', lookup_expr='lte')

    class Meta:
        model = QuizResult
        fields = ['start_date', 'end_date', 'min_score', 'max_score']
