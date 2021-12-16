from main.models import Question, QuizResult


def get_quiz_result(quiz_id, user_id):
    return QuizResult.objects.filter(quiz_id=quiz_id, user_id=user_id).first()


def get_quiz_questions_answers(quiz_id):
    answers = {}
    for q in Question.objects.filter(quiz_id=quiz_id):
        answers[q.id] = q.right_answer
    return answers
