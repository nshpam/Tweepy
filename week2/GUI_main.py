import os
import sys

from ui_gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from plotly.offline import *
import pymongo
import pandas as pd

import plotly.express as px
from ui_gui import Ui_MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # navigate to home page
        self.ui.pushButton_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # self.ui.pushButton_home.clicked.connect(lambda: print("dfghjk"))

        
        self.show()
        


        
    def do_search(self):
        QMessageBox.information(self, "Search", self.linesearch.text(), QMessageBox.StandardButton.Ok)
        
    def create_topwords_bar_chart(self):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["twitter_data"]
        collection = db["ranking_word"]

        # retrieve data from a MongoDB collection and store it in a Pandas dataframe
        data = list(collection.find({}))
        source = pd.DataFrame({"word":list(data[0].keys())[1:11], "count":list(data[0].values())[1:11]})
        source = source.sort_values(by='count', ascending=True)
        print(source)

        # Plot bar chart using Plotly
        fig = px.bar(source, x='count', y='word', title='Ranking of words in tweets', text='count', orientation='h')
        fig.update_traces(textposition='auto', marker=dict(color='blue'))
        fig.update_layout(
            title=dict(font=dict(size=24)),
            xaxis=dict(title=dict(font=dict(size=18)), tickfont=dict(size=14)),
            yaxis=dict(title=dict(font=dict(size=18)), tickfont=dict(size=14)),
        )

        # Save the chart to an HTML file
        fig.write_html('topwords_bar_chart.html')
        
        # # check the location of the current working directory
        # print(os.getcwd())
        
        # view = QtWebEngineWidgets.QWebEngineView()
        # view.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]))
        
        # view.show()
        
        # # Show the chart legend
        # chart.legend().setVisible(True)
        # chart.legend().setAlignment(Qt.AlignBottom)
        
        # # Set chart renderer and theme
        # self.ui.chart_view = QtCharts.QChartView(chart)
        # self.ui.chart_view.setRenderHint(QPainter.Antialiasing)
        # self.ui.chart_view.chart().setTheme(QtCharts.QChart.ChartThemeDark)
        
        # # Set chart size policy
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.ui.chart_view.sizePolicy().hasHeightForWidth())
        # self.ui.chart_view.setSizePolicy(sizePolicy)
        
        # # Add chart to container
        # self.ui.chart_view.setMinimumSize(QSize(0,300))
        # self.ui.top_word.addWidget(self.ui.chart_view)
        
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
