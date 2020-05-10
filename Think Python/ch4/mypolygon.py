from swampy.TurtleWorld import *
import math
#creating a turtle world
world = TurtleWorld()

#creating a turtle (bob)
bob = Turtle()

print bob

#drawing a squar
def draw_square(t,n=100):
	for i in range(4):
		fd(t, n)
		lt(t)


def polygon(t,length = 10, n= 10):
	angle = float(360)/n
	for i in range(n):
		fd(t,length)
		lt(t, angle)

def circle(t,r):
	l = (2 * math.pi * r)/float(100)
	polygon(t, l, 100)

def arc(t, r, angle):
	l = (2 * math.pi * r)/float(100)
	n = int((float(360)/angle) * 100)
	polygon(t, l, n)

bob.delay = 0.001
print("drawing asquare")
#draw_square(bob,100)
print("drawing a  polygon")
#polygon(bob, 10, 8)
print("drawing a circle")
#circle(bob,20)
print("drawing arc")
arc(bob,420, 90)

wait_for_user()
