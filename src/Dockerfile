FROM python:3.8
ADD . /app
WORKDIR /app
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN pip install poetry 
COPY pyproject.toml pyproject.toml 
COPY poetry.lock poetry.lock 
RUN poetry install --no-interaction
ENTRYPOINT poetry run python bot.py 
