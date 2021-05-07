import math

def distance(a, b):
    # Calculate the distance between two cells using the Pythagoras' theorem
    dist = int(math.sqrt(abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)*10)
    return dist