import config
import datetime
import database_action
import twitterDataProcessing

db_action = database_action.DatabaseAction()
db_action.not_print_raw()

start_collection =  db_action.tweetdb_object(config.mongo_client, config.database_name, config.old_collection)
des_collection =  db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

#field for start database
# data_field_1 = ["_id", "id", "username", "date", "time", "text", "favorite_count", "retweet_count"]
# data_list_1 = [0, 1, 1, 1, 1, 1, 1, 1]

#field for des database
data_field_2 = ["_id", "id", "keyword", "username", "date", "location", "text", "favorite_count", "retweet_count"]
data_list_2 = [0, 1, 1, 1, 1, 1, 1, 1, 1]

# query_object_1 = db_action.tweetdb_create_object(data_field_1, data_list_1)
query_object_2 = db_action.tweetdb_create_object(data_field_2, data_list_2)

# collection_1 = db_action.tweetdb_object(config.mongo_client, config.database_name, config.old_collection)
collection_1 = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_4)
collection_2 = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

# cursor_1 = db_action.tweetdb_show_collection(config.collection_name, collection_1, query_object_1)
cursor_1 = db_action.tweetdb_show_collection(config.collection_name_4, collection_1, query_object_2)
cursor_2 = db_action.tweetdb_show_collection(config.collection_name, collection_2, query_object_2)

my_filter = twitterDataProcessing.FilterData()
check_dict = {}
data_dict = {}

#get all data from old database
for doc in cursor_1:
    raw_list = doc['text'].split()
    clean_json = ''

    #filter the url from word
    for word in raw_list:
        if not my_filter.FilterUrl(word):
            clean_json += word

    if clean_json not in list(check_dict.values()):
        #reversing the str format into datetime
        # dt = datetime.datetime.strptime(doc['date']+' '+doc['time']+':00', '%d-%m-%Y %H:%M:%S')

        #convert it to iso format and convert it into datetime data type
        # dt = datetime.datetime.fromisoformat(dt.isoformat())

        #create the data object
        # temp_data_list = [int(doc['id']),'#รีวิวหนัง', doc['username'], dt, None, doc['text'], doc['favorite_count'], doc['retweet_count']]
        temp_data_list = [int(doc['id']),doc['keyword'], doc['username'], doc['date'], None, doc['text'], doc['favorite_count'], doc['retweet_count']]
        data_object = db_action.tweetdb_create_object(data_field_2[1:], temp_data_list)

        #dictionary for checking
        check_dict[doc['id']] = clean_json
        data_dict[doc['id']] = data_object

print('filtered :',len(list(check_dict.values())))

data_list = list(data_dict.values())

def pull_all_data(cursor):

      all_data = []

      for doc in cursor:
         raw_list = doc['text'].split()
         clean_data = ''
         for word in raw_list:
            if not my_filter.FilterUrl(word):
               clean_data += word
         all_data.append(clean_data)
      
      return all_data

def check_duplicate(text, cursor):
      raw_list = text.split()
      clean_data = ''
      
      for word in raw_list:
         if not my_filter.FilterUrl(word):
            clean_data += word
      
      if clean_data in pull_all_data(cursor):
         return True
      return False

duplicate_count = 0
count = 0

#insert the data to cleaned_data
for i in range(len(data_list)):

    #find object using id
    query_object_3 = db_action.tweetdb_create_object(["id"],[data_list[i]['id']])
    cursor_3 = db_action.tweetdb_find(config.collection_name, collection_2, query_object_3)

    cursor_4 = db_action.tweetdb_show_collection(config.collection_name, collection_2, query_object_2)
    #duplicate id
    if list(cursor_3) != []:
        data_field_3 = ['favorite_count', 'retweet_count']
        data_list = [data_list[i][data_field_3[0]], data_list[i][data_field_3[1]]]
        duplicate_count+=1
    if check_duplicate(data_list[i]['text'], cursor_4):
        # print('the context duplicate :', data_list[i]['text'] )
        duplicate_count+=1
    else:
        count +=1
        db_action.tweetdb_insert(config.collection_name, collection_2, data_list[i])

print('finish')
print('duplicate count :', duplicate_count)
print('inserted count :', count)