import math

def distance(a, b):
    dist = int(math.sqrt(abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)*10)
    return dist