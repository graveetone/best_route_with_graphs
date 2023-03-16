from flask import current_app

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib

import networkx as nx

import os
import uuid

matplotlib.use('Agg')

class MapGeneratorService:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

        self.basic_map_image = mpimg.imread('static/map.png')

    def call(self, nodes_to_highlight, edges_to_highlight):
        self.nodes_to_highlight = nodes_to_highlight
        self.edges_to_highlight = edges_to_highlight

        plt.cla()

        self.compose_graph()
        self.fit_canvas()
        return self.save_image()

    def fit_canvas(self):
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                    hspace = 0, wspace = 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())


    def compose_edge_colors(self):
        self.edge_widths = []
        self.edge_colors = []

        for edge in self.edges:
            edge_is_chosen = edge in self.edges_to_highlight
            
            self.edge_colors.append('red' if edge_is_chosen else 'black')
            self.edge_widths.append(2 if edge_is_chosen else 0.5)

    def compose_node_colors(self):
        colors = []
        
        for node in self.nodes:
            colors.append('blue' if node in self.nodes_to_highlight else 'white')

        self.node_colors = colors


    def compose_graph(self):
        titles = [node.title for node in self.nodes]
        positions = {node.title : [node.x, node.y] for node in self.nodes}

        self.compose_node_colors()
        self.compose_edge_colors()

        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(titles)
        self.graph.add_weighted_edges_from([(edge.start_node.title, edge.end_node.title, edge.weight) for edge in self.edges])
        
        nx.draw_networkx_nodes(self.graph, positions, node_color=self.node_colors, node_size=50, edgecolors='black')
        nx.draw_networkx_edges(self.graph, positions, width=self.edge_widths, edge_color=self.edge_colors, arrows=False)

        edge_labels = nx.get_edge_attributes(self.graph, 'weight')

        # nx.draw_networkx_edge_labels(self.graph, pos=positions, edge_labels=edge_labels, font_size=6, font_color='white', bbox=dict(boxstyle='round',facecolor='black', edgecolor='none'), label_pos=0.5)

    def save_image(self):
        plt.imshow(self.basic_map_image)

        static_folder = current_app.static_folder
        filename = f"frames/{uuid.uuid4()}.png"
        path = os.path.join(static_folder, filename)
        plt.savefig(path, dpi=600, bbox_inches='tight', pad_inches = 0)
        return filename
