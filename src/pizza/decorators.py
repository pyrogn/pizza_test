"""Decorators for adding a delay, spinner and help messages to heavy tasks"""
import functools
import os
import random
import time
from functools import reduce
from typing import TypedDict

from pizza.spinner import add_spinner


def add_latency(fn):
    """Add random latency to a class method to simulate real work
    Latency is distributed uniformly
    min_ms: minimum latency in ms
    max_ms: maximum latency in ms"""
    min_ms = 150
    max_ms = 3_000

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        seconds_sleep = 0
        # CONFUSION: I am not sure if it is a good way to read some global defaults
        is_latency_enabled = os.getenv(
            "LATENCY_ENABLED", "0"
        )  # if 1 - latency added (cli), if 0 - no latency (everything else)

        if is_latency_enabled == "1":
            smoothness = 1000
            # imitate uniform distribution without numpy
            seconds_sleep = random.randint(
                min_ms * smoothness, max_ms * smoothness
            ) / (1000 * smoothness)

        time.sleep(seconds_sleep)
        result = fn(self, *args, **kwargs)
        return result

    return wrapper


def log_time(str_template: str):
    """Log and print time spent in the function call
    str_template: string with placeholder to insert time spent in function
        Example: Delivery took {:.2f} seconds"""

    def outer_wrapper(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            result = fn(self, *args, **kwargs)
            lapsed_time = time.time() - time_start
            print(str_template.format(lapsed_time), end="\n")
            return result

        return wrapper

    return outer_wrapper


class MsgForParam(TypedDict):
    """Dict with required keys for tracing heavy tasks"""

    log_time_msg: str
    start_msg: str
    end_msg: str


MethodName = str


def trace_heavy_tasks(
    params: dict[MethodName, MsgForParam],
):
    """Decorate a class adding functionality to selected methods
    added functionality:
        synthetic latency
        spinner during task execution
        time logging
    parameters:
        params: dict with key=method_name, value - map of keyword and text
        required keywords:
            start_msg: Message while running
            end_msg: Message at the finish
            log_time_msg: String with placeholder to log time"""

    def wrapper(cls):
        @functools.wraps(cls, updated=())
        class DecClass(cls):
            pass

        for method_name in params.keys():
            original_method = getattr(cls, method_name)
            m_params = params[method_name]

            apply_latency = add_latency
            apply_spinner = add_spinner(m_params["start_msg"], m_params["end_msg"])
            apply_timer = log_time(m_params["log_time_msg"])

            func_list = [apply_latency, apply_spinner, apply_timer]
            full_mod_method = (
                reduce(  # apply every function consecutively to original_method
                    lambda o, func: func(o),
                    func_list,
                    original_method,
                )
            )

            setattr(DecClass, method_name, full_mod_method)
        return DecClass

    return wrapper
