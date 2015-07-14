# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 23:12:28 2015

@author: piotr at nicecircuits.com
"""

import datetime

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


if __name__ == "__main__":
    print(timestamp())