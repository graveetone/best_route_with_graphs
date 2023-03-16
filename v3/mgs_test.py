from services.map_generator_service import MapGeneratorService as MGS
from app import app
from models import Node, Edge
from sqlalchemy import func

with app.app_context():

    random_nodes = Node.query.order_by(func.random()).all()[:5]

    random_edges = Edge.query.order_by(func.random()).all()[:5]

    mgs_instance = MGS(nodes=Node.query.all(), edges=Edge.query.all())

    print(mgs_instance.call(edges_to_highlight=random_edges, nodes_to_highlight=random_nodes))
