"""Tileset visualiser by Akira Baes
This version works with manually-inserted tile representations in the code. 
Here I have: tetrahedron, cube, pyramid
A future version should interface with a tile-representation-generator directly

First, "extend" show the representation of a single tile with its neighbouring tiles infos

"fill_screen" then fill the screen with the given tile to verify that it is a tile

"explore" is supposed to find all the places that can be rolled into, with a stopping condition when reaching a position+orientation that has already been met,
but it is rather difficult to read to determine if it can roll in the space or not. 
"""

from tkinter import *
from Point import Point
from time import sleep
from math import pi
root = Tk(className ="Shapes representation") #add a root window named Myfirst GUI
WIDTH = 1000
HEIGHT = 800
graph = Canvas(root, width=WIDTH, height=HEIGHT) # add a label to root window
graph.pack()

#Represent the faces of the 3D shape that can be rolled
#Each shape gives its neighbours
J1R = { #order is clockwise (but unimportant here)
	0: [1,2,3,4],
	1: [0,4,2],
	2: [1,3,0],
	3: [0,2,4],
	4: [0,3,1]
}

p = 5
#Represents the cases of the 2D net that tiles the space
#The neighbours outside of the net are represented by their ID + k*p (p being bigger than the number of polygons)
#A same outside shape has a same k. For example, for the pyramid, there are 4 different shapes
#A shape that is on one side and on the other is k*p on one side and -k*p on the other side (for easy symmetry)
#The representation is recursive, meaning the ID+k*p part can be further be explored as part of a full net as (ID + k*p-1)%p+1 = ID
#This is a simple representation, but all the tiles that I can see from the document follow this pattern
J1N = { #order is clockwise
	0: [1,0-p,3,0+p],
	1: [0,2+p,2],
	2: [1,4+2*p,1-p],
	3: [0,4-p,4],
	4: [3+p,3,2-2*p]
}

tetraR = {
	0: [1,2,3],
	1: [2,0,3],
	2: [0,1,3],
	3: [0,2,1]
}

p=4
tetraN = {
	0: [1,2,3],
	1: [3-p,2-2*p,0],
	2: [0,1+2*p,3-3*p],
	3: [0,2+3*p,1+p]
}

p=6

cubeR = {
	0: [1,2,4,3],
	1: [0,3,5,2],
	2: [0,1,5,4],
	3: [0,4,5,1],
	4: [0,2,5,3],
	5: [1,3,4,2]
}


cubeN = {
	0: [1,2,4,3],
	1: [0,2-p,5,5+2*p],
	2: [0,5+2*p,1+p,3+p],
	3: [0,4+p,4+2*p,2-p],
	4: [0,3-2*p,3-p,4],
	5: [5,2-2*p,1-2*p,1]
}
#Here, an exception, 5 goes to 5 symmetrically and 6 goes to 6 symmetrically

J1 = 0
tetra = 1
cube = 2

Rolls = [J1R, tetraR, cubeR]
Nets = [J1N, tetraN, cubeN]

current = cube #####

roll = Rolls[current]
net = Nets[current]
	
def pointAngle(a,b,c):
	#Course formula: [AB]x[BC] product
	return ((b.x-a.x)*(c.y-b.y) - (b.y-a.y)*(c.x-b.x));


def square(p1,p2):
	#creates a rectangle clockwise to p1,p2
	p1 = p1
	p2 = p2
	
	p34 = p1-p2
	p3 = p2 + Point(p34.y,-p34.x)
	p4 = p3+p34
	return round(p1),round(p2),round(p3),round(p4)
	
def triangle(p1,p2):
	#creates a triangle clockwise to p1,p2
	p1 = p1
	p2 = p2
	p3 = p1 + (p2-p1).rotate(pi/3)
	"""pb = p1 + ((p2-p1)/2)
	ph = 
	dist = (p2-p1)"""
	return round(p1),round(p2),round(p3)
	
def hexagon(p1,p2):
	#creates a triangle clockwise to p1,p2
	p1 = p1
	p2 = p2
	sol = [round(p1), round(p2)]
	pa = p1
	pb = p2
	for i in range(4):
		pn = pb + (pa-pb).rotate(-2*pi/3)
		sol.append(round(pn))
		pa = pb
		pb = pn
	"""pb = p1 + ((p2-p1)/2)
	ph = 
	dist = (p2-p1)"""
	return sol
	
colors = ("black","red","yellow","cyan","magenta","blue","green")
def make(points,color=0):
	#Creates a shape from given points
	list = []
	w = 2+(color==0)*2
	#print(color)
	c = colors[color%len(colors)]
	for i,point in enumerate(points):
		next = points[(i+1)%len(points)]
		list.append(graph.create_line((point.x,point.y),(next.x,next.y),fill=c,width=w))
	return list

