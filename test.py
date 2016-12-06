#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
def use_logging(func:object) -> object:
    def wrapper(*args, **kwargs):
        logging.warning("{0} is running".format(func))
        return func(*args, **kwargs)
    return wrapper

@use_logging
def bar():
    return "I'm bar!"

print(bar())
