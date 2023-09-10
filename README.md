# pizza

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<img src="./pictures/tom.png" width="230"/>

## Example

https://github.com/pyrogn/pizza_test/assets/60060559/36dbf444-d156-475e-8243-03c9d807cde2


## How to install
1. `git clone https://github.com/pyrogn/pizza_test.git`
2. `cd pizza`
3. If master is empty: `git switch test-task`
4. `virtualenv .venv` or `python3 -m venv .venv`
5. `. .venv/bin/activate`
6. For usage: `python -m pip install .`
7. For development:
   1. [Install PDM](https://pdm.fming.dev/latest/#recommended-installation-method)
   2. `pdm install`
   3. `pre-commit install`

## How to use

1. `pizza menu` get list of all available pizzas
2. `pizza order <pizza name>` order a pizza and pick it up from a restaurant. Escape pizza name if it has more than 1 word.
3. `pizza order <pizza name> --delivery` order a pizza and get delivery
4. `pizza order <pizza name> --delivery --size L` choose pizza size

## TODO
* [x] Add pre-commit hooks for pytest and black,isort
* [x] Add pytest checks to GitHub Actions
* [x] Get familiar with PDM and pyproject.toml
* [x] Think how to make better OO relations
* [x] Add tests (parameters, fixtures)
* [x] Reformat code into modules
* [x] Add emoji to every action (static at the moment)
* [x] Add delay and good stdout to cli commands
* [x] Add comments
* [x] Make it tidy
* [x] Add async cycle bar
