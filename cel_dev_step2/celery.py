from celery import Celery

app = Celery('cel_dev_step2',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://',
             include=['cel_dev_step2.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    task_keyprefix="jack_rpc_",  # Custom prefix for task queues
    rpc_result_persistent=True,  # Ensure the result queue is not auto-deleted
    worker_prefetch_multiplier = 1

 )

app.conf.result_backend_transport_options = {
    'global_keyprefix': 'my_prefix_'
}

if __name__ == '__main__':
    app.start()