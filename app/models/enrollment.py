class Enrollment:

    def __init__(self, enrollment_id, student_id, course_code):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_code = course_code

    def display(self):
        print("Enrollment ID:", self.enrollment_id)
        print("Student ID:", self.student_id)
        print("Course Code:", self.course_code)