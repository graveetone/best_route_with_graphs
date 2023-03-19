class WayBuilderService:
    def __init__(self, nodes):
        self.nodes = nodes
        self.visited = set()
        self.path = []

    def build_way(self, start, end):
        Node = type(self.nodes[0])
        Edge = type(self.nodes[0].edges()[0])

        nodes =  self.find_path(start, end)
        edges = []
        for i in range(len(nodes)-1):
            edge = Edge.query.filter_by(start_node=nodes[i], end_node=nodes[i+1]).first()
            edge = Edge.query.filter_by(start_node=nodes[i+1], end_node=nodes[i]).first() if not edge else edge
            edges.append(edge)
        return nodes, edges

    def find_path(self, start, end):
        self.path.append(start)
        self.visited.add(start)

        if start == end:
            return self.path
        
        for edge in start.edges(): #start.neighbours:
            node = edge.end_node
            node = edge.start_node if node == start else node
            if node not in self.visited:
                result = self.find_path(node, end)
                if result:
                    return result
                
        self.path.pop()
