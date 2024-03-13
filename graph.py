import math
import heapq
import random
from vertex import Vertex
from edge import Edge

class Graph:
    def __init__(self, num_vertices, num_edges, max_weight):
        self.vertices = {}  # Dictionary to store vertices and their associated edges
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.max_weight = max_weight
        self.goal_vertex = None
        self.heuristic = None
        self.generate_random_graph(num_vertices, num_edges, max_weight)

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        if vertex.name not in self.vertices:
            self.vertices[vertex.name] = {}

    def add_edge(self, from_vertex, to_vertex, weight=1):
        """
        Add a directed edge from one vertex to another with an optional weight.
        """
        if from_vertex.name not in self.vertices:
            self.add_vertex(from_vertex)
        if to_vertex.name not in self.vertices:
            self.add_vertex(to_vertex)
        if to_vertex.name not in self.vertices[to_vertex.name]:
            self.vertices[from_vertex.name][to_vertex.name] = Edge(from_vertex, to_vertex, weight)

    def get_neighbors(self, vertex):
        """
        Get the neighbors of a vertex.
        """
        if vertex.name in self.vertices:
            return list(self.vertices[vertex.name].keys())
        return []

    def get_edge_weight(self, from_vertex, to_vertex):
        """
        Get the weight of the edge from one vertex to another.
        """
        if from_vertex.name in self.vertices and to_vertex.name in self.vertices[from_vertex.name]:
            return self.vertices[from_vertex.name][to_vertex.name].weight
        return None

    @property
    def goal(self):
        """
        Property to access the goal vertex.
        """
        return self.goal_vertex

    def generate_random_graph(self, num_vertices, num_edges, max_weight):
        """
        Generate a random graph with a given number of vertices and edges.
        """
        for i in range(num_vertices):
            vertex = Vertex(str(i))
            self.add_vertex(vertex)

        for _ in range(num_edges):
            from_vertex_name = str(random.randint(0, num_vertices - 1))
            to_vertex_name = str(random.randint(0, num_vertices - 1))
            weight = random.randint(1, max_weight)  # Random weight between 1 and 10
            from_vertex = Vertex(from_vertex_name)
            to_vertex = Vertex(to_vertex_name)
            self.add_edge(from_vertex, to_vertex, weight)

        # Randomly select a goal vertex
        goal_vertex_name = str(random.randint(0, num_vertices - 1))
        self.goal_vertex = Vertex(goal_vertex_name)
        self.heuristic = self.compute_noisy_heuristics(noise = 2)



    def dijkstra(self):
        """
        Dijkstra's algorithm to compute the shortest distances from the start vertex to all other vertices.
        """
        dijkstra_distances = {}
        dijkstra_distances[self.goal_vertex.name] = 0
        for i in self.vertices:
            if(i == self.goal_vertex.name): continue
            start_name = i
            distances = {vertex_name : float('inf') for vertex_name in self.vertices.keys()}
            distances[start_name] = 0
            pq = [(0, start_name)]

            while pq:
                curr_dist, curr_vertex = heapq.heappop(pq)
                if curr_dist > distances[curr_vertex]:
                    continue
                for neighbor, edge in self.vertices[curr_vertex].items():
                    new_dist = curr_dist + edge.weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))

            dijkstra_distances[start_name] = distances[self.goal_vertex.name]
        return dijkstra_distances


    def noisy_heuristic(self,vertex, dijkstra_distances, noise):
        """
        Compute a noisy heuristic by adding random noise to the distance obtained from Dijkstra's algorithm.
        """
        base_distance = dijkstra_distances[vertex]
        rand_noise = random.uniform(0, noise)  # Adjust the range of noise as needed
        # Ensure the heuristic is non-negative
        return max(0, base_distance - rand_noise)


    def compute_noisy_heuristics(self, noise = 2):
        """
        Compute noisy heuristic values for each vertex in the graph based on Dijkstra's algorithm with added noise.
        """
        heuristics = {}
        dijkstra_distances = self.dijkstra()
        self.dijkstra_distances = dijkstra_distances

        for vertex_name in self.vertices.keys():
            # vertex = self.vertices[vertex_name]
            heuristic = self.noisy_heuristic(vertex_name, dijkstra_distances, noise)
            heuristics[vertex_name] = heuristic

        return heuristics


