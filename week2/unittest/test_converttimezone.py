from datetime import datetime
import unittest
from unittest.mock import patch
from dateutil import tz
import sys

sys.path.insert(0, '../')
from tweepy_main import PullTwitterData

convert = PullTwitterData()

class  ConvertTimezoneTest(unittest.TestCase):
    
    #test input is empty 
    def test_InputNull(self):
        check = convert.convert_timezone(None,None,None)
        assert check == 'Timezone type is not datetime'
        
    #UTC is not Date/Time
    # test argrument 'convert_date' / test input type
    #fix this
    def test_ConvertDateInputTypeString(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        
        toZoneDate = fromZoneDate.replace(tzinfo=fromZoneUTC)
        convert_time = toZoneDate.astimezone(toZoneUTC).strftime('%d-%m-%Y | %H:%M')
        check = convert.convert_timezone(fromZoneUTC, toZoneUTC, convert_time)
        assert check == 'Timezone type is not datetime'

    #fix this
    def test_ConvertDateInputTypeDatetime(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Thailand/Bangkok')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(fromZoneUTC, toZoneUTC, fromZoneDate)
        assert check == fromZoneDate.replace(tzinfo=fromZoneUTC).astimezone(toZoneUTC)
        
    def test_ConvertDateInputTypeInt(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        check = convert.convert_timezone(fromZoneUTC, toZoneUTC,1)
        assert check == 'Timezone type is not datetime'
        
    #test argrument 'from_zone' / test input type
    def test_From_zoneInputTypeString(self):
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        # fromZoneStr = fromZoneDate.strftime('%d-%m-%Y | %H:%M')
        check = convert.convert_timezone('String', toZoneUTC, fromZoneDate)
        assert check == 'Timezone type is not timezone'
        
    def test_From_zoneInputTypeDatetime(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(fromZoneUTC, toZoneUTC, fromZoneDate)
        assert check == 'Timezone type is not timezone'
        
    def test_From_zoneInputTypeInt(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(1, toZoneUTC, fromZoneDate)
        assert check == 'Timezone type is not timezone'
        
        
    #test argrument 'to_zone' / test input type
    def test_To_zoneInputTypeString(self):
        fromZoneUTC = tz.gettz('UTC')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(fromZoneUTC, 'String', fromZoneDate)
        assert check == 'Timezone type is not timezone'
        
    def test_To_zoneInputTypeDatetime(self):
        fromZoneUTC = tz.gettz('UTC')
        toZoneUTC = tz.gettz('Asia/Bangkok')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(fromZoneUTC, toZoneUTC, fromZoneDate)
        assert check == 'Timezone type is not timezone'
        
    def test_To_zoneInputTypeInt(self):
        fromZoneUTC = tz.gettz('UTC')
        fromZoneDate = datetime.utcnow()
        check = convert.convert_timezone(fromZoneUTC, 1, fromZoneDate)
        assert check == 'Timezone type is not timezone'

#run this code if and only if it's the main file
if __name__ == '__main__':
    unittest.main()      
