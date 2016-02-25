from math import cos, sin, pi, fabs

def isBetween(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if abs(crossproduct) > 0.1 : return False   # (or != 0 if using integers)

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0 : return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba: return False

    return True

def intersectLineRay(s, e, p, t): 
	print str(s) + ' ' + str(e) + ' ' + str(p) + ' ' + str(t)
	a = e.y - s.y
	b = e.x - s.x
	c = s.x - p.x
	d = s.y - p.y
	det = (cos(t)*(e.y - s.y) - sin(t)*(e.x - s.x)) 
	print a, b, c, d, det
	if det == 0.0:
		return None
	m = ((a*c) - (b*d)) /det 
	print m
        if(m <= 0.0): 
                return None 
	intx = cos(t)*m + p.x
	inty = sin(t)*m + p.y
	print intx, inty
	if not isBetween(s, e, Point(intx, inty)):
		return None
        return m 

                 
def getMappedDepth(position, angle): 
	depth = float('inf') 
        for line in lines: 
		newDepth = intersectLineRay(line[0], line[1], position, angle) 
		print newDepth
        	if(newDepth != None and newDepth < depth): 
			depth = newDepth 
	return depth 

class Point:
	def __init__(self, x, y):
        	self.x = x
                self.y = y
	def __str__(self):
		return '('+str(self.x) + ',' + str(self.y)+')'

lines =  [\
                        (Point(0.00, 0.00), Point(0.00, 1.68)), \
                        (Point(0.00, 1.68), Point(0.84, 1.68)), \
                        (Point(0.84, 1.26), Point(0.84, 2.10)), \
                        (Point(0.84, 2.10), Point(1.68, 2.10)), \
                        (Point(1.68, 2.10), Point(1.68, 0.84)), \
                        (Point(1.68, 0.84), Point(2.10, 0.84)), \
                        (Point(2.10, 0.84), Point(2.10, 0.00)), \
                        (Point(2.10, 0.00), Point(0.00, 0.00))  \
                ] 


print getMappedDepth(Point(0.83, 0.30), pi/2)

