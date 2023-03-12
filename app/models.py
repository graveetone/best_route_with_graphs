from collections import namedtuple

Point = namedtuple('Point', 'x y')
Path = namedtuple('Path', 'start end')

class Node:
    
    def __init__(self, title, coordinates):
        self.title = title
        self.coordinates = Point(*coordinates)

    def add_neighbours(self, ns):
        self.neighbours = ns
    
    def __repr__(self):
        return f"Node <{self.title}> ({self.coordinates.x};{self.coordinates.y})"

    @staticmethod
    def from_dicts(dictionaries):
        nodes = []
        
        # iterate through node as objects in json
        for dictionary in dictionaries:
            # create node
            node = Node(
                title=dictionary['title'],
                coordinates=(dictionary['x'], dictionary['y'])
            )
            nodes.append(node)

        # iterate through node as objects in json
        for dictionary in dictionaries:
            # find current node in nodes as py object
            node = Node.find_by_title(dictionary['title'], nodes)

            # set neighbours of dict node and distances as existing py objects
            neighbours = [(Node.find_by_title(n['title'], nodes), n['distance']) for n in dictionary['neighbours']]
            node.add_neighbours(neighbours)
        
        return nodes

    @staticmethod
    def find_by_title(title, nodes):
        for node in nodes:
            if node.title == title:
                return node
            
    def distance_to(self, other):
        for n in self.neighbours:
            if n[0] == other:
                return n[1]



class Edge:
    _edges = []

    def __init__(self, start, end, distance):
        self.path = Path(start, end)
        self.distance = distance
        Edge._edges.append(self)

    def __repr__(self):
        start = self.path.start
        end = self.path.end
        return f"Edge from {start} to {end} with distance {self.distance}"
