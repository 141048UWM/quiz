def calculate_quiz_score(quiz_answers, user_answers):
    score = 0
    for q_id, answer in quiz_answers.items():
        if answer == user_answers.get(q_id):
            score += 1
    return score
