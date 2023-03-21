import sys
import os
from ui_gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtWebEngineWidgets import *
from plotly.offline import *
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import plotly

import plotly.express as px
from ui_gui import Ui_MainWindow

from tweepy_search import *
from twitterDataRankings import *

from pytagcloud import *
import tempfile

#class for progressbar
class SearchThread(QThread):
    progress_changed = pyqtSignal(int)
    finished = pyqtSignal(object)

    def __init__(self, api, search_word, search_type, num_tweet, parent=None):
        super().__init__(parent)
        self.api = api
        self.search_word = search_word
        self.search_type = search_type
        self.num_tweet = num_tweet

    def run(self):
        twitter_data = PullTwitterData()
        tweets = []
        total_tweets = self.num_tweet
        progress = 0
        for i, tweet in enumerate(twitter_data.search_twitter(self.api, self.search_word, self.search_type, self.num_tweet)):
            tweets.append(tweet)
            i += 1
            if i % 10 == 0 or total_tweets >= 10 or total_tweets <= 10:
                progress = int(i / total_tweets * 100)
                self.progress_changed.emit(progress)
        self.progress_changed.emit(100)
        self.finished.emit(tweets)
        
#main class
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
        # navigate to library page
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
        # Click the navigation icon to go to the Home page.
        self.ui.pushButton_iconhome.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        # Click the navigation icon to go to the Extract page.
        self.ui.pushButton_iconextract.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        # Click the navigation icon to go to the Sentiment page.
        self.ui.pushButton_iconsentiment.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        # Click the navigation icon to go to the ranking page.
        self.ui.pushButton_iconrankings.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        # Click the navigation icon to go to the library page.
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
        # when click extract botton will show input user in terminal
        self.ui.pushButton_extract_2.clicked.connect(lambda: self.print_search_params())
        
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(0))
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(1))
        # Click botton to scrap tweets.
        self.ui.pushButton_extract_2.clicked.connect(lambda: self.search_twitter())
        # link the textChanged signal of the search lineEdit object to a function
        self.ui.lineEdit_search.textChanged.connect(self.auto_fill)
        # set the icon in the search bar located on the right side
        search_action = self.ui.lineEdit_search.addAction(QIcon("icon/magnifying-glass.png"),QLineEdit.ActionPosition.TrailingPosition)
        # connection between a search action and a function that will be executed when the action is triggered by the user.
        search_action.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        
        # call the show_trends method to show in Listview
        self.show_trends_word()
        self.show_trends_hashtags()
        self.show_keywords_database()
        # display a drop-down list containing the three items: "Popular", "Recent", and "Mixed"
        self.ui.comboBox_searchtype.addItems(["Popular","Recent","Mixed"])
        # Add chart view to QFrame (Overview of hashtags)
        self.create_pie_chart()
        self.ui.frame_21.layout().addWidget(self.chart_view)
        
        
        
        # Add world cloud to QFrame 
        # self.create_word_cloud()
        # self.ui.frame_24.layout().addWidget(self.wordcloud_label)
        
        # Add world cloud to QFrame (Ranking Top 10 Words)
        # self.create_bar_chart()
        # self.ui.frame_33.layout().addWidget(self.horizontalbar_chart_view)
        
        # Call spatial_chart method and add it to the layout
        # self.plot_spatial_chart()
        # self.ui.frame_23.layout().addWidget(self.spatial_chart_view)
        
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
    ),
    plot_bgcolor='rgb(13, 15, 33)',
    paper_bgcolor='rgb(13, 15, 33)',
)
        
        # Create figure and plot in QWebEngineView
        fig = go.Figure(data=[data], layout=layout)
        po.init_notebook_mode(connected=True)
        plot_html = po.plot(fig, include_plotlyjs=False, output_type='div')
        # Add Plotly library to HTML file
        html = "<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>{plot_html}</body></html>".format(plot_html=plot_html)

        
        self.chart_view = QWebEngineView()
        self.chart_view.setHtml(html)
        self.chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    # for Sentiment Word Clound (Overall)
    def create_word_cloud(self):
        # Generate mock data
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        words = text.split()
        word_counts = {word: words.count(word) for word in words}
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = dict(sorted_word_counts[:20])
        
        # Create tags for word cloud
        tags = make_tags(list(top_words.items()), maxsize=80)
        
        # Set font for word cloud
        create_tag_image(tags, 'wordcloud.png', fontname='Droid Sans')
        
        # Set temporary file path to save the word cloud image
        tmp_file_path = os.path.join(tempfile.gettempdir(), "wordcloud.png")
        
        # Generate word cloud image and save to file
        create_tag_image(tags, tmp_file_path, size=(800, 600))
        
        # Load word cloud image into QLabel widget in GUI
        pixmap = QtGui.QPixmap(tmp_file_path)
        self.wordcloud_label = QtWidgets.QLabel()
        self.wordcloud_label.setPixmap(pixmap)
        self.wordcloud_label.setScaledContents(True)
        self.wordcloud_label.setMinimumSize(1, 1)
        self.wordcloud_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
    def create_bar_chart(self):
        # Load the font file
        font_id = QFontDatabase.addApplicationFont("FontsFree-Net-SFCompactDisplay-Regular.ttf")
        # Get the family name of the loaded font
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        top_words, top_frequencies = Ranking().rank_list()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_frequencies[::-1],
            y=top_words[::-1],
            orientation='h'
        ))
        fig.update_layout(
            title='Top {} Words'.format(len(top_words)),
            xaxis_title='Frequency',
            yaxis_title='Word',
            font=dict(
                family=font_family,
                size=20,
                color='black',
            ),
            title_font=dict(
                family=font_family,
                size=22,
                color='black',
        ))
        
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

        
        self.horizontalbar_chart_view = QWebEngineView()
        self.horizontalbar_chart_view.setHtml(html)
        self.horizontalbar_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def plot_spatial_chart(self):
        # Connect to the database and get the tweets with non-null locations
        collection = db_action.tweetdb_object(
            config.mongo_client,
            config.database_name,
            config.collection_name
        )
        query = db_action.tweetdb_create_object(["location"], [{"$ne": None}])
        cursor = db_action.tweetdb_find(config.collection_name, collection, query)

        # Create a dataframe from the cursor
        data_frame = pd.DataFrame(list(cursor))

        # Extract the latitude and longitude values from the location array
        data_frame["longitude"] = data_frame["location"].apply(lambda x: x[0])
        data_frame["latitude"] = data_frame["location"].apply(lambda x: x[1])

        # Plot the map
        fig = px.scatter_mapbox(
            data_frame,
            lat="latitude",
            lon="longitude",
            zoom=3
        )
        fig.update_layout(mapbox_style="open-street-map")
        
        # create a QWebEngineView widget to display the HTML chart
        self.spatial_chart_view = QWebEngineView()
        self.spatial_chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))
        self.spatial_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def auto_fill(self, text):
        # Use the setText method to autofill keyword lineEdit with the text from search lineEdit
        self.ui.lineEdit_keyword.setText(text)
    
    def search_twitter(self):
        # switch to the progress page
        self.ui.stackedWidget.setCurrentIndex(1)
       
        # get the search keyword from the input textbox
        search_word = self.ui.lineEdit_keyword.text()

        # get the selected search type from the combo box
        search_type = self.ui.comboBox_searchtype.currentText()
        # get the selected search limit from the spin box
        num_tweet = self.ui.spinBox_searchlimit.value()
        
        # set the text of the labels to the search parameters
        self.ui.label_26.setText(search_word)
        self.ui.label_28.setText(search_type)
        self.ui.label_30.setText(str(num_tweet))
        # create an instance of the Twitter API
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        api = tweepy.API(auth)
        # create an instance of PullTwitterData
        self.twitter_data = PullTwitterData()
        # set the maximum value for the progress bar
        self.ui.progressBar.setMaximum(num_tweet)

        # create a thread to run the search_twitter function
        self.thread = SearchThread(api, search_word, search_type, num_tweet)
        self.thread.progress_changed.connect(self.ui.progressBar.setValue)
        self.thread.finished.connect(self.on_search_finished)
        self.thread.start()
        # create a QTimer to update the progress bar every 100ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
        
        # connect the cancel button to the slot function
        self.ui.pushButton_2.clicked.connect(self.cancel_search)
        
    def cancel_search(self):
        # stop the timer
        self.timer.stop()
        # stop the thread
        self.thread.terminate()
        # switch to the home page
        self.ui.stackedWidget.setCurrentIndex(4)
        
    def update_progress(self):
        # update the progress bar value based on the current progress of the search thread
        progress = self.ui.progressBar.value()
        if progress < 100:
            progress += 1
            self.ui.progressBar.setValue(progress)
            
    def on_search_finished(self):
        # switch to the new page
        self.ui.stackedWidget.setCurrentIndex(0)
        
    def print_search_params(self):
        # get the search keyword from the input textbox
        search_word = self.ui.lineEdit_keyword.text()

        # get the selected search type from the combo box
        search_type = self.ui.comboBox_searchtype.currentText()

        # get the selected search limit from the spin box
        num_tweet = self.ui.spinBox_searchlimit.value()

        # print the search parameters to the terminal
        print("Search Word:", search_word)
        print("Search Type:", search_type)
        print("Number of Tweets:", num_tweet)

            
        
    def show_keywords_database(self):
        # Connect to the database
        collection = db_action.tweetdb_object(
            config.mongo_client,
            config.database_name,
            config.collection_name
        )

        # Fetch the keywords from the database
        keywords = collection.distinct('keyword')

        # Qt model used to display data in a QListView widget
        model_3 = QStandardItemModel()
        model_5 = QStandardItemModel()

        # create a custom font
        # Load the font file
        font_id = QFontDatabase.addApplicationFont("FontsFree-Net-SFCompactDisplay-Regular.ttf")
        # Get the family name of the loaded font
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Create a QFont object using the loaded font
        font = QFont(font_family)
        font.setPointSize(14)
        font.setBold(True)

        # Add the keywords to the list models
        count_3 = 0
        count_5 = 0
        for i, keyword in enumerate(keywords):
            count = collection.count_documents({'keyword': keyword})
            text = f"{keyword}\n"
            if count > 0:
                text += f"{count} tweets\n"
            item = QStandardItem(text)
            item.setFont(font)
            if "#" in keyword:
                count_3 += 1
                item.setText(f"{count_3}. " + item.text())
                model_3.appendRow(item)
            else:
                count_5 += 1
                item.setText(f"{count_5}. " + item.text())
                model_5.appendRow(item)

        # set the font for the list view widgets
        self.ui.listView_3.setFont(font)
        self.ui.listView_5.setFont(font)

        # display the list of trends in the widgets
        self.ui.listView_3.setModel(model_3)
        self.ui.listView_5.setModel(model_5)



            
    def show_trends_word(self):
        # authenticate the Twitter API requests with the Twitter API keys and access tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        # make requests to the Twitter API
        api = tweepy.API(auth)
        # calls the pull_trends_hashtags method from the PullTwitterData class
        trends_keyword = PullTwitterData().pull_trends(api, config.WOEid)
        trends_keyword = trends_keyword["words"]
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

        list_keys = list(trends_keyword.keys())
        list_values = list(trends_keyword.values())
        for i in range(len(list_keys)):
            name = list_keys[i]
            volume = list_values[i]
            # convert volume to thousands and format as string with "K" appended
            volume_str = "{:.1f}K".format(volume/1000) if volume is not None else ""
            # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
            item = QStandardItem(f"{i+1}. {name}")
            item.setFont(font)  # set the custom font to the QStandardItem
            # adds a new row of items to the model
            model.appendRow(item)
            # create a new QStandardItem for the trend volume
            if volume is not None:
            # create a new QStandardItem for the trend volume if volume is not None
                volume_item = QStandardItem(f"{volume_str} tweets\n")
                volume_item.setFont(volume_font) # set the custom font to the QStandardItem
                model.appendRow(volume_item)
            else:
                # create a placeholder QStandardItem if volume is None
                placeholder_item = QStandardItem(volume_str)
                placeholder_item.setFont(volume_font)
                model.appendRow(placeholder_item)


        
        # display the list of trends in the widget.
        self.ui.listView_4.setModel(model)
        
            
    def show_trends_hashtags(self):
        # authenticate the Twitter API requests with the Twitter API keys and access tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        # make requests to the Twitter API
        api = tweepy.API(auth)
        # calls the pull_trends_hashtags method from the PullTwitterData class
        trends_keyword = PullTwitterData().pull_trends(api, config.WOEid)
        trends_keyword = trends_keyword["hashtags"]
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

        list_keys = list(trends_keyword.keys())
        list_values = list(trends_keyword.values())
        for i in range(len(list_keys)):
            name = list_keys[i]
            volume = list_values[i]
            # convert volume to thousands and format as string with "K" appended
            volume_str = "{:.1f}K".format(volume/1000) if volume is not None else ""
            # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
            item = QStandardItem(f"{i+1}. {name}")
            item.setFont(font)  # set the custom font to the QStandardItem
            # adds a new row of items to the model
            model.appendRow(item)
            # create a new QStandardItem for the trend volume
            if volume is not None:
            # create a new QStandardItem for the trend volume if volume is not None
                volume_item = QStandardItem(f"{volume_str} tweets\n")
                volume_item.setFont(volume_font) # set the custom font to the QStandardItem
                model.appendRow(volume_item)
            else:
                # create a placeholder QStandardItem if volume is None
                placeholder_item = QStandardItem(volume_str)
                placeholder_item.setFont(volume_font)
                model.appendRow(placeholder_item)

        
        # display the list of trends in the widget.
        self.ui.listView_2.setModel(model)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
