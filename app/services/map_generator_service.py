from services.json_loader_service import JsonLoaderService
from services.config_service import ConfigService
from services.logger_service import Loger

from models import Node, Edge
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
import os

class MapGeneratorService:
    def __init__(self, nodes_to_highlight, edges_to_highlight):
        self.nodes_to_highlight = nodes_to_highlight
        self.edges_to_highlight = edges_to_highlight

        self.basic_map_image = mpimg.imread(ConfigService.MAP_FILEPATH)

    def call(self):
        plt.cla()
        self.load_nodes()
        self.load_edges()
        self.compose_graph()
        self.fit_canvas()
        return self.save_image()

    def load_nodes(self):
        self.nodes = Node.from_dicts(JsonLoaderService(ConfigService.NODES_FILEPATH).load())

    def load_edges(self):
        self.edges = []

        for node in self.nodes:
            for neighbour in node.neighbours:
                self.edges.append((node, neighbour[0], neighbour[1]))


    def fit_canvas(self):
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                    hspace = 0, wspace = 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

    def compose_edge_colors(self):
        def edge_in_array(edge, array):
            for e in array:
                if e[0].title == edge[0].title and e[1].title == edge[1].title and e[2] == edge[2]:
                    return True
        colors = []
        self.edge_widths = []

        for edge in self.edges:
            colors.append('red' if edge_in_array(edge, self.edges_to_highlight) else 'black')
            self.edge_widths.append(2 if edge_in_array(edge, self.edges_to_highlight) else 0.5)

        self.edge_colors = colors 

    def compose_node_colors(self):
        colors = []
        
        for node in self.nodes:
            colors.append('blue' if Node.find_by_title(node.title, self.nodes_to_highlight) else 'white')

        self.node_colors = colors


    def compose_graph(self):
        self.load_nodes()
        self.load_edges()

        titles = [node.title for node in self.nodes]
        positions = {node.title : [*node.coordinates] for node in self.nodes}

        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(titles)
        self.graph.add_weighted_edges_from([(e[0].title, e[1].title, e[2]) for e in self.edges])

        self.compose_edge_colors()
        self.compose_node_colors()
        
        nx.draw_networkx_nodes(self.graph, positions, node_color=self.node_colors, node_size=50, edgecolors='black')
        nx.draw_networkx_edges(self.graph, positions, width=self.edge_widths, arrowsize=10, edge_color=self.edge_colors)
    
    def save_image(self):
        plt.imshow(self.basic_map_image)

        path = os.path.join(os.path.dirname(__file__), '..', 'frames', 'frame.png')
        plt.savefig(path, dpi=500, bbox_inches='tight', pad_inches = 0)
        
        return os.path.realpath(path)
