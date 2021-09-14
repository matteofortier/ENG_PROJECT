from apscheduler.schedulers.background import BackgroundScheduler
import time

print('Hello')

sched = BackgroundScheduler()
sched.add_job(lambda : sched.print_jobs(),'interval',seconds=5)
sched.start()

try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown() 