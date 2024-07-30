from threading import Semaphore, Thread

semaphore = Semaphore()
threads = []


def thread_worker(func, *args):
    # Acquire a semaphore before starting the thread
    semaphore.acquire()
    try:
        func(*args)
    finally:
        # Release the semaphore after the thread function completes
        semaphore.release()


def start_thread(func, *args):
    # Create a new thread to run the worker
    thread = Thread(target=thread_worker, args=(func,) + args)
    threads.append(thread)
    thread.start()
