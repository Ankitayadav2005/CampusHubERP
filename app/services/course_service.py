from app.utils.decorators import log_decorator, time_decorator


courses = []


@log_decorator
@time_decorator
def add_course(course):
    courses.append(course)
    print("Course added successfully.")


@log_decorator
@time_decorator
def remove_course(course_code):
    for course in courses:
        if course.course_code == course_code:
            courses.remove(course)
            print("Course removed successfully.")
            return

    print("Course not found.")


@log_decorator
@time_decorator
def update_course(
    course_code,
    course_name=None,
    credits=None
):
    for course in courses:
        if course.course_code == course_code:

            if course_name is not None:
                course.course_name = course_name

            if credits is not None:
                course.credits = credits

            print("Course updated successfully.")
            return

    print("Course not found.")


@log_decorator
@time_decorator
def list_courses():
    return courses


def list_courses_sorted():
    return sorted(
        courses,
        key=lambda course: course.course_name
    )