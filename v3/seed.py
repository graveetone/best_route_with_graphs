from app import app, db
from models import Node, Edge
import json

JSON_FILENAME = 'nodes.json'


with open(JSON_FILENAME, encoding='utf-8-sig') as source:
    nodes = json.load(fp=source)

    nodes_to_save = []

with app.app_context():
    db.drop_all()
    db.create_all()
    
    for n in nodes:
        node = Node(
            title=n['title'],
            x=n['x'],
            y=n['y']
        )

        nodes_to_save.append(node)
    db.session.add_all(nodes_to_save)
    

    edges_to_save = []
    for n in nodes:
        title = n['title']
        node = Node.find_by_title(title)
        
        for neighbour in n['neighbours']:
            neighbour_title, weight = neighbour.values()

            neighbour_node = Node.find_by_title(title=neighbour_title)
            edge = Edge(
                start_node=node,
                end_node=neighbour_node,
                weight=weight
            )

        edges_to_save.append(edge)

    db.session.add_all(edges_to_save)
    db.session.commit()

print('Nodes and edges created successfully!')