def makefull(points,color=0):
	c = colors[color%len(colors)]
	return graph.create_polygon([(p.x,p.y) for p in points], fill=c) 
	
	
def makefill(points,color=0,full=False):
	if(full):
		s = ""
	else:
		s = "gray50"
	c = colors[color%len(colors)]
	return graph.create_polygon([(p.x,p.y) for p in points], fill=c, stipple=s) 
	
def number(id,point):
	graph.create_text((point.x,point.y),text=str(id))
def numcenter(id,points):
	number(id,sum(points,Point(0,0))/len(points))
def numbours(id,neighbours,points):
	m=sum(points,Point(0,0))/len(points)
	number(id,m)
	for i in range(len(neighbours)):
		p1 = points[i]
		p2 = points[(i+1)%len(points)]
		p = ((p1+p2)/2+m)/2
		number(neighbours[i]%len(order),p)

"""i = w.create_line(xy, fill="red")
w.coords(i, new_xy) # change coordinates
w.itemconfig(i, fill="blue") # change color

w.delete(i) # remove"""

p1 = Point(300,300)
p2 = Point(350,300) #350 300



		

shape = net
shapes = []
shapespoly = []
order = sorted(shape)

class Poly:
	def __init__(self,id,points, color=None, full=False):
		self.n = []
		self.id = id
		self.points = points
		realid = id%len(order)
		if(full):
			self.pid = makefull(points,color)
		elif(color==None):
			self.pid = make(points,(int((id-realid)/len(order)))%len(colors))
		else:
			self.pid = make(points,color%len(colors))
		#print(points)
		number(realid,sum(points,Point(0,0))/len(points))
		
	def order(self,neighbor):
		index = self.n.index(neighbor)
		return self.n[neighbor:]+self.n[:neighbor]
	def fill(self,neighbours):
		self.n = list(neighbours)
	def __eq__(self,other):
		return self.id == other
	def has_points(self,pts):
		#print(sorted(self.points),sorted(pts),sorted(self.points)==sorted(pts))
		return sorted(self.points)==sorted(pts)
	def remplis(self, color = "red"):
		graph.create_polygon([(p.x,p.y) for p in self.points], fill=color,stipple="gray50") 
	def __repr__(self):
		return str(self.points)

def get_face_points(p1,p2,face, noisy=True):
	faceid = face%len(order)
	if(len(shape[faceid]))==3:
		points = triangle(p1,p2)
		if(noisy): print(" triangle ",face)
	elif(len(shape[faceid]))==4:
		points = square(p1,p2)
		if(noisy): print(" square ",face)
	else:
		points = hexagon(p1,p2)
		if(noisy): print(" hexagon ",face)
	return points
	

	
def visualise(p1,p2,newshape,oldshape, color = 0, drawnshapes = None, shapespoly = None):
	#Copy of extend, but fills the whole space
	realshape = newshape%len(order)
	if(drawnshapes==None):
		drawnshapes = list()
		#print("Visualise---------",newshape,oldshape,shape[realshape])
	if(shapespoly==None):
		shapespoly = list()
	points = get_face_points(p1,p2,newshape,False)
	shapespoly.append(Poly(newshape,points,color,True))
	current = shape[realshape]
	index = current.index(oldshape)
	current =  current[index:]+current[:index]
	shapespoly[-1].fill(current)
	drawnshapes.append(realshape)
	
	root.update()
	#sleep(0.1)
	#print("I have",len(points),"points")
	#if(newshape==realshape):
	#print("Next ones:",current)
	for index,p in enumerate(current):
		#print("Looking",p)
		#print(index)
		p1 = points[index%len(points)]
		p2 = points[(index+1)%len(points)]
		if (p not in drawnshapes) and (p%len(order)==p):
			visualise(p2,p1,p,newshape,color,drawnshapes,shapespoly)
		"""else:
			if(p in drawnshapes):
				print("P in drawn:",p,drawnshapes,p not in drawnshapes)
			if(p%len(order)!=p):
				print("P not to draw",p,p%len(order))"""
	return shapespoly
	
