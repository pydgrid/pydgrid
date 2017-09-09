#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid

sys1 = grid()
t_0 = time.time()
sys1.read('./examples/luna/luna_1_4w.json')  # Load data
sys1.pf()
sys1.get_v()
sys1.get_i()
print('iters: ', sys1.params_pf['iters'])
    