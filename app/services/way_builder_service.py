from models import Node
class WayBuilderService:
    def __init__(self, nodes):
        self.nodes = nodes
        self.visited = set()
        self.path = []

    def build_way(self, start, end):
        nodes =  self.find_path(start, end)
        edges = []
        for i in range(len(nodes)-1):
            edge = (Node.find_by_title(nodes[i].title, self.nodes), Node.find_by_title(nodes[i+1].title, self.nodes), nodes[i].distance_to(nodes[i+1]))
            edges.append(edge)
        return nodes, edges

    def find_path(self, start, end):
        self.path.append(start)
        self.visited.add(start)

        if start == end:
            return self.path
        
        for node in start.neighbours:
            if node not in self.visited:
                result = self.find_path(node[0], end)
                if result:
                    return result
                
        self.path.pop()
