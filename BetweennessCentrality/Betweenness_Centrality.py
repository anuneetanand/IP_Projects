#!/usr/bin/env python3
#Name: Anuneet Anand
#Roll Number: 2018022
#Section: A
#Group: 6
#HW3 - Betweenness Centrality

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
	name = "Anuneet Anand"
	email = "anuneet18022@iiitd.ac.in"
	roll_num = "2018022"

	def __init__ (self, vertices, edges):
		"""
		Initializes object for the class Graph
		Args:
			vertices: List of integers specifying vertices in graph.
			edges: List of 2-tuples specifying edges in graph.
		"""
		self.vertices = vertices
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))        
		self.edges    = ordered_edges 
		self.validate()
		self.G=self.create_graph()		

	def validate(self):
		"""
		Validates if Graph if valid or not.
		Raises:
			Exception if:
				- Name is empty or not a string.
				- Email is empty or not a string.
				- Roll Number is not in correct format.
				- Vertices contains duplicates.
				- Edges contain duplicates.
				- Any endpoint of an edge is not in vertices.
			"""
		if (not isinstance(self.name, str)) or self.name == "":
			raise Exception("Name can't be empty")
		if (not isinstance(self.email, str)) or self.email == "":
			raise Exception("Email can't be empty")
		if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
			raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))
		if not all([isinstance(node, int) for node in self.vertices]):
			raise Exception("All vertices should be integers")
		elif len(self.vertices) != len(set(self.vertices)):
			duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])
			raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

		edge_vertices = list(set(itertools.chain(*self.edges)))

		if not all([node in self.vertices for node in edge_vertices]):
			raise Exception("All endpoints of edges must belong in vertices")
		if len(self.edges) != len(set(self.edges)):
			duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])
			raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

	def create_graph(self):
		''' Creates a graph for the vertices based on edges provided.
			Implemented using dictionary where nodes are keys and lists of neighbouring nodes are values.
		'''
		Y={}
		for i in self.vertices:
			x=[]
			for j in self.edges:
				if j[0]==i:
					x.append(j[1])
				if j[1]==i:
					x.append(j[0])
			Y[i]=x
		return Y

	def make_list(self,LSP,dist):
		'''
		To make proper list of path
		'''
		Y=[]
		X=[]
		for i in range(len(LSP)):
			X.append(LSP[i])
			if len(X)%(dist+1)==0:
				Y.append(X)
				X=[]
		return Y

	def min_dist(self, start_node, end_node):
		'''
		Finds minimum distance between start_node and end_node.
		Args:
			start_node: Vertex to find distance from.
			end_node: Vertex to find distance to.

		Returns:
			An integer denoting minimum distance between start_node and end_node.
		'''
		D={}							#Dictionary maintaining levels of nodes
		Q=[]
		V=[]
		Q.append(start_node)				
		V.append(start_node)			#To keep track of visited nodes
		D[start_node]=0					
		while len(Q):
			N=self.G[Q[0]]				#Neighbours of concerned node
			n=Q.pop(0)
			for i in N:
				if i not in V:
					Q.append(i)
					V.append(i)
					D[i]=D[n]+1
		return D[end_node],D

		raise NotImplementedError

	def all_paths(self, node, destination, dist, D, path):
		"""
		Finds all paths from node to destination with length = dist.
		Args:
			node: Node to find path from.
			destination: Node to reach.
			dist: Allowed distance of path.
			path: Path already traversed.
		Returns:
			List of path, where each path is list ending on destination.
			Returns None if there no paths.
		"""
		path.append(node)
		temp=list(path)
		if len(path)-1==dist:
			if node==destination:
				return path
			else:
				return None

		SP=[]				
		for i in self.G[node]: 				
			path=list(temp)
			if (i not in path) and (D[i]==D[node]+1):
				RP=self.all_paths(i,destination,dist,D,path)
			else:
				RP=None
			if RP!=None:
					SP=SP+RP

		if len(SP):
			return SP
		else:
			return None 
		raise NotImplementedError

	def all_shortest_paths(self, start_node, end_node):
		"""
		Finds all shortest paths between start_node and end_node.
		Args:
			start_node: Starting node for paths.
			end_node: Destination node for paths.
		Returns:
			A list of path, where each path is a list of integers.
		"""
		dist,D=self.min_dist(start_node,end_node)
		LSP=self.all_paths(start_node,end_node,dist,D,path=[])
		LSP=self.make_list(LSP,dist)
		return LSP
		raise NotImplementedError

	def betweenness_centrality(self, node):
		"""
		Find betweenness centrality of the given node.
		Args:
			node: Node to find betweenness centrality of.
		Returns:
			Single floating point number, denoting betweenness centrality
			of the given node.
		"""
		B=0							#Betweenness Centrality
		s=[]						#List of pairs checked
		for i in self.vertices:
			for j in self.vertices:
				z=[i,j]
				z.sort()
				if (i!=j) and (i!=node) and (j!=node) and (z not in s) : 
					ASP=self.all_shortest_paths(i,j)
					x=0			#No. Of Paths
					y=0			#No. Of Paths With Node
					for k in ASP:
						#print(node,i,j,ASP)
						if node in k:
							y=y+1
						x=x+1
					if x!=0:				
						B=B+y/x
					s.append(z)		#To Prevent repetition of a pair

		n=len(self.vertices)			
		SBC=(B*2)/((n-1)*(n-2))		#Standard Betweenness Centrality
		return SBC
		raise NotImplementedError

	def top_k_betweenness_centrality(self):
		"""
		Find top k nodes based on highest equal betweenness centrality.
		Returns:
		List of integers, denoting top k nodes based on betweenness centrality.
		"""
		BC={}						#Nodes & there Betweenness Centrality
		L=[]						#Nodes with highest Bewteenness Centrality
		m=0
		for x in self.vertices:
			y=self.betweenness_centrality(x)
			BC[x]=y
			if y>m:
				m=y
		#print(BC)
		for a in BC.keys():
			if BC[a]==m:
				L.append(a)
		L.sort()
		return L

		raise NotImplementedError

if __name__ == "__main__":
	vertices = [1, 2, 3, 4, 5, 6]
	edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 6), (4, 5), (4, 6)]
	graph = Graph(vertices,edges)
	print(graph.top_k_betweenness_centrality())

	#print(Graph([1,2,3,4,5,6,7],[(1,2),(1,3),(1,4),(2,3),(2,5),(2,6),(3,5),(4,7),(5,6),(6,7)]).top_k_betweenness_centrality())
	#print(Graph([1,2,3,4,5],[(1,2),(2,3),(2,5),(3,4),(3,5)]).top_k_betweenness_centrality())
	#print(Graph([1,2,3,4,5,6],[(1,2),(1,3),(1,4),(2,3),(2,5),(3,6),(4,5),(4,6),(5,6)]).top_k_betweenness_centrality())
	#print(Graph([1,2,3,4],[(1,2),(1,4),(2,3),(2,4),(3,4)]).top_k_betweenness_centrality())


