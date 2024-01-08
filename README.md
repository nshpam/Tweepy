# 📊 Twitisen – Your Twitterverse ✨📲

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

### 
| **🔍🧐 Competitor Analysis 🧐🔍** |
|:--:|
| ![](https://github.com/nshpam/Tweepy/assets/97942535/8b424da2-23d6-4738-b834-0f814d7b1297) |
| _Before creating our pipeline, we conducted research on other competitors. We aimed to merge the strengths and improve the weaknesses identified during the analysis._ |

## 📐🎨 GUI Designing 🎨📐

This is our initial design, sketched by hand. We created a rough draft of the GUI in a low-fidelity (Lofi) format and transform it into GUI using pyqt5. The disadvantage of this design is...
- No spatial chart
- Few options to extract data
- The search input field is too large.
- Shows only three tabs
- Bad layout
### 
| **🗜️🧩 Prototype 1 🧩🗜️** |
|:--:|
| ![prototype1](https://github.com/nshpam/Tweepy/assets/97942535/e70f31bd-9882-443d-9c76-c957cfde9929) |
| ![prototype1](https://github.com/nshpam/Tweepy/assets/97942535/0315c207-2eb3-4cfd-b24a-7ad7b4df383b) |
| ![prototype1](https://github.com/nshpam/Tweepy/assets/97942535/56ff2128-7225-40e8-913b-a3b10f280921) |
| ![GUI1](https://github.com/nshpam/Tweepy/assets/97942535/71ea1bf0-224d-4df9-a73f-4e1383e1e536) |
| ![GUI1](https://github.com/nshpam/Tweepy/assets/97942535/27408cee-97b3-4c11-b263-93da344bdf82) |
| ![GUI1](https://github.com/nshpam/Tweepy/assets/97942535/78de45f8-46ef-435c-a029-9135e44a8cd7) |



This is our second design. We created a rough draft of the GUI in a low-fidelity (Lofi) format and transform it into GUI using pyqt5. This time we named the program as Twitter Harvest and recolor it into darkmode. The disadvantage of this design is...
- There is an unnecessary push button.
- Too many separate pages make it difficult for users to use.
- The layout of the elements is inconsistent.
- Too many pushbuttons, difficult to use.
### 
| **🗜️🧩 Prototype 2 🧩🗜️** |
|:--:|
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/b6205ebc-2d51-4467-ac77-c40fa90de506) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/0dd149d8-1d86-438b-a258-d78a5ad00e06) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/a682bb45-3b51-43e6-872d-00ddb636c9c4) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/4bbabb69-0e48-4c64-98d0-f27f8b047681) |

Description of prototype 3
### 
| **🗜️🧩 Prototype 3 🧩🗜️** |
|:--:|
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/b6205ebc-2d51-4467-ac77-c40fa90de506) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/0dd149d8-1d86-438b-a258-d78a5ad00e06) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/a682bb45-3b51-43e6-872d-00ddb636c9c4) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/4bbabb69-0e48-4c64-98d0-f27f8b047681) |

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
