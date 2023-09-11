"""Constants for the project"""
MIN_LATENCY_MS = 150
MAX_LATENCY_MS = 3_000

# Latency duration for testing
TEST_LATENCY_MS = 5
TEST_LATENCY_S = TEST_LATENCY_MS / 1000

# Lines of messages in stdout (some of them can be calculated from info messages)
PIZZA_SIZES_LINES = 1  # extra line under menu about pizza sizes available
INFO_LINES = 1  # info back to user what he orders
INFO_MESSAGE_WRONG_PIZZA_LINES = 1
NUM_ACTIONS_LINES = 2  # bake + deliver/pick up

# Restaurant have these available sizes for all pizzas
AVAILABLE_PIZZA_SIZES: list[str] = ["L", "XL"]
