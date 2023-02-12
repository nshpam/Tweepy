import os
import sys

from TweetHarvestGUI import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pymongo
import altair as alt
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Page
        self.ui.pushButton_dataSentiment.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.data_sentiment))
        
        self.show()
        
    def create_topwords_bar_chart(self):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["twitter_data"]
        collection = db["ranking_word"]

        # retrieve data from a MongoDB collection and store it in a Pandas dataframe
        data = list(collection.find({}))
        df = pd.DataFrame(data)
        
        # Extract the word and count columns
        words = df.get("word")
        counts = df.get("count")
        
        # Plot bar chart using Altair
        chart = alt.Chart({"word": words, "count": counts}).mark_bar().encode(
            x='word',
            y='count'
        ).properties(title='Ranking of words in tweets')
        chart.save("bar_chart.png")
        
        # Show the chart legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        # Set chart renderer and theme
        self.ui.chart_view = QtCharts.QChartView(chart)
        self.ui.chart_view.setRenderHint(QPainter.Antialiasing)
        self.ui.chart_view.chart().setTheme(QtCharts.QChart.ChartThemeDark)
        
        # Set chart size policy
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.chart_view.sizePolicy().hasHeightForWidth())
        self.ui.chart_view.setSizePolicy(sizePolicy)
        
        # Add chart to container
        self.ui.chart_view.setMinimumSize(QSize(0,300))
        self.ui.top_word.addWidget(self.ui.chart_view)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
