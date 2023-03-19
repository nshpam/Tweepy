# coding=utf8
import tweepy
import config
import calendar
import datetime
import database_action
import numpy as np
import twitterDataProcessing

# input = 'ยาพลังช้างก็มาจ้า!!#TheLostHeroOfAyodhya#ขุนแหย  #หนังไทย #หนังสนุก #ดูหนัง #หนังตลก #รีวิวหนัง #moive22hd #ดูหนังเต็มเรื่อง #ดูหนังมันส์ๆ #ดูหนังสนุกๆ #ดูหนังในโรงภาพยนตร์ https://t.co/NQecJ2jzVz'
input = 'ยาพลังช้างก็มาจ้า!! # TheLostHeroOfAyodhya#ขุนแหย  #หนังไทย #หนังสนุก #ดูหนัง #หนังตลก #รีวิวหนัง #moive22hd #ดูหนังเต็มเรื่อง #ดูหนังมันส์ๆ #ดูหนังสนุกๆ #ดูหนังในโรงภาพยนตร์ https://t.co/NQecJ2jzVz'

print(twitterDataProcessing.FilterData().Filters(input))

# hashtags = input.split('#')
# remove_word = []
# test = '#ดูหนังในโรงภาพยนตร์ https://t.co/NQecJ2jzVz'.split()

# #find the word to remove
# for word in hashtags:

#     if word.startswith(' '):
#        print(word)
#        continue
#     try: 
#       hashtag = input[input.index(word)-1]
#       if hashtag == '#':
#         check_hashtags = word.split()
#         filter_hashtags = word
#         # print(check_hashtags)
#         if len(check_hashtags)>1:
#             filter_hashtags = check_hashtags[0]
#         remove_word.append(hashtag+filter_hashtags)
#     except:
#       continue

# # print(remove_word)

# for word in remove_word:
#    input = input.replace(word,'')
  
# print(input)
  



    
    

# output_string = ""
# for word in hashtags:
#     if not word.startswith("#"):
#         output_string += word + " "
#     elif len(word) > 1:
#         output_string = output_string.rstrip() + " "

# print(output_string.strip())