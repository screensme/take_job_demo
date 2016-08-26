#!/usr/bin/env python
# encoding: utf-8

import random
def random_str():
    number = '%06i' % (random.randint(0, 999999),)
    return number