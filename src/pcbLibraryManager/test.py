# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:46:18 2015

@author: piotr at nicecircuits.com
"""
import logging
#enable debug logs
log=logging.getLogger()
log.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s - %(message)s')
logfile=logging.FileHandler("debug.log","w")
logfile.setLevel(logging.INFO)
logfile.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
log.addHandler(console)
log.addHandler(logfile)

log.info("dupa")
log.debug("kuka")