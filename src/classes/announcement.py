from datetime import datetime


class Announcement:
    def __init__(self, title, description, date, author):
        self.title = title
        self.description = description
        self.date = date

        # Example: 'joaopeixoto@isr.tecnico.ulisboa.pt (Joao Peixoto)'
        self.author = author.split("(")[1].replace(")", "")

        month = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        # Example: 'Sat, 17 Sep 2022 17:13:01 +0100'
        date = date.split(" ")
        date = date[1:4] + date[4].split(":")
        self.date = datetime(
            int(date[2]),
            month[date[1]],
            int(date[0]),
            int(date[3]),
            int(date[4]),
            int(date[5]),
        )

    def __eq__(self, other):
        return self.title == other.title and self.description == other.description

    def __str__(self):
        return f"{{'title': {self.title}, 'description': {self.description}, 'date': {self.date}}}"
