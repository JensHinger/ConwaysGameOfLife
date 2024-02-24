import time

def measure_time(func):

    def timer(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        stop = time.time()
        print(f"Function {func.__name__} done after: {(stop-start)*1000} ms")

    return timer