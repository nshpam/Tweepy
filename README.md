# 📊 Twitisen – Your Twitterverse ✨📲

In our Software Developer coursework, we utilized the Twitter API to collect tweet data and employed Natural Language Processing (NLP) for in-depth analysis. The program, designed with user-friendly principles, seamlessly integrates Python, Unittest for rigorous testing, and an Extract, Load, Transform (ELT) pipeline for efficient data processing. With a strong emphasis on data visualization techniques, we've created a versatile tool that not only collects Twitter data but also employs NLP for insightful analysis. The program doesn't just gather information; it transforms raw data into meaningful visualizations, showcasing trends and patterns derived from the Twitterverse. This project highlights our collaborative synergy in developing a comprehensive and effective computer program for Twitter data analysis and visualization. We store the data securely in MongoDB.

## Lessons Learned 🎓  

### 🧠 NLP (Natural Language Processing) 🧠
- 📈 Implementing NLP techniques for sentiment analysis to gauge user opinions.
- ⚙️ **Filtering Unnecessary Data:** Removing emojis and special characters to clean the text.
- ✂️ **Tokenization:** Breaking down text into individual tokens (words or phrases).
- ⚖️ **Normalization:** Converting verbs from their base form (Verb 3) to their infinitive form (Verb 1).
- ⛔ **Removing Stopwords:** Eliminating common words (e.g., "the," "and") that don't carry significant meaning.
- 📊 **Sentiment Analysis:** Determining the emotional tone or sentiment expressed in the text.

### Python Programming
- 🐍 Mastering Python for efficient scripting and data manipulation.
- 🧪 Writing modular and reusable code for improved maintainability.
- 🌐 Utilizing Python for data extraction, transformation, and loading (ETL) processes.

### Twitter API
- 🕊️ Extracting data from Twitter using the Twitter API.
- 🔄 Transforming raw Twitter data for analysis and visualization.

### GUI (Graphical User Interface)
- 🖥️ Developing user-friendly graphical interfaces for data visualization.
- 🎨 Enhancing user experience through intuitive design.

### Unittest
- 🧪 Implementing unit tests for code reliability and robustness.
- 🚀 Ensuring the correctness of data extraction and transformation processes.

### Data Visualization
- 📊 Creating compelling visualizations to convey insights effectively.
- 📈 Using tools like Matplotlib or Plotly for graphical representation.

### ELT Pipeline (Extract, Load, Transform)
- 🚀 Designing and implementing efficient ELT pipelines.
- 🔄 Extracting data from various sources, transforming it, and loading it into databases.

### MongoDB
- 🗄️ Storing and retrieving data efficiently using MongoDB.
- 🔐 Ensuring data security and scalability.

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

###
| **🤖📥 Extracting Algorithm 📥🤖** |
|:--:|
| ![extract](https://github.com/nshpam/Twitisen/assets/97942535/588c6f1c-0e39-48aa-a1a7-b2c8e4c749d1) |
| ![extract](https://github.com/nshpam/Twitisen/assets/97942535/3314fbee-e9ce-4e22-9c5f-c8f431ffe9e0) |


###
| **📅🕑 Timeline Classification 🕑📅** |
|:--:|
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/0b81fcb3-2d63-4626-8e0b-a25435e68df9) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/f505b253-7cb0-47c3-924a-cd549c4f3d9a) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/9e833cea-7db0-4ea2-85cd-d75a72c05abf) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/b335c54f-e441-4300-a8b7-7f881fc81e09) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/82be072d-5eab-4207-b18f-ae6b110120c9) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/5de089e7-fc07-4311-b4e5-ee221af37d28) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/b4639189-32f8-4448-ae7b-8a2b1f1cdbc3) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/7e44bdcc-080b-45ed-ac6e-b40168a2314c) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/7e618d7a-e0e9-4b2c-b2c6-7be3f31fc18b) |
| ![timeline](https://github.com/nshpam/Twitisen/assets/97942535/7639f957-64b7-46b7-a577-72348ff54e7e) |

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
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/0c119b90-da8e-40d9-abb4-b04eb6eb1d3b) |
| ![prototype2](https://github.com/nshpam/Tweepy/assets/97942535/4167519a-72c8-49ba-a336-6a87287c45c7) |

Description of prototype 3
### 
| **🗜️🧩 Prototype 3 🧩🗜️** |
|:--:|
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/33730fbc-6612-4598-9c00-0e512134500e) |
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/9a9d3df6-1a6e-426c-9afa-4041930ee1e1) | 
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/37c87d6d-1696-47bf-8116-7a6f63ee9f24) |
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/7bf4372c-6416-471d-bce1-ad8465afd585) |
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/8446e361-be86-49c2-9c74-95ebf2eb07e9) |
| ![prototype3](https://github.com/nshpam/Tweepy/assets/97942535/af2afb7e-284f-4e98-9c07-573dad61c1f4) |
| ![prototype3](https://github.com/nshpam/Twitisen/assets/97942535/ee2b0186-5d71-47c0-9890-3b4855885092) |
| ![prototype3](https://github.com/nshpam/Twitisen/assets/97942535/16040b85-13f2-4028-9b1e-96277388ac2a) |

Description of version 1.0
### 
| **🎉🚀 Version 1.0 🎉🚀** |
|:--:|
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/376ed73e-85e9-4742-ac44-99b14f4f66d1) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/8af1e118-7524-4fed-b123-72ace78ab302) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/ebba16ac-97d0-4b04-ab7b-60c567f6bd0e) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/9da36b3f-f306-414f-ae5b-91cbeeb2a3cc) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/7fda138a-3677-411b-8df1-f0b3c704ff0a) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/4570e905-6886-430e-9832-2a234ec93fc9) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/76be9ac5-ebc4-4efd-9ed6-586d89fb86a2) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/fe03b3c5-3088-4f4d-becc-a987b3047359) |
| ![ver1](https://github.com/nshpam/Twitisen/assets/97942535/092b0e8e-3c4d-42bc-a3ef-5285e5ae76a7) |

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
