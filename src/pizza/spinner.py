"""Inspiration came from the book Fluent Python"""
import functools
import itertools
from threading import Event, Thread


def spin(start_msg: str, end_msg: str, done: Event):
    for char in itertools.cycle(r"\|/-"):
        status = f"\r {char} {start_msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{end_msg}! ", end="")
    # print(f"\r{blanks}\r", end="")


def add_spinner(start_msg, end_msg):
    def outer(fn):
        functools.wraps(fn)

        def wrapper(self, *args, **kwargs) -> int:
            done = Event()
            spinner = Thread(target=spin, args=(start_msg, end_msg, done))
            spinner.start()
            result = fn(self, *args, **kwargs)
            done.set()
            spinner.join()
            return result

        return wrapper

    return outer


# def main(slow_func, *args) -> None:
#     result = supervisor(slow_func, *args)
