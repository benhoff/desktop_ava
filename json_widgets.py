from PyQt5 import QtCore, QtWidgets
import json
import urllib.request
from collections import OrderedDict

def get_data(url):
    request = urllib.request.urlopen(url)
    encoding = request.headers.get_content_charset()
    if encoding is None:
        encoding = 'utf-8'
    return json.loads(request.read().decode(encoding))

def parse_data_simply(kls, data):
    kls._count = data['count']
    kls._next = data['next']
    kls._previous = data['previous']

    return data['results']

class JSONTreeWidget(QtWidgets.QTreeWidget):

    url_signal = QtCore.pyqtSignal(QtCore.QUrl)
    
    def __init__(self, parent=None, *args, **kwargs):
        super(JSONTreeWidget, self).__init__(parent, *args, **kwargs)
        data = get_data("http://127.0.0.1:8000/projects/")
        self.results = parse_data_simply(self, data)
        self._store_results_in_widget(self.results)
        self.doubleClicked.connect(self.cell_double_clicked_slot)

    def _store_results_in_widget(self, results_list_of_dicts):
        for list_index, results_dict in enumerate(results_list_of_dicts):
            string_list = [results_dict['title'],]
            top_level_item = QtWidgets.QTreeWidgetItem(string_list)

            description_list = ["Description: {}".format(results_dict['description']),]
            description_item = QtWidgets.QTreeWidgetItem(top_level_item, description_list)

            sub_string_list = ["User: {}".format(results_dict['user']),]
            user_item = QtWidgets.QTreeWidgetItem(top_level_item, sub_string_list)

            status_list = ["Status: {}".format(results_dict['status']),]
            status_item = QtWidgets.QTreeWidgetItem(top_level_item, status_list)

            self.addTopLevelItem(top_level_item)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def cell_double_clicked_slot(self, model_index):    
        line_dict = self.results[model_index.row()]
        self.url_signal.emit(QtCore.QUrl(line_dict['url']))
                
class JSONTableWidget(QtWidgets.QTableWidget):

    url_signal = QtCore.pyqtSignal(QtCore.QUrl)
    NUM_OBJS_IN_PROJ = 5

    def __init__(self, parent=None, *args, **kwargs):
        super(JSONWidget, self).__init__(parent, *args, **kwargs)
        
        data = get_data("http://127.0.0.1:8000/projects/")
        self.results = parse_data_simply(self, data)
        self.setRowCount(len(self.results)*self.NUM_OBJS_IN_PROJ)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Key", "Value"])
        self._set_up_data(self.results)
        self.cellDoubleClicked.connect(self.cell_double_clicked_slot)
        
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
    widget = JSONTreeWidget()
    #widget = JSONTableWidget()
    widget.show()
    sys.exit(app.exec_())

