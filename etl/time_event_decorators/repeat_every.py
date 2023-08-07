import time


def repeat_every_seconds(interval):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                func(*args, **kwargs)
                time.sleep(interval)

        return wrapper

    return decorator
