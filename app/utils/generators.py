def create_id_generator(prefix):
    number = 1

    while True:
        yield f"{prefix}{number:03d}"
        number += 1


student_id_generator = create_id_generator("ST")
faculty_id_generator = create_id_generator("FC")
course_id_generator = create_id_generator("CS")


def generate_student_id():
    return next(student_id_generator)


def generate_faculty_id():
    return next(faculty_id_generator)


def generate_course_id():
    return next(course_id_generator)


def student_report(students):
    for student in students:
        yield student


def faculty_report(faculties):
    for faculty in faculties:
        yield faculty


def course_report(courses):
    for course in courses:
        yield course


class StudentIterator:

    def __init__(self, students):
        self.students = students
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.students):
            raise StopIteration

        student = self.students[self.index]
        self.index += 1

        return student