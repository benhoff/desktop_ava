import sys
import json
import urllib

from PyQt5 import QtWidgets, QtCore


j = json.loads('{"one": "1", "two": "2", "three": "3"}')

# Emma told me this works.... in python2 :(
# json.loads(' '.join(urllib2.urlopen(URL).readlines()))

class JSONWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(JSONWidget, self).__init__(parent, *args, **kwargs)
"""
url = None
headers = {"User-Agent":"alexthenicefontguy:foobar"}
request = urllib.request.Request(url, headers=headers)
a_thing = urllib.request(request) 
"""
app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()

json_widget = JSONWidget(parent=main_window)
json_widget.setRowCount(len(j))
json_widget.setColumnCount(2)
json_widget.setHorizontalHeaderLabels(["Key", "Value"])

for index, (key, value) in enumerate(j.items()):
    json_widget.setItem(index, 0, QtWidgets.QTableWidgetItem(key))
    json_widget.setItem(index, 1, QtWidgets.QTableWidgetItem(value))

main_window.setCentralWidget(json_widget)
main_window.show()

sys.exit(app.exec_())
