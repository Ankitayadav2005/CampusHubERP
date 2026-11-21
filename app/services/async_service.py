import asyncio


async def load_student():
    print("Loading Student...")
    await asyncio.sleep(1)
    print("Student loaded successfully.")


async def load_faculty():
    print("Loading Faculty...")
    await asyncio.sleep(1)
    print("Faculty loaded successfully.")


async def load_courses():
    print("Loading Courses...")
    await asyncio.sleep(1)
    print("Courses loaded successfully.")


async def load_enrollments():
    print("Loading Enrollments...")
    await asyncio.sleep(1)
    print("Enrollments loaded successfully.")