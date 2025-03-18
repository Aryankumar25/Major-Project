import time

def track_performance(func):
    """Measure the execution time of a function."""
    start_time = time.time()
    result = func()
    end_time = time.time()
    return result, end_time - start_time
