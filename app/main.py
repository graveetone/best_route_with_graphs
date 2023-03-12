from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from frontend import Ui_MainWindow

from services.json_loader_service import JsonLoaderService
from services.config_service import ConfigService
from services.way_builder_service import WayBuilderService
from services.map_generator_service import MapGeneratorService
from services.logger_service import Loger
from models import Node
from pytimer import Timer
import uuid
import random

class CustomMainWindow(Ui_MainWindow):
    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.nodes = Node.from_dicts(JsonLoaderService(ConfigService.NODES_FILEPATH).load())
        
        self.fill_comboboxes()
        self.display_map()

        self.nodes_to_highlight = []

        self.build_way_button.clicked.connect(lambda: self.update_map())
        self.add_node_button.clicked.connect(lambda: self.add_node())


    def add_node(self):
        def add_point(event):
            node = Node(title=uuid.uuid4().__str__()[4:8], coordinates=(event.pos().x, event.pos().y))
            node.add_neighbours([(random.sample(self.nodes, 1), random.randint(30, 205)) for _ in range(3)])

            self.start_point.addItem(node.title)
            self.end_point.addItem(node.title)
            self.nodes.append(node)

            QApplication.restoreOverrideCursor()


        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.map.mousePressEvent = lambda QMouseEvent: add_point(QMouseEvent)

    def update_map(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        start = Node.find_by_title(title=self.start_point.currentText(), nodes=self.nodes)
        end = Node.find_by_title(title=self.end_point.currentText(), nodes=self.nodes)

        nodes_to_highlight = self.nodes_to_highlight

        t = Timer()
        nodes_to_highlight, edges_to_highlight = WayBuilderService(self.nodes).build_way(start, end)

        new_map_filepath = MapGeneratorService(nodes_to_highlight, edges_to_highlight).call()
        self.display_map(map_path=new_map_filepath)
        distances = [edge[2] for edge in edges_to_highlight]
        path = [n.title for n in nodes_to_highlight]
        self.display_info(sum(distances), str(t), '->'.join(path))
        QApplication.restoreOverrideCursor()

    def fill_comboboxes(self):
        titles = [node.title for node in self.nodes]

        self.start_point.addItems(titles)
        self.end_point.addItems(titles)
    
    def display_map(self, map_path=ConfigService.MAP_FILEPATH):
        Loger.log('map_path', map_path)
        pixmap = QtGui.QPixmap(map_path)
        self.map.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.map.setPixmap(pixmap)

        self.map.show()

    def display_info(self, distance, time, path):
        self.distance.setVisible(True)
        self.path.setVisible(True)
        self.time.setVisible(True)

        self.distance.clear()
        self.time.clear()
        self.path.clear()

        self.distance.setText("Відстань: " + str(distance) + 'км')
        self.time.setText("Часу витрачено:" + str(time))
        self.path.setText("Шлях: " + str(path))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CustomMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())