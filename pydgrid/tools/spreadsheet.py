#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 07:14:17 2017

@author: jmmauricio
"""


def a2n(column):
    num_column = 0
    for it in range(len(column)):
        num_column += ord(column[it])-65+26*it
    return num_column