from PyQt5 import QtCore, QtWidgets
import json
import urllib.request
from collections import OrderedDict

class JSONWidget(QtWidgets.QTableWidget):

    url_signal = QtCore.pyqtSignal(QtCore.QUrl)


    def __init__(self, parent=None, *args, **kwargs):
        super(JSONWidget, self).__init__(parent, *args, **kwargs)
        self.data = OrderedDict(self._get_data())
        print(self.data)
        self.setRowCount(len(self.data))
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Key", "Value"])
        self._set_up_data(self.data)
        self.cellDoubleClicked.connect(self.cell_double_clicked_slot)
        
    def _get_data(self):
        # s3.amazonaws.com/Minecraft.Download/versions/versions.json
        url = "http://smile.sh/benhoff.json"
        request = urllib.request.urlopen(url)
        encoding = request.headers.get_content_charset()
        if encoding is None:
            data = json.loads(request.read().decode('utf-8'))
        else:
            data = json.loads(request.read().decode(encoding))
        return data

    def _set_up_data(self, data):
        for index, (key, value) in enumerate(data.items()):
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(key))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(value))


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

