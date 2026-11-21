import multiprocessing


def calculate_summary():
    total_students = 1
    total_faculty = 1
    total_courses = 1
    total_enrollments = 0

    print("\n===== MULTIPROCESSING SUMMARY =====")
    print("Total Students:", total_students)
    print("Total Faculty:", total_faculty)
    print("Total Courses:", total_courses)
    print("Total Enrollments:", total_enrollments)


if __name__ == "__main__":

    process = multiprocessing.Process(
        target=calculate_summary
    )

    process.start()
    process.join()

    print("Summary process completed.")