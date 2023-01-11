#twitter developer token
consumer_key = 'Zsj2fTEUS4IU9h7wJhA2CeaKt' #API Key
consumer_secret = 'GeukQOhgWKKHHKHLTh0wGjcwixl3p6KxYqxIc8uqrNoRMFVoaW' #API Key Secret
access_token = '3302501826-yxgMxO6n1A1aXmVXS45x7zHP8FLkcSitvNyEQw4' #access token
access_token_secret = 'CwVEYsPoXpHJvYzbZvxlKv3mC8XlyYynmDRgsKLxauTMu' #access token secret

#database settings
mongo_client = 'mongodb://localhost:27017/' #mongodb server
database_name = "twitter_data" #database name
collection_name = "tweets" #collection name
collection_name_2 = "tokenization" #collection name for clean data

#search settings
search_word = '#รีวิวหนัง' #search word
search_mode = "extended" #search mode
search_type = "recent" #serach type ( recent | popular | mixed )
num_tweet = 20 #search limit
local_timezone = "Thailand/Bangkok" #local timezones

#task settings
task_period = 5 #minutes
task_delay = 1 #seconds
task_terminate_timeout = 5 #seconds

#Lexto+ settings
LextoPlus_API_key = 'Ex0WSb2UFAyfDXRU8vLwkeR04N6e58Tq' 
LextoPlus_URL = 'https://api.aiforthai.in.th/lextoplus'
LextoPlus_Norm = '1' #normalization activation ( 0 deactivate | 1 activate )
