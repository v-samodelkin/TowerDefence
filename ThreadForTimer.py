import threading
import functools


def set_interval(interval):
    def decorator(function, interval=interval):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(interval=interval):
                while not stopped.wait(interval):
                    function(*args, **kwargs)
            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped
        return wrapper
    return decorator
