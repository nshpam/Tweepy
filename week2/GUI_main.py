import sys

from ui_gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtWebEngineWidgets import *
from plotly.offline import *
import plotly.graph_objs as go
import plotly.offline as po

import pymongo
import pandas as pd

import plotly.express as px
from ui_gui import Ui_MainWindow

from tweepy_search import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # hides the menu icon bar by default
        self.ui.frame_minmenu.hide()
        # navigate to Home page
        self.ui.pushButton_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # navigate to Extract page
        self.ui.pushButton_extract.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        # navigate to Sentiment page
        self.ui.pushButton_sentimeny.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        # navigate to Rankings page
        self.ui.pushButton_rankings.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        # Click the navigation icon to go to the Home page.
        self.ui.pushButton_iconhome.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # Click the navigation icon to go to the Extract page.
        self.ui.pushButton_iconextract.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        # Click the navigation icon to go to the Sentiment page.
        self.ui.pushButton_iconsentiment.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        # Click the navigation icon to go to the Home page.
        self.ui.pushButton_iconrankings.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        # link the textChanged signal of the search lineEdit object to a function
        self.ui.lineEdit_search.textChanged.connect(self.auto_fill)
        # set the icon in the search bar located on the right side
        search_action = self.ui.lineEdit_search.addAction(QIcon("icon/magnifying-glass.png"),QLineEdit.ActionPosition.TrailingPosition)
        # # connection between a search action and a function that will be executed when the action is triggered by the user.
        # search_action.triggered.connect(self.do_search)
        
        # call the show_trends method to show in Listview
        self.show_trends()
        # display a drop-down list containing the three items: "Popular", "Recent", and "Mixed"
        self.ui.comboBox_searchtype.addItems(["Popular","Recent","Mixed"])
        # connect the search button with the search_twitter function
        self.ui.comboBox_searchtype.currentIndexChanged.connect(self.search_twitter)
        
        # Add chart view to QFrame (Overview of hashtags)
        self.create_pie_chart()
        self.ui.frame_21.layout().addWidget(self.chart_view)
        
        # self.ui.frame_24.layout().addWidget(self.chart_view)
        # show window
        self.show()
    # for Overview of hashtags
    def create_pie_chart(self):
        labels = ['Apple', 'Banana', 'Pear']
        values = [80, 70, 50]
        
        # Define data and layout
        data = go.Pie(
                        labels=labels,
                        values=values,
                        marker=dict(colors=['#FF3B30', '#4CD964', '#007AFF']),
                        hole=0.3  # set the size of the center hole
    )
        
        layout = go.Layout(font=dict(
        family='SF Compact Display',
        size=20,
        color='white',  # set font color to white
    ),plot_bgcolor='rgb(13, 15, 33)',
    paper_bgcolor='rgb(13, 15, 33)',
)
        
        # Create figure and plot in QWebEngineView
        fig = go.Figure(data=[data], layout=layout)
        po.init_notebook_mode(connected=True)
        plot_html = po.plot(fig, include_plotlyjs=False, output_type='div')
         # Add Plotly library to HTML file
        html = f"""
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            {plot_html}
        </body>
        </html>
        """
        
        self.chart_view = QWebEngineView()
        self.chart_view.setHtml(html)
        self.chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def auto_fill(self, text):
        # Use the setText method to autofill keyword lineEdit with the text from search lineEdit
        self.ui.lineEdit_keyword.setText(text)
    
    def search_twitter(self):
       
        # get the search keyword from the input textbox
        search_word = self.ui.lineEdit_keyword.text()

        # get the selected search type from the combo box
        search_type = self.ui.comboBox_searchtype.currentText()
        # get the selected search limit from the spin box
        num_tweet = self.ui.spinBox_searchlimit.value()
        # create an instance of the Twitter API
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        api = tweepy.API(auth)
        # create an instance of PullTwitterData
        self.twitter_data = PullTwitterData()
        # call the search_twitter function from the PullTwitterData object
        result_text = self.twitter_data.search_twitter(api, search_word, search_type, num_tweet)

        # print the result in the terminal
        print(result_text)
        
    # def do_search(self):
    
    def show_trends(self):
        # authenticate the Twitter API requests with the Twitter API keys and access tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        # make requests to the Twitter API
        api = tweepy.API(auth)
        # calls the pull_trends method from the PullTwitterData class
        trends_keyword = PullTwitterData().pull_trends(api, config.WOEid, config.ranking_top)
        # Qt model used to display data in a QListView widget
        model = QStandardItemModel()
        # create a custom font
        # Load the font file
        font_id = QFontDatabase.addApplicationFont("FontsFree-Net-SFCompactDisplay-Regular.ttf")
        # Get the family name of the loaded font
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Create a QFont object using the loaded font
        font = QFont(font_family)
        font.setPointSize(14)
        font.setBold(True)
        # Create a QFont object for the trend volume
        volume_font = QFont(font_family)
        volume_font.setPointSize(12)

        # counter for number of trends
        count = 0
        for trend in trends_keyword:
            # iterate through each key-value pair in the current trend dictionary
            for name, volume in trend.items():
                # convert volume to thousands and format as string with "K" appended
                volume_str = "{:.1f}K".format(volume/1000) if volume is not None else "-"
                # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
                item = QStandardItem(f"{count+1}. {name}")
                item.setFont(font)  # set the custom font to the QStandardItem
                # adds a new row of items to the model
                model.appendRow(item)
                # create a new QStandardItem for the trend volume
                volume_item = QStandardItem(f"{volume_str} tweets\n")
                volume_item.setFont(volume_font) # set the custom font to the QStandardItem
                model.appendRow(volume_item)

                count += 1
        
        # display the list of trends in the widget.
        self.ui.listView_2.setModel(model)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
