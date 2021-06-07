# coding = UTF-8
import time, sys

reps = 0
def trace(*args):
    pass

def timer(func, *pargs, **kargs):
    global reps 
    _reps = kargs.pop('_reps', reps)
    trace(func, pargs, kargs, _reps)
    reps_list = range(_reps)
    start = time.perf_counter()
    for n in reps_list:
        ret = func(*pargs, **kargs)
    elapsed = time.perf_counter() - start
    return (elapsed, ret)

def init_timer(r: int = 0):
    global reps 
    reps = r
    reps_list = range(reps)

def best(func, *pargs, **kargs):
    global reps 
    _reps = kargs.pop('_reps', reps)
    best = 2 ** 32
    for i in range(_reps):
        (time, ret) = timer(func, *pargs, _reps = 1, **kargs)
        if time < best:
            best = time
    return (best, ret)


