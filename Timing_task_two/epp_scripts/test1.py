from Timing_task_two .celery import app

def test11():
    print("test11----------------")

def test22(x,y):
    print("test22--------------")
    return x + y

@app.task
def celery_run():
    test11()
    test22(2,5)

if __name__ == '__main__':
    celery_run()
