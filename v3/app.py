from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from services.reset_folder_service import ResetFolderService

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
        Node.query.filter_by(is_custom=True).delete()
        Edge.query.filter_by(is_custom=True).delete()
        
        db.session.commit()

        nodes = Node.query.all()

        ResetFolderService('static/frames').call()
        map_src = MapGeneratorService(nodes, []).call([], [])



        return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename=map_src), nodes=nodes)
    

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

@app.route('/add_node', methods=['GET', 'POST'])
def add_node():
    if request.method == 'POST':
        title, x, y = request.form.values()

        if Node.find_by_title(title):
            ...
        else:
            node = Node(
                title=title,
                x=x,
                y=y,
                is_custom=True
            )

            db.session.add(node)
            db.session.commit()

        nodes = Node.query.all()
        map_src = MapGeneratorService(nodes, []).call([], [])

        return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename=map_src), nodes=nodes)

    nodes = Node.query.all()
    map_src = MapGeneratorService(nodes, []).call([], [])

    return render_template('new_node.html', title='FindWayLab', map_src=url_for('static', filename=map_src), nodes=nodes)

@app.route('/add_edge', methods=['GET', 'POST'])
def add_edge():
    if request.method == 'POST':
        start, end, weight = request.form.values()

        start = Node.query.get(int(start))
        end = Node.query.get(int(end))
        weight = float(weight)
        
        edge = Edge.query.filter_by(start_node=start, end_node=end).first()
        
        if edge:
            edge.weight = weight
        else:
            edge = Edge(start_node=start,
                        end_node=end,
                        weight=weight)

            db.session.add(edge)
            db.session.commit()

        nodes = Node.query.all()
        map_src = MapGeneratorService(nodes, [edge]).call([edge.start_node, edge.end_node], [edge])


        return render_template('home.html', title='FindWayLab', map_src=url_for('static', filename=map_src), nodes=nodes)


    nodes = Node.query.all()
    edges = Edge.query.all()
    map_src = MapGeneratorService(nodes, edges).call([], [])


    return render_template('new_edge.html', title='FindWayLab', map_src=url_for('static', filename=map_src), nodes=nodes)