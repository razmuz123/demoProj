import DBcom
import beanstalkc
from pymemcache.client.base import Client


db = DBcom.DBHandler()
beanstalk = beanstalkc.Connection(host='localhost', port=11300)
client = Client(('localhost', 11211))

#Runs the backend, beanstalk will wait for a job to come in end then execute
while True:
    print('Waiting for queued job...')
    job = beanstalk.reserve()
    print(job.body)
    try:
        client.set('info', db.readDataFromDB(job.body)[0].value)
    except Exception:
        pass
    job.delete()
    print('Job executed...')
