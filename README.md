# 📊 Tweepy – Your Twitterverse ✨📲

In our Software Developer coursework, we utilized the Twitter API to collect tweet data and employed Natural Language Processing (NLP) for in-depth analysis. The program, designed with user-friendly principles, seamlessly integrates Python, Unittest for rigorous testing, and an Extract, Load, Transform (ELT) pipeline for efficient data processing. With a strong emphasis on data visualization techniques, we've created a versatile tool that not only collects Twitter data but also employs NLP for insightful analysis. The program doesn't just gather information; it transforms raw data into meaningful visualizations, showcasing trends and patterns derived from the Twitterverse. This project highlights our collaborative synergy in developing a comprehensive and effective computer program for Twitter data analysis and visualization. We store the data securely in MongoDB.

## Lessons Learned 🎓 

#### NLP
- [Description]

#### Python Programming
- [Description]

#### Twitter API
- [Description]

#### GUI
- [Description]

#### Unittest
- [Description]

#### Data Visualization
- [Description]

#### ELT pipeline
- [Description]

## Screenshots 📷

### 
| **🛢️🔗 ELT Pipeline 🔗🛢️** |
|:---| 
| ![Exclusive Summary](https://github.com/nshpam/Tweepy/assets/97942535/5eb17cf8-64fd-432e-b80e-204c3b4959e5) |
|**Firstly,** we extract tweets from the Twitter API. The API provides information such as id, username, datetime, text, favorite count, retweet count, and location.<br>**Secondly,** we store the extracted data in MongoDB, referring to this dataset as raw data.<br>**Thirdly,** we apply a complex algorithm to transform the data. We filter out URL symbols, numeric symbols, emojis, and special characters using our custom implementation and Lexto+. Given the dataset's diverse language composition, our focus is solely on Thai and English. For Thai language, we tokenize and normalize using Lexto+, while for English, we utilize NLTK. We clean Thai stop words with PythaiNLP and English stop words with NLTK.<br>**Fourthly,** we store the cleaned data in MongoDB, naming this dataset as clean data.<br>**Lastly,** we utilize the cleaned data for data visualization. The visualization includes sentiments, a donut chart, word cloud, bar chart, and spatial chart, all of which are presented on the GUI.|

### 
| **🗂️💽 Database Schema 💽🗂️** |
|:--:| 
| ![](https://github.com/nshpam/Tweepy/assets/97942535/e8189a5d-6c9c-49d9-b71c-8321f7402025) |
|_We have four independent databases. The **'tweets'** database will contain raw data collected from the Twitter API. The **'cleaned_data'** database will store transformed or cleaned data. The **'locations'** database will include the location and coordinates of tweets. The **'sentiments'** database will house keywords that users use for searching in the Twitter search bar and the corresponding ranked results._|

| tweets      | cleaned_data | locations |  sentiments    |
|  :----:         |    :----:   |    :----:   |          :----:  |
| **PK:** id<br>**FK:** location      | **PK:** id       | **PK:** id   |**PK:** id |

## Contributor 👩‍💻👨‍💻
- [@nshpam](https://github.com/nshpam) [Back-End]
- [@tw94sh](https://github.com/tw94sh) [Front-End]

Features
- Extract Twitter Data
- Clean the data
- Ranking top 10 keyword
- Ranking top 10 key
- Sentiment
- Update engine
- Remove engine
- Search engine
- Tableau data visulization
- Data visulization from tweets
- Unit test case
- ELT pipeline
- Database Schema
