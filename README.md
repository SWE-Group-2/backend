# Software Engineering Project Backend
## Mega Cool Badge Zone
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=bugs)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=coverage)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=SWE-Group-2_backend&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=SWE-Group-2_backend)
## Setup
First setup poetry and install the dependencies.
```bash
poetry install
```
After that you can set up pre-commit hooks by running
```bash
poetry run pre-commit install
```
Also feel free to set up Poetry interpreter in Pycharm by going to `File` -> `Settings` -> `Project: backend` -> `Python Interpreter` -> `Add Interpreter` -> `Add Local Interpreter` -> `Poetry Environment`. Then you won't have to type `poetry run` before every command. Afterward, you can run the backend using
```bash
poetry run flask run
```
## Before Committing
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
