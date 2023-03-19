from services.way_builder_service import WayBuilderService
from app import app
from models import Node

with app.app_context():
    nodes = Node.query.all()

    start = Node.find_by_title('Чернігів')
    end = Node.find_by_title('Полтава')

    wbs = WayBuilderService(nodes)

    path = wbs.build_way(start, end)

    print(path)
