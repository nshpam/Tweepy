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

import plotly.express as px
from ui_gui import Ui_MainWindow

from tweepy_search import *

from pytagcloud import *
import tempfile

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
        
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        
        # link the textChanged signal of the search lineEdit object to a function
        self.ui.lineEdit_search.textChanged.connect(self.auto_fill)
        # set the icon in the search bar located on the right side
        search_action = self.ui.lineEdit_search.addAction(QIcon("icon/magnifying-glass.png"),QLineEdit.ActionPosition.TrailingPosition)
        # # connection between a search action and a function that will be executed when the action is triggered by the user.
        # search_action.triggered.connect(self.do_search)
        
        # call the show_trends method to show in Listview
        self.show_trends_word()
        self.show_trends_hashtags()
        
        # display a drop-down list containing the three items: "Popular", "Recent", and "Mixed"
        self.ui.comboBox_searchtype.addItems(["Popular","Recent","Mixed"])
        # connect the search button with the search_twitter function
        self.ui.comboBox_searchtype.currentIndexChanged.connect(self.search_twitter)
        
        
        # Add chart view to QFrame (Overview of hashtags)
        self.create_pie_chart()
        self.ui.frame_21.layout().addWidget(self.chart_view)
        
        # Add world cloud to QFrame 
        self.create_word_cloud()
        self.ui.frame_24.layout().addWidget(self.wordcloud_label)
        
        # Add world cloud to QFrame (Ranking Top 10 Words)
        self.create_bar_chart()
        self.ui.frame_33.layout().addWidget(self.horizontalbar_chart_view)
        
        # Call spatial_chart method and add it to the layout
        self.spatial_chart()
        self.ui.frame_23.layout().addWidget(self.spatial_chart_view)
        
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
        # Generate mock data
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        words = text.split()
        word_counts = {word: words.count(word) for word in words}
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = dict(sorted_word_counts[:10])

        # Get data for horizontal bar chart
        labels = list(top_words.keys())
        values = list(top_words.values())

        # Define data and layout
        data = go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker=dict(color='#007AFF', )
        )

        layout = go.Layout(
            font=dict(
                family='SF Compact Display',
                size=20,
                color='white'
            ),
            plot_bgcolor='rgb(13, 15, 33)',
            paper_bgcolor='rgb(13, 15, 33)',
            xaxis=dict(
                title=dict(
                    text='Frequency',
                    font=dict(
                        family='SF Compact Display',
                        size=20,
                        color='white'
                    )
                ),
                tickfont=dict(
                    family='SF Compact Display',
                    size=18,
                    color='white'
                ),
                autorange=True,
                zeroline=False,
                range=[0, max(values) + 10],
            ),
            yaxis=dict(
                tickfont=dict(
                    family='SF Compact Display',
                    size=18,
                    color='white'
                ),
                autorange='reversed' # Reverse the y-axis
            )
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

        
        self.horizontalbar_chart_view = QWebEngineView()
        self.horizontalbar_chart_view.setHtml(html)
        self.horizontalbar_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    
    def spatial_chart(self):
        # Geojson
        ccaa = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"ccaa_id": "01", "name": "Andalucía"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[-5.158, 36.417], [-4.877, 36.773], [-3.001, 36.975], [-2.53, 36.728],
                                         [-2.469, 36.558], [-4.116, 36.128], [-4.799, 36.16], [-5.158, 36.417]]],
                    },
                },]}
        # Data
        unemp_rates = [    
                       {"ccaa_id": "01", "name": "Andalucía", "unemp_rate": 18.68},
                       {"ccaa_id": "02", "name": "Aragón", "unemp_rate": 8.96},
                       {"ccaa_id": "03", "name": "Principado de Asturias", "unemp_rate": 11.36},
                       {"ccaa_id": "04", "name": "Islas Baleares", "unemp_rate": 9.29},
                       {"ccaa_id": "05", "name": "Islas Canarias", "unemp_rate": 17.76},
                       {"ccaa_id": "06", "name": "Cantabria", "unemp_rate": 8.17},
                       {"ccaa_id": "07", "name": "Castilla y León", "unemp_rate": 10.19},
                       {"ccaa_id": "08", "name": "Castilla-La Mancha", "unemp_rate": 14.11},
                       {"ccaa_id": "09", "name": "Cataluña", "unemp_rate": 9.29},
                       {"ccaa_id": "10", "name": "Comunidad Valenciana", "unemp_rate": 12.81},
                       {"ccaa_id": "11", "name": "Extremadura", "unemp_rate": 16.73},
                       {"ccaa_id": "12", "name": "Galicia", "unemp_rate": 11.2},
                       {"ccaa_id": "13", "name": "Comunidad de Madrid", "unemp_rate": 10.18},
                       {"ccaa_id": "14", "name": "Región de Murcia", "unemp_rate": 12.18},
                       {"ccaa_id": "15", "name": "Comunidad Foral de Navarra", "unemp_rate": 8.76},
                       {"ccaa_id": "16", "name": "País Vasco", "unemp_rate": 8.75},
                       {"ccaa_id": "17", "name": "La Rioja", "unemp_rate": 10.19},
                       {"ccaa_id": "18", "name": "Ceuta y Melilla", "unemp_rate": 23.71},
                       ]

        fig = px.choropleth_mapbox(
            data_frame = unemp_rates,
            geojson = ccaa,
            featureidkey = 'properties.ccaa_id',
            locations = 'ccaa_id',
            color = 'unemp_rate',
            hover_name = 'name',
            mapbox_style = 'open-street-map',
            center = dict(lat = 40.0, lon = -3.72),
            zoom = 4)
        # convert Plotly figure to HTML
        plot_html = po.plot(fig, include_plotlyjs=False, output_type='div')

        # create an HTML file with the Plotly chart
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

        # create a QWebEngineView widget to display the HTML chart
        self.spatial_chart_view = QWebEngineView()
        self.spatial_chart_view.setHtml(html)
        self.spatial_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
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
    
    def show_trends_word(self):
        # authenticate the Twitter API requests with the Twitter API keys and access tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        # make requests to the Twitter API
        api = tweepy.API(auth)
        # calls the pull_trends_hashtags method from the PullTwitterData class
        trends_keyword = PullTwitterData().pull_trends_word(api, config.WOEid)
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
                volume_str = "{:.1f}K".format(volume/1000) if volume is not None else ""
                # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
                item = QStandardItem(f"{count+1}. {name}")
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


                count += 1
        
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
        trends_keyword = PullTwitterData().pull_trends_hashtags(api, config.WOEid)
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
                volume_str = "{:.1f}K".format(volume/1000) if volume is not None else ""
                # representation of the form "trend_name (trend_volume)" for each trend in the trends_keyword list
                item = QStandardItem(f"{count+1}. {name}")
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

                count += 1
        
        # display the list of trends in the widget.
        self.ui.listView_2.setModel(model)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
