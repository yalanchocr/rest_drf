from celery import Celery

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//', backend='rpc://')

@app.task
def add(x, y):
    return x + y