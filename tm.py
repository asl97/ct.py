################################################################
# File: tm.py
# Title: Task (Job) Manager Library
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.1
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import time
import queue
import threading

# job manager

class job_manager:

    def __init__(self):
        self.job_queue = queue.Queue()
        self.job_lock = threading.Lock()

    def job_thread(self):
        while True:
            func, args, kw = self.job_queue.get()
            func(*args, **kw)

    def start_job_thread(self,num_of_thread):
        for l in range(0,num_of_thread):
            t = threading.Thread(target=self.job_thread)
            t.daemon = True
            t.start()

    def set_job(self,func,*args, **kw):
        self.job_queue.put((func,args,kw))

_wrapper = job_manager()
set_job = _wrapper.set_job
start_job_thread = _wrapper.start_job_thread

# task object

class _task:

    def __init__(self,timeout,interval,func,*args,**kw):
        self.target = time.time()+timeout
        self.timeout = timeout
        self.interval = interval
        self.job = (func,args,kw)

# task manager

class task_manager:

    def __init__(self):
        self.tasks = set()

    def tick(self):
        now = time.time()
        for task in self.tasks.copy():
            if task.target <= now:
                func, args, kw = task.job
                set_job(func, *args, **kw)
                if task.interval:
                    task.target = now + task.timeout
                else:
                    self.tasks.remove(task)

    def set_timeout(self, timeout, func, *args, **kw):
        task = _task(timeout,False,func,*args,**kw)
        self.tasks.add(task)
        return task

    def set_interval(self, timeout, func, *args, **kw):
        task = _task(timeout,True,func,*args,**kw)
        self.tasks.add(task)
        return task

    def remove_task(self, task):
        self.tasks.remove(task)

_wrapper = task_manager()
tick = _wrapper.tick
set_timeout = _wrapper.set_timeout
set_interval = _wrapper.set_interval
remove_task = _wrapper.remove_task
