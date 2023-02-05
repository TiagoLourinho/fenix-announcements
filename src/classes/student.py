class Student:
    def __init__(self, name, email, courses):
        self.name = name
        self.email = email
        self.courses = courses

    def __str__(self):
        return (
            f"{{'name': {self.name}, 'email': {self.email}, 'courses': {self.courses}}}"
        )
