# from services.json_loader_service import JsonLoaderService
# from services.config_service import ConfigService
# from services.logger_service import Loger
from flask import current_app
# from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
import os
import matplotlib
matplotlib.use('Agg')
# from app import Node, Edge

class MapGeneratorService:
    # from models import Node, Edge

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        # self.nodes_to_highlight = nodes_to_highlight
        # self.edges_to_highlight = edges_to_highlight

        self.basic_map_image = mpimg.imread('static/map.png')

    def call(self, nodes_to_highlight, edges_to_highlight):
        self.nodes_to_highlight = nodes_to_highlight
        self.edges_to_highlight = edges_to_highlight
        # plt.ion()
        plt.cla()
        # self.load_nodes()
        # self.load_edges()
        self.compose_graph()
        self.fit_canvas()
        return self.save_image()

    # def load_nodes(self):
    #     self.nodes = Node.query.all()

    # def load_edges(self):
    #     self.edges = Edge.query.all()

        # for node in self.nodes:
            # for neighbour in node.neighbours:
                # self.edges.append((node, neighbour[0], neighbour[1]))


    def fit_canvas(self):
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                    hspace = 0, wspace = 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())


    def compose_edge_colors(self):
        # def edge_in_array(edge, array):
        #     for e in array:
        #         if e[0].title == edge[0].title and e[1].title == edge[1].title and e[2] == edge[2]:
        #             return True
        colors = []
        self.edge_widths = []

        for edge in self.edges:
            edge_is_chosen = edge in self.edges_to_highlight
            colors.append('red' if edge_is_chosen else 'black')
            self.edge_widths.append(2 if edge_is_chosen else 0.5)

        self.edge_colors = colors

    def compose_node_colors(self):
        colors = []
        
        for node in self.nodes:
            # import pdb; pdb.set_trace()
            colors.append('blue' if node in self.nodes_to_highlight else 'white')

        self.node_colors = colors


    def compose_graph(self):
        # self.load_nodes()
        # self.load_edges()

        titles = [node.title for node in self.nodes]
        positions = {node.title : [node.x, node.y] for node in self.nodes}

        self.graph = nx.Graph()
        self.graph.add_nodes_from(titles)
        self.graph.add_weighted_edges_from([(edge.start_node.title, edge.end_node.title, edge.weight) for edge in self.edges])

        self.compose_edge_colors()
        self.compose_node_colors()
        
        nx.draw_networkx_nodes(self.graph, positions, node_color=self.node_colors, node_size=50, edgecolors='black')
        nx.draw_networkx_edges(self.graph, positions, width=self.edge_widths, arrowsize=10, edge_color=self.edge_colors)
    
    def save_image(self):
        plt.imshow(self.basic_map_image)

        static_folder = current_app.static_folder
        filename = "frames/frame.png"
        path = os.path.join(static_folder, filename)
        # path = url_for('static', filename='frames/frame.png')#os.path.join(os.path.dirname(__file__), 'static', 'frames', 'frame.png')
        plt.savefig(path, dpi=600, bbox_inches='tight', pad_inches = 0)
        # print(path)
        return filename#os.path.realpath(path)
