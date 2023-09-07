"""Decorators for adding a delay and help messages to heavy tasks"""
import functools
import os
import random
import time

from pizza.spinner import add_spinner


def add_latency(fn):
    """Add random latency to a class method to simulate real work"""

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        time_sleep = 0
        # CONFUSION: I am not sure if it is a good way to read some global defaults
        is_latency_enabled = os.getenv(
            "LATENCY_ENABLED", "0"
        )  # if 1 - latency added (cli), if 0 - no latency (everything else)

        if is_latency_enabled == "1":
            multiply = 1000
            # imitate uniform distribution without numpy
            time_sleep = random.randint(1 * multiply, 30 * multiply) / (
                10 * multiply
            )  # max 3 seconds

        time.sleep(time_sleep)
        result = fn(self, *args, **kwargs)
        return result

    return wrapper


def log_time(str_template: str):
    """Log and print time spent in the function call"""

    def outer_wrapper(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            result = fn(self, *args, **kwargs)
            lapsed_time = time.time() - time_start
            print(
                str_template.format(lapsed_time)
            )  # put time into placeholder
            return result

        return wrapper

    return outer_wrapper


MethodName = str
MsgForParam = dict[str, str]


def trace_heavy_tasks(
    params: dict[MethodName, MsgForParam],
):
    def wrapper(cls):
        @functools.wraps(cls, updated=())
        class DecClass(cls):
            pass

        for method_name in params.keys():
            original_method = getattr(cls, method_name)
            m_params = params[method_name]

            apply_latency = add_latency
            apply_spinner = add_spinner(
                m_params["start_msg"], m_params["end_msg"]
            )
            apply_timer = log_time(m_params["log_time_msg"])

            full_mod_method = apply_timer(
                apply_spinner(apply_latency(original_method))
            )
            setattr(DecClass, method_name, full_mod_method)
        return DecClass

    return wrapper
