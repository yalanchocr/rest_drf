from time import sleep

from .celery import app


@app.task
def add2(x, y):
    sleep(5)
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)