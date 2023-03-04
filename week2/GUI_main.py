import sys

from ui_gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from plotly.offline import *
import pymongo
import pandas as pd

import plotly.express as px
from ui_gui import Ui_MainWindow

from tweepy_main import *
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
        # show window
        self.show()
        
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
        
            # counter for number of trends
        count = 0
        for trend in trends_keyword:
            # iterate through each key-value pair in the current trend dictionary
            for name, volume in trend.items():
                # convert volume to thousands and format as string with "K" appended
                volume_str = "{:.1f}K".format(volume/1000) if volume is not None else "-"
                # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
                item = QStandardItem(f"{count+1}. {name} ({volume_str})")
                # adds a new row of items to the model
                model.appendRow(item)
                count += 1
        # display the list of trends in the widget.
        self.ui.listView_2.setModel(model)
    
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
