"""Adds spinner for long tasks. Inspiration came from the book Fluent Python"""
import functools
import itertools
from threading import Event, Thread


def spin(start_msg: str, end_msg: str, done: Event):
    """Cycle dashes forever until the other thread don't change the Event"""
    for char in itertools.cycle(r"\|/-"):
        status = f"\r {char} {start_msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):  # waits for done to be True
            break
    print(
        f"\r{end_msg}! ", end=""
    )  # print success message rewriting previous msg


def add_spinner(start_msg, end_msg):
    def outer_wrapper(fn):
        functools.wraps(fn)

        def inner_wrapper(self, *args, **kwargs) -> int:
            done = Event()
            spinner = Thread(
                target=spin, args=(start_msg, end_msg, done)
            )  # create new thread
            spinner.start()  # start a second thread
            result = fn(
                self, *args, **kwargs
            )  # function will block main thread. But I don't know what happens to GIL...
            done.set()  # going to stop spin
            spinner.join()  # wait until spin finishes
            return result

        return inner_wrapper

    return outer_wrapper