def extend2(p1,p2,newshape,oldshape=None, drawnshapes = None, shapespoly=None):
	if(drawnshapes==None):
		drawnshapes = list()
	if(shapespoly==None):
		shapespoly = list()
	print(end="Draw the")
	realshape = newshape%len(order)
	if(len(shape[realshape]))==3:
		points = triangle(p1,p2)
		print(" triangle ",newshape)
	elif(len(shape[realshape]))==4:
		points = square(p1,p2)
		print(" square ",newshape)
	else:
		points = hexagon(p1,p2)
		print(" hexagon ",newshape)
		
	current = shape[realshape]
	if(oldshape==None):
		oldshape = -current[0] + 2*(current[0]%len(order))
	if(oldshape!=None and newshape==realshape):
		#print(oldshape,"in",current,newshape,realshape)
		index = current.index(oldshape)
		current =  current[index:]+current[:index]
		print("Previous:",oldshape,"Next:",current)
	drawnshapes.append(newshape)
	root.update()
	sleep(0.1)
	#print("I have",len(points),"points")
	if(newshape==realshape):
		shapespoly.append(Poly(newshape,points))
		shapespoly[-1].fill(current)
		for index,p in enumerate(current):
			#print(index)
			p1 = points[index%len(points)]
			p2 = points[(index+1)%len(points)]
			if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
				###[TODO] ici pose problème de retourner à même shape
				#print(p,shapes)
				#print("Work",newshape)
				if(p==newshape):
					p+=len(order)
				extend2(p2,p1,p,newshape,drawnshapes,shapespoly)
	else:
		visualise(p1,p2,newshape,oldshape)
				
def extend(p1,p2,newshape,oldshape=None, drawnshapes = None, shapespoly=None):
	if(drawnshapes==None):
		drawnshapes = list()
	if(shapespoly==None):
		shapespoly = list()
	print(end="Draw the")
	realshape = newshape%len(order)
	if(len(shape[realshape]))==3:
		points = triangle(p1,p2)
		print(" triangle ",newshape)
	elif(len(shape[realshape]))==4:
		points = square(p1,p2)
		print(" square ",newshape)
	else:
		points = hexagon(p1,p2)
		print(" hexagon ",newshape)
		
	shapespoly.append(Poly(newshape,points))
	current = shape[realshape]
	if(oldshape!=None and newshape==realshape):
		#print(oldshape,"in",current,newshape,realshape)
		index = current.index(oldshape)
		current =  current[index:]+current[:index]
		print("Previous:",oldshape,"Next:",current)
	shapespoly[-1].fill(current)
	drawnshapes.append(newshape)
	
	root.update()
	sleep(0.1)
	#print("I have",len(points),"points")
	if(newshape==realshape):
		for index,p in enumerate(current):
			#print(index)
			p1 = points[index%len(points)]
			p2 = points[(index+1)%len(points)]
			if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
				###[TODO] ici pose problème de retourner à même shape
				#print(p,shapes)
				#print("Work",newshape)
				if(p==newshape):
					p+=len(order)
				extend(p2,p1,p,newshape,drawnshapes,shapespoly)
		
def point_outside(point):
	x,y = point.x,point.y
	if(x<0 or y<0 or x>WIDTH or y>HEIGHT):
		return True
		
def points_outside(points):
	for point in points:
		if(point_outside(point)):
			return True
	return False

def swap(oldshape):
	return -oldshape+2*(oldshape%len(order))
def rest(oldshape):
	return oldshape-(oldshape%len(order))
def real(shape):
	return shape%len(order)

def fill_screen(p1,p2,newshape,oldshape=None, exploredpoints=None, drawnpoly=None, color = 3):
	if(exploredpoints==None):
		exploredpoints = list()
	if(drawnpoly==None):
		drawnpoly = list()
	realshape = newshape%len(order)
	if(realshape!=newshape):
		print("Erreur de paramètre....",realshape,newshape)
	points = get_face_points(p1,p2,newshape,False)
	#Poly(newshape,points)
	if(points_outside(points)):
		return
	for face in exploredpoints:
		if sorted(face)==sorted(points):
			return
	exploredpoints.append(points)
	current = shape[realshape]
	if(oldshape==None):
		oldshape = -current[0] + 2*(current[0]%len(order))
	#if(oldshape!=None and newshape==realshape): #on explore même quand on est dehors
		#print(oldshape,"in",current,newshape,realshape)
	index = current.index(oldshape)
	current =  current[index:]+current[:index]
	#print("Previous:",oldshape,"Next:",current)
	root.update()
	#sleep(0.5)
	#print("I have",len(points),"points")
	#if(newshape==realshape):
	drawn = False
	for poly in drawnpoly:
		if(poly.has_points(points)):
			drawn = True
	if not drawn:
		#print("Not yet drawn")
		#print(drawnpoly)
		drawnpoly+= visualise(p1,p2,newshape,oldshape, color) 
		#print(drawnpoly[-1])
		color+=1
		#print("Finished drawing")
	for index,p in enumerate(current):
		#print(index)
		p1 = points[index%len(points)]
		p2 = points[(index+1)%len(points)]
		"""if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
			###[TODO] ici pose problème de retourner à même shape
			#print(p,shapes)
			#print("Work",newshape)
			if(p==newshape):
				p+=len(order)"""
		#print("Do I explore ",realshape," to ",p,"(",p%len(order),") ?")
		if((p%len(order)==p) and (p%len(order)!=realshape)):
			#print("Yes")
			fill_screen(p2,p1,real(p),newshape-rest(p),exploredpoints,drawnpoly,color)
			
	for index,p in enumerate(current):
		#print(index)
		p1 = points[index%len(points)]
		p2 = points[(index+1)%len(points)]
		"""if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
			###[TODO] ici pose problème de retourner à même shape
			#print(p,shapes)
			#print("Work",newshape)
			if(p==newshape):
				p+=len(order)"""
		if((p%len(order)!=p) or p%len(order)==realshape):
			color+=1
			fill_screen(p2,p1,real(p),newshape-rest(p),exploredpoints,drawnpoly,color)
