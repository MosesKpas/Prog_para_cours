from tpcelery.celery import addition
import time

if __name__ == '__main__':
    task = result = addition.delay(5, 5)

    while(True):
        time.sleep(0.4)
        if task.ready():
            print(task.result)
        else:
            print('Resultat pas pret!')
