import threading
import time


def process_student(student_name):
    print(f"Processing student: {student_name}")
    time.sleep(1)
    print(f"Completed student: {student_name}")


students = ["Ankita", "Rahul", "Amit"]


threads = []

for student in students:
    thread = threading.Thread(
        target=process_student,
        args=(student,)
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()


print("All student processing completed.")