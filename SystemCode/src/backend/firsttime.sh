#! /bin/bash
poetry config virtualenvs.in-project true

poetry install

cp .env.example .env

alembic upgrade head

flask seed run

flask run