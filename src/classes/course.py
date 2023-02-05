class Course:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.anns = None

    def __str__(self):
        return f"{{'name': {self.name}, 'id': {self.id}, 'anns:' {self.anns}}}"
