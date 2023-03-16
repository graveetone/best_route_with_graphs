from app import db


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    out_edges = db.relationship('Edge', back_populates='start_node', foreign_keys='Edge.start_node_id')
    in_edges = db.relationship('Edge', back_populates='end_node', foreign_keys='Edge.end_node_id')

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    def __repr__(self):
        return f"<Node {self.title} ({self.x};{self.y})>"
    
    def edges(self):
        return [
            *self.in_edges,
            *self.out_edges
        ]

class Edge(db.Model):
    __tablename__ = 'edges'
    id = db.Column(db.Integer, primary_key=True)
    start_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    end_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    weight = db.Column(db.Float)
    start_node = db.relationship('Node', back_populates='out_edges', foreign_keys=[start_node_id])
    end_node = db.relationship('Node', back_populates='in_edges', foreign_keys=[end_node_id])

    def __repr__(self):
        return f"<Edge {self.start_node.title}-{self.end_node.title} with weight {self.weight}>"
