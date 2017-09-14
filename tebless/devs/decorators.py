# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from functools import wraps

def theme(func):
    @wraps(func)
    def wrapper(window, opt={}):
        opt_cp = dict(opt)
        tmp = func(window, dict(opt))
        opt_cp.update(tmp)
        return opt_cp
    return wrapper