#draw_tile(p1,p2,order[0],1)	
#visualise(p1,p2,order[0])			
extend(p1,p2,order[0])
sleep(1)
graph.delete("all")
fill_screen(p1,p2,order[0])
root.update()
#sleep(0.5)

graph.delete("all")

"""
Two things:
the face, and the orientation
The orientation = current face (its shape) and order

For example, we went 2-3 on the net, and 4-1 on the shape

So on face 3, if face 3 is 2,4,6, we note, 4,X,X (the important part is the 4 at the beginning of the 1 face, matching the order in face 3)
We re-order them from the smallest face, so that it always matches

Same orientation as beginning: fill the normal set
Then go into a new set: until meet an orientation that we already met before, then stop


Algo:
If orientation is not in face
	Add orientation in face (and draw it)
	Try out possible rolls (same shape, adjacent)
else:
	found (draw it differently)
"""
print("#"*30)

orientations = dict()
for face in roll:
	orientations[face] = []
start = 1
#case = part of J1 net on which we are rolling
#face = part of J1R polyhedron which is looking at the floor
def explore(p1,p2,case,face,previouscase=None,previousface=None):
	print("Exploring",previouscase,"-",case,"with face",previousface,"-",face)
	
	#else same shape
	if(len(roll[face])==3):
		points = triangle(p1,p2)
	elif(len(roll[face])==4):
		points = square(p1,p2)
	else:
		points = hexagon(p1,p2)
		
	if(len(net[case]) != len(roll[face])):
		make(points,-2)
		#different shapes: incompatible
		return
		
	currentCaseNeighbours = net[case]
	currentFaceNeighbours = roll[face]
	if(previouscase!=None):
		#décalage : previouscase n'est pas le bas, le bas réel l'est: on fait l'inverse de la rotation pour qu'elle y soit
		print(currentCaseNeighbours)
		caseOrientation = currentCaseNeighbours.index(previouscase) #décalage actuel par rapport à la normale
		points = points[-caseOrientation:]+points[:-caseOrientation]
		#currentCaseNeighbours = currentCaseNeighbours[caseOrientation:] + currentCaseNeighbours[:caseOrientation]
		
		#décalage : previousface doit être le bas: on fait une rotation pour qu'elle y soit
		faceOrientation = currentFaceNeighbours.index(previousface)
		#décalage: la face du bas doit être la même que celle de l'orientation que la case
		faceOrientation = (faceOrientation - caseOrientation)%len(order)
		currentFaceNeighbours = currentFaceNeighbours[faceOrientation:] + currentFaceNeighbours[:faceOrientation]
	orientation = currentFaceNeighbours
	print("My orientation is",orientation)
	if(orientation in orientations[case]):
		#already visited like this
		makefill(points,-1,True)
		make(points,2)
		numbours(case,currentCaseNeighbours,points)
		return
	elif(points_outside(points)):
		return
	else:
		make(points)
		makefill(points,1)
		numbours(case,currentCaseNeighbours,points)
		orientations[case].append(orientation)
		for i in range(len(currentFaceNeighbours)):
			print(i)
			nextcasereal = currentCaseNeighbours[i]
			nextface = currentFaceNeighbours[i]
			p1 = points[i%len(points)]
			p2 = points[(i+1)%len(points)]
			nextcase = nextcasereal%len(order)
			difference = nextcasereal-nextcase
			if(nextface!=previousface):
				root.update()
				sleep(0.05)
				explore(p2,p1,nextcase,nextface,case-difference,face)
			
explore(p1,p2,0,0)
print("Finished!")
for face in sorted(orientations):
	print("orientations found for face",face,":", len(orientations[face]))
	print(orientations[face])
root.mainloop()