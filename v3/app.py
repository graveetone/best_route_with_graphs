from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from services.map_generator_service import MapGeneratorService


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graph.sqlite3'
app.config['SERVER_NAME'] = 'localhost:5000'
db = SQLAlchemy(app)
from models import Node, Edge

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename='map.png'))
    

@app.route('/build_way')
def build_way():
    nodes = Node.query.all()
    edges = Edge.query.all()

    random_nodes = Node.query.order_by(func.random()).all()[:5]
    random_edges = Edge.query.order_by(func.random()).all()[:5]
    mgs_instance = MapGeneratorService(edges=edges, nodes=nodes)
    frame_filepath = mgs_instance.call(edges_to_highlight=random_edges, nodes_to_highlight=random_nodes)

    return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename=frame_filepath))
    