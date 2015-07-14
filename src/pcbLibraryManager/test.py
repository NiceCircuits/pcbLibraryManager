# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:46:18 2015

@author: piotr at nicecircuits.com
"""

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
