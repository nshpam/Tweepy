from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import config

class Googleform(object):
    # link chrome driver and open google form
    def __init__(self):
        self.browser = webdriver.Chrome(config.path)
        self.browser.get(config.google_form)
    # enter email address
    def login_user(self,id:str):
        inputemail_boxes = self.browser.find_element(By.XPATH,f'//*[@id="{id}Id"]')
        inputemail_boxes.send_keys(config.username)
        submitemail_button = self.browser.find_element(By.XPATH,f'//*[@id="{id}Next"]/div/button').click()
        self.browser.implicitly_wait(10)
    # enter password
    def login_password(self,id:str):
        inputpassword_boxes = self.browser.find_element(By.XPATH,f'//*[@id="{id}"]/div[1]/div/div[1]/input')
        inputpassword_boxes.send_keys(config.password)
        submitpassword_button = self.browser.find_element(By.XPATH,f'//*[@id="{id}Next"]/div/button').click()
        self.browser.implicitly_wait(10)
    # clean all answer in form
    def clear_form(self):
        clear_all = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[2]/div/span/span').click()
        submit_clearall = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span').click()
        self.browser.implicitly_wait(10)
    # select one choice
    def choice(self):
        choiceid_page1 = '8','18','43','53'
        for id in choiceid_page1:
            time.sleep(0.5)
            onechoice_page1 = self.browser.find_element(By.XPATH,f'//*[@id="i{id}"]/div[3]/div').click()
        nextpage1_button =self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
        time.sleep(1)
    # select multiple choices
    def multichoice(self):
        choiceid_page2 = '6','9','26','38'
        for id in choiceid_page2:
            time.sleep(0.5)
            multichoice_page2 = self.browser.find_element(By.XPATH,f'//*[@id="i{id}"]/div[2]').click()
        time.sleep(1)
    # select dropdown answer
    def dropdowns(self):
        dropdownid = 'div[1]/div[1]/div[1]','div[2]/div[3]'
        for id in dropdownid:
            time.sleep(0.5)
            dropdown = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/{id}').click()
        time.sleep(1)
        nextpage2_button = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()
    # enter the time and seconds.
    def times(self):
        timeid = 'div[1]/div[2]','div[3]/div'
        for i in range(len(timeid)):
            time.sleep(0.5)
            date_time = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/{timeid[i]}/div[1]/div/div[1]/input')
            date_time.send_keys(config.timebox[i])
        time.sleep(1)
    # enter date
    def calender(self):
        calender = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
        calender.send_keys(config.date, config.month, config.year)
        time.sleep(1)
    # enter short answer and text
    def Text(self):
        textid = 'div[4]','div/div[1]/input','div[5]','div[2]/textarea'
        text_answer = config.text_answer
        for i in range(0,len(textid),2):
            input_answer = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/{textid[i]}/div/div/div[2]/div/div[1]/{textid[i+1]}')
            input_answer.send_keys(text_answer[i//2])
        time.sleep(1)
        nextpage3_button = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()
    # multi table question and choose one choice 
    def choiceTable(self):
        choiceTableid = 'div[2]/span/div[3]','div[4]/span/div[3]','div[6]/span/div[3]','div[8]/span/div[4]','div[10]/span/div[3]'
        for id in choiceTableid:
            time.sleep(0.5)
            onechoice_tablebutton = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/{id}/div/div/div[3]/div').click()
        time.sleep(1)
    # choose multi label choice 
    def labelChoice(self):
        promotion_tablebutton = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[1]/span/div/label[4]/div[2]/div/div/div[3]/div').click()
        time.sleep(0.5)
    # multi table question and choose multi choice 
    def multiTable_button(self):
        mutiTableid = 'div[2]/label[1]','div[2]/label[2]','div[4]/label[2]','div[4]/label[7]'
        for id in mutiTableid:
            time.sleep(0.5)
            multiTablebutton = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/{id}/div/div/div[2]').click()
        time.sleep(1)
    # play youtube video
    def play_video(self):
        playvideo = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div[2]/iframe').click()
        time.sleep(3)
        nextpage4_button = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[2]/div[1]/div[2]/span').click()
        time.sleep(2)
    
form = Googleform()
form.login_user('identifier')
form.login_password('password')
form.clear_form()
form.choice()
form.multichoice()
form.dropdowns()
form.times()
form.calender()
form.Text()
form.choiceTable()
form.labelChoice()
form.multiTable_button()
form.play_video()
