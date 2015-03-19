from PyQt5 import QtCore, QtWidgets
import json
import urllib.request
from collections import OrderedDict

class JSONWidget(QtWidgets.QTableWidget):

    url_signal = QtCore.pyqtSignal(QtCore.QUrl)
    NUM_OBJS_IN_PROJ = 5

    def __init__(self, parent=None, *args, **kwargs):
        super(JSONWidget, self).__init__(parent, *args, **kwargs)
        self._count = None
        self._next = None
        self._previous = None

        self.results = self._get_and_parse_data()
        #print(self.results)
        self.setRowCount(len(self.results)*self.NUM_OBJS_IN_PROJ)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Key", "Value"])
        self._set_up_data(self.results)
        self.cellDoubleClicked.connect(self.cell_double_clicked_slot)
        
    def _get_and_parse_data(self):
        # s3.amazonaws.com/Minecraft.Download/versions/versions.json
        url = "http://127.0.0.1:8000/projects/"
        request = urllib.request.urlopen(url)
        encoding = request.headers.get_content_charset()
        if encoding is None:
            print("There was no encoding!")
            data = json.loads(request.read().decode('utf-8'))
        else:
            data = json.loads(request.read().decode(encoding))
        self._count = data['count']
        self._next = data['next']
        self._previous = data['previous']

        return data['results']

    def _set_up_data(self, data):
        for results_index, results_dict in enumerate(self.results):
            for dict_index, (key, value) in enumerate(results_dict.items()):
                calculated_index = (results_index *self.NUM_OBJS_IN_PROJ) + dict_index
                self.setItem(calculated_index, 0, QtWidgets.QTableWidgetItem(key))
                self.setItem(calculated_index, 1, QtWidgets.QTableWidgetItem(value))

    @QtCore.pyqtSlot(int, int)
    def cell_double_clicked_slot(self, row, column):
        if column != 0:
            url_item = self.item(row, column).data(QtCore.Qt.DisplayRole)
            print(url_item)
            self.url_signal.emit(QtCore.QUrl(url_item))
        else:
            pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = JSONWidget()
    widget.show()
    sys.exit(app.exec_())

