from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graph.sqlite3'
app.config['SERVER_NAME'] = 'localhost:5000'
db = SQLAlchemy(app)

from services.map_generator_service import MapGeneratorService
from services.way_builder_service import WayBuilderService

from models import Node, Edge
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        nodes = Node.query.all()

        return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename='map.png'), nodes=nodes)
    

@app.route('/build_way')
def build_way():
    start, end = request.args.values()

    start = Node.query.get(int(start))
    end = Node.query.get(int(end))

    nodes = Node.query.all()
    edges = Edge.query.all()

    wbs = WayBuilderService(nodes)
    nodes_to_highlight, edges_to_highlight = wbs.build_way(start, end)

    mgs_instance = MapGeneratorService(edges=edges, nodes=nodes)
    frame_filepath = mgs_instance.call(edges_to_highlight=edges_to_highlight, nodes_to_highlight=nodes_to_highlight)

    return {
        'map': url_for('static', filename=frame_filepath)
    }
    