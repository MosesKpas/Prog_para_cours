from celery import Celery
app = Celery(
    'tpcelery',
    broker='amqp://guest:guest@192.168.101.210',
    backend='rpc://'
)
@app.task #
def addition(x, y):
    print(f'1. {x} + {y} = {x+y}')
    print(f'2. {x} + {y} = {x+y}')
    print(f'3. {x} + {y} = {x+y}')
    print(f'4. {x} + {y} = {x+y}')
    return x+y