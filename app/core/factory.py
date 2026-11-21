
class Student:
    def __init__(self, name):
        self.name = name

    def get_details(self):
        return f"Student Name: {self.name}"


class Faculty:
    def __init__(self, name):
        self.name = name

    def get_details(self):
        return f"Faculty Name: {self.name}"


class Course:
    def __init__(self, name):
        self.name = name

    def get_details(self):
        return f"Course Name: {self.name}"


class PersonFactory:

    @staticmethod
    def create_person(person_type, name):

        if person_type.lower() == "student":
            return Student(name)

        elif person_type.lower() == "faculty":
            return Faculty(name)

        elif person_type.lower() == "course":
            return Course(name)

        else:
            raise ValueError("Invalid person type")


student = PersonFactory.create_person("student", "Ankita")
faculty = PersonFactory.create_person("faculty", "Rahul")
course = PersonFactory.create_person("course", "Python Programming")

print(student.get_details())
print(faculty.get_details())
print(course.get_details())
