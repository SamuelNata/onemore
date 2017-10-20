from math import sqrt

def module(v):
    return sqrt(v[1]**2+v[0]**2)

def vetUnitario(v):
    return (v[0]/module(v), v[1]/module(v))