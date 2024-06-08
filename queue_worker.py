#!/usr/bin/env python
from redis import Redis
from rq import Worker

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['generate'], connection=Redis())
w.work()
