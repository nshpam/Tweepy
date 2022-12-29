from datetime import datetime
from dateutil import tz
import tweepy_main
fromZoneUTC = tz.gettz('UTC')
toZoneUTC = tz.gettz('Asia/Bangkok')
    
fromZoneDate = datetime.utcnow()
toZoneDate = fromZoneDate.replace(tzinfo=fromZoneUTC)

convertDate = toZoneDate.astimezone(toZoneUTC)

# from_time = '20:46'
# print(type(fromZoneDate))
# print(type(from_time))
# print(type(convertDate))
# check = type(tweepy_main.convert_timezone(fromZoneUTC, toZoneUTC, fromZoneDate))
# print(check)
print(type(fromZoneDate.replace(tzinfo=fromZoneUTC).astimezone(toZoneUTC).strftime('%d-%m-%Y | %H:%M')))
print(type(datetime.utcnow()))