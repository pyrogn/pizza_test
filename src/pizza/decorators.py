"""Decorators for adding a delay, spinner and help messages to heavy tasks.

I think it is better to apply decorators directly to methods,
but also check global variable. Current implementation is unnecessary convoluted
and unpythonic (because of procedural generation methods using setattr, getattr).
"""
import functools
import os
import random
import time
from collections.abc import Callable
from functools import reduce
from typing import Any, TypedDict

from pizza.constants import MAX_LATENCY_MS, MIN_LATENCY_MS, TEST_LATENCY_MS
from pizza.spinner import add_spinner


def add_latency(fn) -> Callable:
    """Add random latency to a class method to simulate real work."""

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        """Run function and add random latency from uniform distribution.

        min_ms: minimum latency in ms
        max_ms: maximum latency in ms
        If LATENCY_ENABLED=0, then don't add latency
            If LATENCY_FOR_TEST=1, then set min_ms, max_ms as LATENCY_FOR_TEST
                for test purposes
        """

        min_ms = MIN_LATENCY_MS
        max_ms = MAX_LATENCY_MS

        if os.getenv("LATENCY_ENABLED", "0") == "1":
            if os.getenv("LATENCY_FOR_TEST", "0") == "1":
                min_ms = TEST_LATENCY_MS
                max_ms = TEST_LATENCY_MS

            smoothness = 1000
            # imitate uniform distribution without numpy
            seconds_sleep = random.randint(
                min_ms * smoothness,
                max_ms * smoothness,
            ) / (1000 * smoothness)

            time.sleep(seconds_sleep)

        return fn(self, *args, **kwargs)

    return wrapper


class LogTimeDecorator:
    """Decorator to track and log time of function execution"""

    def __init__(self, str_template: str = "", *, is_return_time: bool) -> None:
        """Initialization decorator with parameters

        Args:
            str_template: string with placeholder to insert time spent in function
                Usage example: Delivery took {:.2f} seconds.
                If provided, then print it, else: do not print
            is_return_time:
                if true, add time as a second return value
        """
        self.str_template = str_template
        self.is_return_time = is_return_time

    def __call__(self, fn: Callable) -> Callable:
        """Decorate provided function"""

        @functools.wraps(fn)
        def log_time(*args: Any, **kwargs: Any) -> tuple[Any, float]:
            """Execute function with custom parameters"""

            time_start = time.time()
            result = fn(*args, **kwargs)
            time_end = time.time()
            execution_time = time_end - time_start
            if self.str_template:
                print(self.str_template.format(execution_time), end="\n")
            if self.is_return_time:
                return result, execution_time
            return result

        return log_time


class MsgForParam(TypedDict):
    """Dict with required keys for tracing heavy tasks."""

    log_time_msg: str
    start_msg: str
    end_msg: str


MethodName = str


def trace_heavy_tasks(params: dict[MethodName, MsgForParam]) -> Callable:
    """Decorate a class adding functionality to selected methods.

    added functionality:
        synthetic latency
        spinner during task execution
        time logging

    Args:
        params: dict with key=method_name, value - map of keyword and text
            keywords:
                start_msg: Message while running
                end_msg: Message at the finish
                log_time_msg: String with placeholder to log time.
    """

    def wrapper(cls):
        @functools.wraps(cls, updated=())
        class DecClass(cls):
            pass

        for method_name in params:
            original_method = getattr(cls, method_name)
            m_params = params[method_name]

            apply_latency = add_latency
            apply_spinner = add_spinner(m_params["start_msg"], m_params["end_msg"])
            apply_timer = LogTimeDecorator(
                m_params["log_time_msg"],
                is_return_time=False,
            )

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
