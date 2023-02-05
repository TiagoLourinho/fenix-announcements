# Fenix Announcements Bot

## Description
This project monitors the courses enrolled by a student and informs them via email whenever a new announcement was made. 

The [FenixEdu API](https://fenixedu.org/dev/api/) was used to get the information needed.

___

## Necessary input

The input necessary should be on the `input.py` file following the scheme in this example:

```python
  students = [
    Student("Tiago", 
            "email@gmail.com", 
            [   Course("Course 1 name", 546545654),
                Course("Course 2 name", 569845754),
            ]
    )
]
```

The classes have the following fields:

| Student     | Course          |
| -------- | -------------- |
| name | name |
| email | id |

_Note:_ The id of the course can be found using  the [FenixEdu API](https://fenixedu.org/dev/api/) and [Postman](https://www.postman.com/) for example.