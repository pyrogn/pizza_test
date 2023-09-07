# pizza

<img src="./pictures/tom.png" width="230"/>

## Example

https://github.com/pyrogn/pizza_test/assets/60060559/f889dad5-a3fa-46f8-98d0-bb49113dccc4


## How to install
1. `git clone <link>`
2. `cd pizza`
3. `virtualenv .venv`
4. `. .venv/bin/activate`
5. `python -m pip install .` or for development `pdm install -d`
6. `pre-commit install` (development)

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
