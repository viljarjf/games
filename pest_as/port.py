# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:48:34 2020

@author: Viljar Femoen
"""

class Port:

    def __init__(self, A, B, prob):
        self.A = A
        self.B = B
        self.prob = prob

    def check(self, rand):
        return self.prob < rand
    