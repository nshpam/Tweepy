# coding=utf8

from unidecode import unidecode
import twitterDataProcessing
import config
import re

test = ' 📼 𝐍𝐞𝐭𝐟𝐥𝐢𝐱 𝐔𝐥𝐭𝐫𝐚 𝐇𝐃 𝐊 📼 🏷  day ฿ -แอคไทยแท้  % -ไม่ต้องเปิด vpn ขณะดู 🛒                : #netflixราคาถูก #หารnetflixราคาถูก #หารnetflix #หารnetflixTH #NetflixTH #รีวิวหนัง #หารเน็ตฟลิกซ์ราคาถูก #หารnetflixราคาถูก #หารเน็ตฟลิกซ์รายเดือน'

print(test)

# my_dict = {}
# temp = ''

# test = '🎉🎉 งานดีดีมาแล้ว อยากบอกต่อ🎉🎉\n‼️ work  from home ‼️\n📍หาเงินค่าขนม ค่าหนังสือ บัตรคอนได้สบายๆ\n#พาร์ทไทม์ No experience needed\n💌สจ.@ไลน์หน้าไบโอเลยค่าาา  #เครื่องบินกระดาษ #งานวันเด็ก #งานออนไลน์ฟรี #งานวิจัย #งานแต่ง #หาค่าขนม #หาเงินออนไลน์ #รีวิวซีรี่ย์เกาหลี #รีวิวหนัง https://t.co/FJpLLYllUB'
# test = '🧸ส่งต่อตุ๊กตาน่ารักๆ ป้ายห้อย มือ1 ของแท้100%\n💖Sale ตัวละ  200 บ. \nรับน้องหลายตัว ลดได้ค่ะ\nDM มาได้เลยย🥰\n\n #ส่งต่อ #ส่งต่อเสื้อผ้า #ส่งต อสกินแคร์ #เสื้อผ้ามือสอง #ตุ๊กตามือสอง #มือสอง #มือสองสภาพดี #รองเท้ามือสองของแท้ #รีวิวหนัง #ของขวัญปีใหม่ #ส่งต่อเสื้อผ้ามือ2 https://t.co/UnnwsLe22F'
# test_list = test
# test = 'sngt`tuktaanaarak+ 🧸ส่งต่อตุ๊กตาน่ารักๆ ป้ายห้อย มือ ของแท้% Sale ตัวล ะ บ. รับน้องหลายตัว ลดได้ค่ะ มาได้เลยย🥰 #ส่งต่อ #ส่งต่อเสื้อผ้า #ส่งต อสกินแคร์ # เสื้อผ้ามือสอง #ตุ๊กตามือสอง #มือสอง #มือสองสภาพดี #รองเท้ามือสองของแท้ #รีวิวหนัง #ของขวัญปีใหม่ #ส่งต่อเสื้อผ้ามือ'

# test = '〰️ NETFLIX THAI 💒  \n𓏔 7 day — 28 baht          \n𓏔 30 day — 92 baht ❌\n𓏔 37 day — 110 baht ❌\n#หารnetfilxราคา   ถูก #หารnetfilx #หารเน็ตฟลิกซ์ราคาถูก #หารnetflix #หารnetflixTH #รีวิวหนัง #รีวิวหนังสนุก'
# filter = twitterDataProcessing.FilterData()
# test = filter.FilterUrlAndFilterNum(test)
# test = filter.FilterSpecialChar(test)
# # test = filter.ThaiCleansing({'text' : test})['cleansing_text']

# my_dict['text'] = test
# my_dict['norm'] = '1'

# print('🧸ส่งต่อตุ๊กตาน่ารักๆ'.isalnum())

# print(my_dict['text'])

# test = 'ของแท้%'

# regex = re.compile('[@_!#$%^&*()<>?/\|~:]')
# print(regex.search(test))

# print(test.isalnum())

# res = twitterDataProcessing.ConnectLextoPlus().ConnectApi(
#     config.LextoPlus_API_key, 
#     config.LextoPlus_URL, 
#     my_dict)

# print(res.text)



# print(test)

# print(unidecode(x))


# for list_word in test.split():

#     my_dict[list_word] = list_word.encode('ascii','namereplace').decode('utf-8').split('\\N')
#     my_dict[list_word] = my_dict[list_word][1:]

#     for word in my_dict[list_word]:
#         if 'THAI' not in word and '{' in word and '}' in word:
#             if unidecode(list_word) not in temp.split():
#                 temp += ' ' + unidecode(list_word)
#             continue
#         temp += ' ' + list_word
#         break

# print(temp)

