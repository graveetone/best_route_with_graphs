import json
from models import Node

with open('nodes.json', encoding='utf-8-sig') as file:
    nodes = json.load(file)

nodes = [Node(node['id'], node['title'], coordinates=(node['x'], node['y'])) for node in nodes]

def find_node_by_title(title):
    for node in nodes:
        if node.title == title:
            return node
        
def get_node_id(title):
    node = find_node_by_title(title)
    return node and node.id
    


with open('nodes.txt', encoding="utf-8") as raw:
    lines = raw.readlines()
    with open('graph.json', 'w') as cleaned:
        data = []
        for line in lines:
            line = line.strip().split('|')
            start, end, distance = line 
            data.append({
                "start": get_node_id(start),
                "end": get_node_id(end),
                "distance": int(distance)                
            })

        json.dump(data, fp=cleaned, ensure_ascii=False)