# Setup
First setup poetry and install the dependencies.
```bash
poetry install
```
After that you can set up pre-commit hooks by running
```bash
poetry run pre-commit install
```
Also feel free to set up Poetry interpreter in Pycharm by going to `File` -> `Settings` -> `Project: backend` -> `Python Interpreter` -> `Add Interpreter` -> `Add Local Interpreter` -> `Poetry Environment`. Then you won't have to type `poetry run` before every command.
# Before Committing
Before committing, make sure to run the pre-commit hooks by running
```bash
poetry run pre-commit run --all
```
You can run the tests by running
```bash
poetry run pytest
```
And do linting/formatting by running
```bash
poetry run flake8
poetry run black .
```
