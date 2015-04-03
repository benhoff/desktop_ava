from PyQt5 import QtWidgets, QtCore
from json_parser import JSONParser

URL_ROOT = "http://127.0.0.1:8000"

class InstanceViewWidget(QtWidgets.QListWidget):
    url_signal = QtCore.pyqtSignal(QtCore.QUrl)
    def __init__(self, parent=None, data=None, *args, **kwargs):
        super(InstanceViewWidget, self).__init__(parent, *args, **kwargs)
        self.doubleClicked.connect(self.cell_double_clicked_slot)
        self.urls_index_row_tuple = []

        try:
            for key, value in data.items():
                if not isinstance(value, str):
                    self.addItem("{key}: {value}".format(key=key, value=value))
                elif URL_ROOT in value:
                    self.addItem("{}".format(key))
                    self.urls_index_row_tuple.append((value, self.count()-1))
                else:
                    self.addItem("{key}: {value}".format(key=key, value=value))
        except AttributeError:
            for item in data:
                if "url" in item:
                    self.urls.append(item)
                else:
                    self.addItem(str(item))

        self.data = data

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def cell_double_clicked_slot(self, model_index):
        model_row = model_index.row()
        # the way urls_index_row_tuple is [(urls, index)]
        index_row_list = [x[1] for x in self.urls_index_row_tuple]
        if model_row in index_row_list:
            tuple_index = index_row_list.index(model_row)
            url = self.urls_index_row_tuple[tuple_index][0]
            print(url)
            self.url_signal.emit(QtCore.QUrl(url))


if __name__ == '__main__':
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #j = JSONParser("http://127.0.0.1:8000/projects/2/")
    j = JSONParser("http://127.0.0.1:8000/projects/2/ideas/3/")
    view_widget = InstanceViewWidget(data=j.data) 
    view_widget.show()
    sys.exit(app.exec_())
