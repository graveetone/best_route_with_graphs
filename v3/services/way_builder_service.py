from models import Node
class WayBuilderService:
    def __init__(self):
        self.nodes = Node.query.all()

    def build_way(self, start, end):
        paths = self.find_paths(start, end) # each path: list of nodes and distance
        paths = sorted(paths, key=lambda path: path[1]) # sort by distance

        result = []
        for path in paths:
            nodes, distance = path
            edges = Node.compose_edges(nodes)

            result.append((nodes, edges, distance)) # each element: tuple (nodes_list, edges_list, distance)
        
        return result


    def find_paths(self, start, end, distance=0, path=[]):
        path = path + [start]
        if len(path) > 1:
            distance = distance + path[-2].distance_to(start)

        if start == end:
            return [(path, distance)]

        paths = []
        for neighbor in start.neighbours():
            if neighbor not in path:
                new_paths = self.find_paths(neighbor, end, path=path, distance=distance)
                paths.extend(new_paths)
        return paths
