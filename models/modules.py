class Module:
    def __init__(self, title, lock_until):
        self.title = title
        self.lock_until = lock_until
        self.assignments = []
        self.quizzes = []

    def add_assignment(self, title, description, due_date):
        
        
        assignment = Assignment(title, description, due_date)
        self.assignments.append(assignment)

    def add_quiz(self, title, lock_until):
        quiz = Quiz(title, lock_until)
        self.quizzes.append(quiz)