from models import Node, Edge

class WayBuilderService:
    def __init__(self):
        self.nodes = Node.query.all()
        self.current_min_distance = 0

    def build_way(self, start, end):
        nodes = self.find_path(start, end) or []
        edges = Node.compose_edges(nodes) if nodes else []
        
        return (nodes, edges, Edge.calculate_overall_distance(edges))

    def find_all_paths(self, start_node, end_node):
        visited = set()
        paths = []
        shortest_distance = float('inf')

        def dfs(node, path, distance):
            nonlocal shortest_distance
            if node == end_node:
                paths.append((path, distance))
                if distance < shortest_distance:
                    shortest_distance = distance
                return

            if node in visited or distance > shortest_distance:
                return

            visited.add(node)

            for neighbor in node.neighbours():
                if neighbor not in visited:
                    dfs(neighbor, path + [neighbor], distance + node.distance_to(neighbor))

            visited.remove(node)

        dfs(start_node, [start_node], 0)

        return paths


    def find_path(self, start_node, end_node):
        all_paths = self.find_all_paths(start_node, end_node)

        if not all_paths:
            return None

        all_paths.sort(key=lambda x: x[1])
        shortest_path, shortest_distance = all_paths[0]

        return shortest_path
