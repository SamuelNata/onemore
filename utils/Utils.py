from math import sqrt
from datetime import datetime as dt
from threading import Thread, Condition

startTime = ''

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE =  (255, 255, 255)
SKY = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)


def module(v):
    return sqrt(v[1]**2+v[0]**2)

def vetUnitario(v):
    return (v[0]/module(v), v[1]/module(v))

def logf(msg, show = False):
    global startTime
    startTime = str(dt.now())[19] if startTime=='' else startTime
    filename = "log/log "+(str(dt.now())[:19]).replace(':', '_')+".txt"
    f = open(filename, 'a')
    if show:
        print(str(dt.now())[:19] + ': ' + msg)
    f.write(str(dt.now())[:19] + ': ' + msg + '\n')
    f.close()


#  COLISIONS
def circlesCollide(c1, c2):
    ((x1, y1), r1) = c1
    ((x2, y2), r2) = c2
    return sqrt((x1-x2)**2 + (y1-y2)**2) <= r1 + r2

def squaresCollide(s1, s2):
    (xi1, yi1, xf1, yf1) = s1
    (xi2, yi2, xf2, yf2) = s2
    return (xi2 <= xi1 <= xi2 or xi2 <= xf1 <= xi2) and (yi2 <= yi1 <= yi2 or yi2 <= yf1 <= yi2)

def pointInsideRect(r, p):
    (xir, yir, xfr, yfr) = r
    (xp, yp) = p
    return xir < xp < xfr and yir < yp < yfr



class ReadWriteLock():
    def __init__(self):
        self._readReady = Condition()
        self._readers = 0
        self._writes = 0

    def acquireRead(self):
        while self._writes > 0:
            self._readReady.wait()
        self._readReady.acquire()
        try:
            self._readers += 1
        finally:
            self._readReady.release()

    def releaseRead(self):
        self._readReady.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._readReady.notifyAll()
        finally:
            self._readReady.release()

    def acquireWrite(self):
        self._writes += 1
        self._readReady.acquire()
        while self._readers > 0:
            self._readReady.wait()

    def releaseWrite(self):
        self._writes -= 1
        self._readReady.release()