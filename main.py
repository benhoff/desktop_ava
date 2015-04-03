import sys
import json
import urllib.request
from json_parser.py import JSONParser
from json_widgets import JSONTableWidget, JSONTreeWidget
from PyQt5 import QtWidgets, QtCore, QtWebKitWidgets


class MyWebView(QtWebKitWidgets.QWebView):
    def __init__(self, parent=None, *args, **kwargs):
        super(MyWebView, self).__init__(parent, *args, **kwargs)

    @QtCore.pyqtSlot(QtCore.QUrl)
    def url_slot(self, url):
        self.load(url)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    json_widget = JSONTreeWidget(parent=main_window)
    webkit_view = MyWebView()
    json_widget.url_signal.connect(webkit_view.url_slot)
    
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(json_widget)
    horizontal_layout.addWidget(webkit_view)
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(horizontal_layout)

    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())
