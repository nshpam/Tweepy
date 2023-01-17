from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import config

# not turn off auto
option = Options()
option.add_experimental_option('detach', True)
browser = webdriver.Chrome(config.path,options=option)

browser.get(config.google_form)

# Use the following snippets to get elements by their XPath
inputemail_boxes = browser.find_element(By.XPATH,'//*[@id="identifierId"]')
inputemail_boxes.send_keys(config.username)
submitemail_button = browser.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button').click()
browser.implicitly_wait(10)
inputpassword_boxes = browser.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')
inputpassword_boxes.send_keys(config.password)
submitpassword_button = browser.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button').click()
browser.implicitly_wait(10)

# clear form
clear_all = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[2]/div/span/span').click()
time.sleep(1)
submitclear_all = browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span').click()
time.sleep(1)

#page1

# pause the program for 2 seconds before continuing execution.
time.sleep(2) 
choice_gender_button = browser.find_element(By.XPATH,'//*[@id="i8"]/div[3]/div').click()
time.sleep(1)
choice_old_button = browser.find_element(By.XPATH,'//*[@id="i18"]/div[3]/div').click()
time.sleep(1)
choice_work_button = browser.find_element(By.XPATH,'//*[@id="i43"]/div[3]/div').click()
time.sleep(1)
choice_salary_button = browser.find_element(By.XPATH,'//*[@id="i53"]/div[3]/div').click()
time.sleep(1)
nextpage1_button =browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()

# page2
time.sleep(2)

multichoice_time1_button = browser.find_element(By.XPATH,'//*[@id="i6"]/div[2]"]').click()
time.sleep(1)
multichoice_time2_button = browser.find_element(By.XPATH,'//*[@id="i9"]/div[2]').click()
time.sleep(1)

multichoice_buffet1_button = browser.find_element(By.XPATH,'//*[@id="i26"]/div[2]').click()
time.sleep(1)
multichoice_buffet2_button = browser.find_element(By.XPATH,'//*[@id="i38"]/div[2]').click()
time.sleep(1)

dropdown = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
time.sleep(1)
list_dropdown = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[3]').click()
time.sleep(1)

nextpage2_button = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()
time.sleep(2)
fill_time = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/input')
fill_time.send_keys(config.time_order)
fill_second = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div/div[1]/input')
fill_second.send_keys(config.second_order)
time.sleep(2)

calender = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
calender.send_keys(config.date, config.month, config.year)
time.sleep(2)

input_short_answer = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
input_short_answer.send_keys(config.short_answer)
time.sleep(2)
input_text_answer = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea')
input_text_answer.send_keys(config.text_answer)
time.sleep(2)

nextpage3_button = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()
time.sleep(2)
 
#page3
product_tast_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/span/div[3]/div/div/div[3]/div').click()
time.sleep(0.5)
product_quality_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[4]/span/div[3]/div/div/div[3]/div').click()
time.sleep(0.5)
product_clean_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[6]/span/div[3]/div/div/div[3]/div').click()
time.sleep(0.5)
product_fresh_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[8]/span/div[4]/div/div/div[3]/div').click()
time.sleep(0.5)
product_multimenu_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[10]/span/div[3]/div/div/div[3]/div').click()
time.sleep(0.5)

promotion_tablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[1]/span/div/label[4]/div[2]/div/div/div[3]/div').click()
time.sleep(0.5)

travelto1_multitablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[2]/label[1]/div/div/div[2]').click()
travelto2_multitablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[2]/label[2]/div/div/div[2]').click()
time.sleep(0.5)
returntrip1_multitablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[4]/label[2]/div/div/div[2]').click()
returntrip2_multitablebutton = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[4]/label[7]/div/div/div[2]').click()
time.sleep(0.5)

playvideo = browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div[2]/iframe').click()
time.sleep(3)




