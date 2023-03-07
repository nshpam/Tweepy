# coding=utf8
import tweepy
import config
import database_action
import calendar
import datetime
import numpy as np

#testing time related system

#show 2023 year
# print ("The calendar of year 2023 is : ")
# print (calendar.calendar(2023, 2, 1, 6))

#iterate day in week (0 is sunday)
# days = calendar.Calendar().iterweekdays()
# for day in days:
#     print(day)

#show date for specified month
# mock_calendar = calendar.Calendar().monthdatescalendar(2023, 3)
# for week in mock_calendar:
#     for date in week:
#         if date.month == 3:
#             print(type(date), date)

# test_dict = {datetime.date(2022, 12, 30):'yes'}
# print(test_dict)

date_list = [datetime.date(2022, 12, 28).day,
             datetime.date(2022, 12, 29).day,
             datetime.date(2023, 1, 10).day,
             datetime.date(2023, 1, 12).day,
             datetime.date(2023, 1, 15).day,
             datetime.date(2023, 1, 16).day,
             datetime.date(2023, 1, 19).day,
             datetime.date(2023, 1, 20).day]

# date_list = [datetime.date(2023, 1, 10).day,
#              datetime.date(2023, 1, 11).day,
#              datetime.date(2023, 1, 12).day,
#              datetime.date(2023, 1, 13).day,
#              datetime.date(2023, 1, 14).day,
#              datetime.date(2023, 1, 15).day]


def checkConsecutive(l):
    n = len(l) -1
    if sum(np.diff(sorted(l))) == n:
      return True
    return False

# lst = [2, 3, 1, 4, 5]
print(checkConsecutive(date_list))

# db_action = database_action.DatabaseAction()
# db_action.not_print_raw()

# collection = db_action.tweetdb_object(
#     config.mongo_client,
#     config.database_name,
#     config.collection_name
# )

# query_object = db_action.tweetdb_create_object(["_id","date"],[0,1])
# cursor = db_action.tweetdb_show_collection(config.collection_name, collection, query_object)

# time_list = []

# #pull cursor
# for doc in cursor:
#     time_list.append(doc['date'].date())
# time_list = sorted(list(set(time_list)))
# # print(time_list)

# current_date = datetime.datetime.now()
# interval = datetime.timedelta(days=1)
# stop_date = current_date - datetime.timedelta(days=7)
# scrape_date = []

# #find the 7 days ago
# while current_date.date() > stop_date.date():
#     scrape_date.append(current_date.date())
#     current_date -= interval

# #mock the date period
# start_date = datetime.date(2022, 12, 30) #y m d
# end_date = datetime.date(2023, 1, 16)

# #check if the user input correct date
# if not (end_date <= current_date.date() and start_date <= end_date and start_date <= current_date.date()):
#       print('please enter new end_date')
# else:
#      #first checkpoint
#       checkpoint = start_date
#       while checkpoint <= end_date:
            
#             print(checkpoint)

#             previous = checkpoint
#             next = checkpoint

#             if checkpoint > end_date:
#                   previous = end_date
#                   next = end_date
            
#             #check checkpoint
#             if checkpoint not in time_list:
#                   if checkpoint in scrape_date:
#                         print('can scrape %s' %checkpoint)
#                   else:
#                         print('cannot scrape %s'%checkpoint)

#             #check previous and next
#             for i in range(1,8):
#                   #previous
#                   previous -= interval
#                   if previous not in time_list:
#                         if previous in scrape_date:
#                               print('can scrape %s' %previous)
#                         else:
#                               print('cannot scrape %s'%previous)
#                   #next
#                   next += interval
#                   if next not in time_list:
#                         if next in scrape_date:
#                               print('can scrape %s'%next)
#                         else:
#                               print('cannot scrape %s'%next)
            
#             #pin new checkpoint
#             checkpoint += datetime.timedelta(days=14)