from datetime import datetime
import unittest
from unittest.mock import patch
from dateutil import tz
import tweepy_main

#mock input test
class  ConvertTimezoneTest(unittest.TestCase):
    #UTC is not Date/Time
    #test argrument convert_date / test input type
    def test_input_type_string(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        toZoneDate = fromZoneDate.replace(tzinfo=fromZoneUTC)
        convert_time = toZoneDate.astimezone(toZoneUTC).strftime('%d-%m-%Y | %H:%M')
        check = tweepy_main.convert_timezone(fromZoneUTC, toZoneUTC, convert_time)
        assert check == 'Timezone type is not datetime'
        
    def test_input_type_datetime(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        check = tweepy_main.convert_timezone(fromZoneUTC, toZoneUTC, fromZoneDate)
        assert check == fromZoneDate.replace(tzinfo=fromZoneUTC).astimezone(toZoneUTC).strftime('%d-%m-%Y | %H:%M')
        
#run this code if and only if it's the main file
if __name__ == '__main__':
    unittest.main()      
