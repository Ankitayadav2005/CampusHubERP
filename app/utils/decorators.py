import time
from functools import wraps


def log_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"{func.__name__} - Function Started")

        result = func(*args, **kwargs)

        print(f"{func.__name__} - Function Completed")

        return result

    return wrapper


def time_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()

        execution_time = end_time - start_time

        print(
            f"{func.__name__} execution time: "
            f"{execution_time:.6f} seconds"
        )

        return result

    return wrapper