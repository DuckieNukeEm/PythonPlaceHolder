#3.3
def right_justify(s):
	print( ' '*(10-len(s))+s)


#3.4
def do_twice(f,v):
	f(v)
	f(v)

def print_spam(s):
	print(s)
	print(s)

def do_four(f,v):
	do_twice(f,v)
	do_twice(f,v)


#3.5
def draw_dash():
	return('----+')
def draw_space():
	return('    |')

def draw_top(n):
	ret = '+'+draw_dash()*n
	return(ret)

def draw_inside(n):
	ret = '|' + draw_space()*n
	return(ret)

def draw_box(r,c):
	print(draw_top(c))
	for i in range(1,(5*r+1)):
		if i % 5 == 0:
			print(draw_top(c))
		else:
			print(draw_inside(c))

print("Now executing Exercixe 3")
right_justify('boob')
right_justify('bobby')


print("Now executing Exercise 4")
do_twice(print_spam, 'spam')

print('\n')
do_four(print_spam, 'spam')


print("Now working on Exercise 5")
draw_box(2,2)
draw_box(4,4)
