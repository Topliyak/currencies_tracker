FROM python

WORKDIR /usr/src/currancy_tracker
COPY . .

RUN pip install poetry
RUN poetry install --no-root

CMD poetry run python main.py
