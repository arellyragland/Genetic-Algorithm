# coding: utf-8
import math
import random
import sys
from igraph import *
from collections import defaultdict

#This class represents a directed network
class Network:

    def __init__(self,vertices, pop):

        #No. of vertices
        self.V= vertices
        self.pop = pop

        # default dictionary to store network
        self.network = defaultdict(list)

    # function to add an edge to network
    def addEdge(self,u,v):
        self.network[u].append(v)

    def checkPath (self,child):
        i = 0
        while i < (len(child)-1):
            if not self.network[child[i]].__contains__(child[i+1]):
                return False 
            i +=1
        return True

    def findAllPathsUtil(self, u, d, visited, path):
        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u ==d:
            newPath = Path(0,False)
	    # Create a path Object
            for node in path:
                newPath.appendNode (node)
            # Add it to the population
            pop.appendPath(newPath)
        else:
            # If current vertex is not destination
            #Recur for all the vertices adjacent to this vertex
            for i in self.network[u]:
                if visited[i]==False:
                    self.findAllPathsUtil(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False

    # Prints all paths from 's' to 'd'
    def FindAllPaths(self, s, d):
        # Mark all the vertices as not visited
        visited =[False]*(self.V)
	self.pop.clearPaths()
        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.findAllPathsUtil(s, d,visited, path)
        
        #pop.printPaths()

class Path:
   def __init__(self, pathSize, initialise):
      self.path = []
      self.fitness = 0.0
      self.distance = 0
      if initialise:
         for i in range(0, pathSize):
            self.path.append(None)   
   def __len__(self):
      return len(self.path)
   
   def __getitem__(self, index):
      return self.path[index]
   
   def __setitem__(self, key, value):
      self.path[key] = value
   
   def __repr__(self):
      geneString = "|"
      return geneString
   
   def generateIndividual(self):
      random.shuffle(self.path)
   
   def getNode(self, pathPosition):
      return self.path[pathPosition]
   
   def appendNode(self, node):
      self.path.append(node)
   
   def setNode(self, pathPosition, node):
      self.path [pathPosition] = node 
      self.fitness = 0.0
      self.distance = 0
   
   def pathSize(self):
      return len(self.path)
   
   def containsNode(self, node):
      return node in self.path
   
   def isValidPath(self, src, dst):
      size = len(self.path)
      if (self.path[0]==src):
          if (self.path[size-1] == dst):
             return True
          else:
             return False
      else:
         return False 

   def printPath(self):
      for nodeIndex in range(0, self.pathSize()):
              #print (self.getNode(nodeIndex), end =' ')
              print (self.getNode(nodeIndex)),

   def comparePath (self, parent):
       for nodeIndex in range (0, self.pathSize()-1):
           if (self.getNode(nodeIndex) != parent.getNode(nodeIndex)):
               return False 
       return True

class Population:
   def __init__(self, populationSize, initialise):
      self.paths= []
      if initialise:    
          for i in range(0, populationSize):
              self.appendPath(None)
  
   def __setitem__(self, key, value):
      self.paths[key] = value
   
   def __getitem__(self, index):
      return self.paths[index]
   
   def savePath(self, index, tour):
      self.paths[index] = tour
   
   def appendPath(self, path):
      self.paths.append(path) 
   
   def getPath(self, index):
      return self.paths[index]
   
   def getInitial(self):
      initial= self.paths[0]
      return initial
   
   def populationSize(self):
      return len(self.paths)
   
   def printPaths (self):
      for i in range(0, self.populationSize()):
          self.getPath(i).printPath()
          print(" ")

   def containsPath (self, child):
      for j in range(0, self.populationSize()):
         parent = self.getPath(j)
         print ("Parent")	 
         print (parent.printPath())
         print ("Child")	 
         print (child.printPath())
         if (parent.comparePath(child) == True):
            return True
      return False

   def getFittest(self):
      fittest = self.paths[0]
      for i in range(0, self.populationSize()):
         if self.getPath(i).pathSize() <= fittest.pathSize(): 
            fittest = self.getPath(i)
      return fittest

   def clearPaths(self):
       self.paths = []

class GA:
   def __init__(self):
      self.mutationRate = 0.015
      self.populationSize = 5
      self.elitism = True
   
   def evolvePopulation(self, pop, src, dst,nw):
      newPopulation = Population(pop.populationSize(), False )
      elitismOffset = 0
      
      #print ("Creating the Parents...")
      for i in range(elitismOffset, pop.populationSize()):
         parent1 = self.pathSelection(pop)
         parent2 = self.pathSelection(pop)
         child = self.crossover(parent1, parent2)
         
         # Check if the child is valid before adding into the population
         if (child.isValidPath(src, dst) == True):
             if (nw.checkPath(child) == True):
                 newPopulation.appendPath(child)
      
#      for i in range(elitismOffset, newPopulation.populationSize()):
#         self.mutate(newPopulation.getPath(i))
      
      return newPopulation
   
   def crossover(self, parent1, parent2):
      if parent1.pathSize()<parent2.pathSize():
          size=parent1.pathSize()    	
      else:          
          size=parent2.pathSize()
      child = Path(size,True)
      
      startPos = int(random.random() * parent1.pathSize())
      endPos = int(random.random() * parent1.pathSize())
      for i in range(0, child.pathSize()):
         if startPos < endPos and i > startPos and i < endPos:
            child.setNode(i, parent1.getNode(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
              child.setNode(i, parent1.getNode(i))
      
      for i in range(0, parent2.pathSize()):
         if not child.containsNode(parent2.getNode(i)):
            for ii in range(0, child.pathSize()):
               if child.getNode(ii) == None:
                  child.setNode(ii, parent2.getNode(i))
                  break
      return child
   
   def mutate(self, path):
      for Pos1 in range(0, path.pathSize()):
         if random.random() < self.mutationRate:
            Pos2 = int(path.pathSize() * random.random())
            
            node1 = path.getNode(Pos1)
            node2 = path.getNode(Pos2)
            
            path.setNode(Pos2, node1)
            path.setNode(Pos1, node2)
   
   def pathSelection(self, pop):
      parentPop = Population(self.populationSize, False)
      for i in range(0, self.populationSize):
         randomId = int(random.random() * pop.populationSize())
         parentPop.appendPath(pop.getPath(randomId))
      fittest = parentPop.getFittest()
      return fittest



if __name__ == '__main__':
   
   # Defining the vertices
   vertices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
   
   # Defining the edges
   edges = [(0,1),(0,2),(2,8),(8,18),(17,18),(16,17),(15,16),(7,15),(5,7),(5,6),(6,11),(10,11),(9,10),(9,12),(12,14),(13,14),(1,13),(1,3),(3,4),(2,4),(1,2),(1,5),(2,5),(1,11),(5,11),(2,7),(7,8),(8,13),(8,15),(8,17),(11,15),(11,13),(13,15),(13,16),(1,9),(10,12),(12,13)]
   
   # Defining the list of colors for the nodes and edges
   color_dict = {"f": "green", "m": "red"}

   # Defining the graph elements
   g = Graph(vertex_attrs={"label": vertices}, edges=edges, directed=False)
   g.vs["color"] = ["m", "m","m", "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" ,"m"]
   g.es["color"] = ["m", "m","m", "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" , "m" ,"m"]

   # Initialize the Population Class 
   pop = Population(0, False);

   # Initialize the GA Class
   ga = GA()
   dist=0
   solution = []
   vertex = []
   edge = [] 
   # Create a network given in the above diagram
   nw = Network(19,pop)
 
   # Get the first parameter for network file 
   param_1= sys.argv[1]
   param_2 = int(sys.argv[2])
   vertex.append(param_2)

   # Add the connection to each node
   nwfile = open(param_1, 'r') 
   while True:
       line = nwfile.readline().strip()
       if line == '':
        # either end of file or just a blank line.....
        # we'll assume EOF, because we don't have a choice with the while loop!
            break
       splits = line.split()
       #print (splits[0], splits[1])
       src = int(splits[0])
       dst = int(splits[1])
       nw.addEdge(src,dst)
       nw.addEdge(dst,src)
   
   print (nwfile.read(3)) 
   nwfile.close()

   # Printing the number of arguments and the number of nodes 
   print ("Number of arguments is " + str(len(sys.argv)))
   nodeSize = len(sys.argv) - 2
   print ("Number of nodes to traverse is " + str(nodeSize))
   
   solution.append(int(sys.argv[2]))

   # Looping through the connection nodes 
   for x in range(1,nodeSize):
       param_2= sys.argv[x+1]
       param_3= sys.argv[x+2]
       value1 = int(param_2)
       value2 = int(param_3)
       #g.vs[value1]["color"]="f"
   
       # Initialize population
       nw.FindAllPaths(value1, value2)
         
       print ("\nInitial Populations Size: " + str(pop.populationSize()))
       print ("First Path before applying Genetic Algorithm: ")
       print ( pop.getInitial().printPath())
       print ("First distance before applying Genetic Algorithm: " + str(pop.getInitial().pathSize())) 
       
       #print ("Initial Populations")
       #pop.printPaths()
  
       # Evolve population for configurable generations
       pop = ga.evolvePopulation(pop, value1, value2,nw)
       for i in range(0, 50):
           pop = ga.evolvePopulation(pop, value1, value2, nw)
       dist += pop.getFittest().pathSize()-1    
       
       # Adding the solution to the list       
       final = pop.getFittest()
       for nodeIndex in range(1, final.pathSize()):
            solution.append (final.getNode(nodeIndex))

       # Populating the edge and vertex index for coloring
       for nodeIndex in range(0, (final.pathSize()-1)):
           vertex.append (final.getNode(nodeIndex+1))
           edge.append ( g.get_eid(final.getNode(nodeIndex),final.getNode(nodeIndex+1)))
 
   # Print final results
   print ("\n\nGenetic Algorithm Finished...")
   print ("Final Distance: " + str(dist))
   print ("Final Solution:")
   print (solution)

   # Changing color for edge and vertex
   for i in range (0,len(vertex)):
       g.vs[vertex[i]]["color"]="f"

   for i in range (0, len(edge)):
       g.es[edge[i]]["color"]="f"

   # Drawing the Graph
   visual_style = {}
   visual_style["edge_color"]= [color_dict[color] for color in g.es["color"]]
   visual_style["vertex_color"]= [color_dict[color] for color in g.vs["color"]]
       
   # Plotting the Graph 
   plot(g, **visual_style)
