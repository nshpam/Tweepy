from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import config
class Googleform(object):
    
    def __init__(self):
        self.browser = webdriver.Chrome()  #link chrome driver
        self.browser.get(config.google_form) #open google form

    # enter email address
    def login_user(self,id:str):

        inputemail_boxes.send_keys(config.username)
        # find the next button and click it
        self.browser.find_element(By.XPATH,f'//*[@id="{id}Next"]/div/button').click()
        # wait maximum 10 seconds if finish early it will continue
        self.browser.implicitly_wait(10)

    # enter password
    def login_password(self,id:str):

        self.browser.implicitly_wait(10)

    # clear any previous answers in the form
    def clear_form(self):
        # clicks the "Clear" button on the form to do so
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[2]/div/span/span').click()
        self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span').click()
        # wait maximum 10 seconds if finish early it will continue
        self.browser.implicitly_wait(10)

    # elect one choice in the form
    def choice(self):
        choiceid_page1 = '8','18','43','53'
        # loops through a list of choice IDs
        for id in choiceid_page1:
            # waits for 0.5 seconds before clicking on the choice.
            time.sleep(0.5)
            # clicks the corresponding choice for each ID
            self.browser.find_element(By.XPATH,f'//*[@id="i{id}"]/div[3]/div').click()
            # clicks the "Submit" button
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
        # waits for 1 seconds before clicking on the choice.
        time.sleep(1)

    # select multiple choices in the form
    def multichoice(self):
        choiceid_page2 = '6','9','26','38'
        # loops through a list of choice IDs
        for id in choiceid_page2:
            # waits for 0.5 seconds before clicking on the choice.
            time.sleep(0.5)
            # clicks the corresponding choice for each ID
            self.browser.find_element(By.XPATH,f'//*[@id="i{id}"]/div[2]').click()
        # waits for 1 seconds before clicking on the choice.
        time.sleep(1)

    # select dropdown answers in the form
    def dropdowns(self):
        dropdownid = 'div[1]/div[1]/div[1]','div[2]/div[3]'
        # loops through a list of dropdown IDs 
        for id in dropdownid:
            # waits for 0.5 seconds before clicking on the choice.
            time.sleep(0.5)
            # clicks the corresponding dropdown for each ID
            self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/{id}').click()
        # waits for 1 seconds before clicking on the choice.
        time.sleep(1)
        # clicks the "Submit" button.
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()

    # enter a time and seconds into the form
    def times(self):
        timeid = 'div[1]/div[2]','div[3]/div'
        # loops through a list of time IDs
        for i in range(len(timeid)):
            # waits for 0.5 seconds
            time.sleep(0.5)
            date_time = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/{timeid[i]}/div[1]/div/div[1]/input')
            # enters the corresponding time into each time box
            date_time.send_keys(config.timebox[i])
        # waits for 1 seconds before clicking on the choice.
        time.sleep(1)

    # enter a date into the form
    def calender(self):
        # locates the date input box
        calender = self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
        # enters the date, month, and year from a configuration file
        calender.send_keys(config.date, config.month, config.year)
        # waits for 1 seconds before clicking on the choice.
        time.sleep(1)

    # enter short answers and text into the form
    def Text(self):
        textid = 'div[4]','div/div[1]/input','div[5]','div[2]/textarea'
        text_answer = config.text_answer
        # loops through a list of text IDs
        for i in range(0,len(textid),2):
            # locates the corresponding text box for each ID
            input_answer = self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/{textid[i]}/div/div/div[2]/div/div[1]/{textid[i+1]}')
            # enters the text answer from a configuration file
            input_answer.send_keys(text_answer[i//2])
        time.sleep(1)
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()

    # multi table question and choose one choice 
    def choiceTable(self):
        choiceTableid = 'div[2]/span/div[3]','div[4]/span/div[3]','div[6]/span/div[3]','div[8]/span/div[4]','div[10]/span/div[3]'
        # loop over the `choiceTableid` list and select one choice for each question.
        for id in choiceTableid:
            # wait for 0.5 seconds before clicking on the choice.
            time.sleep(0.5)
            # select a choice for each question by clicking on it. The choice is identified by the XPATH.
            self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/{id}/div/div/div[3]/div').click()
        # wait for 1 second after all choices are selected.
        time.sleep(1)
        
    # choose multi label choice
    def labelChoice(self):
        # select a choice for the multi label question by clicking on it. The choice is identified by the XPATH.
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[1]/span/div/label[4]/div[2]/div/div/div[3]/div').click()
        # wait for 0.5 seconds after the choice is selected.
        time.sleep(0.5)
        
    # multi table question and choose multi choice
    def multiTable_button(self):
        mutiTableid = 'div[2]/label[1]','div[2]/label[2]','div[4]/label[2]','div[4]/label[7]'
        # loop over the `mutiTableid` list and select multiple choices for each question.
        for id in mutiTableid:
            # wait for 0.5 seconds before clicking on the choice.
            time.sleep(0.5)
            # select a choice for each question by clicking on it. The choice is identified by the XPATH.
            self.browser.find_element(By.XPATH,f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/{id}/div/div/div[2]').click()
        # wait for 1 second after all choices are selected.
        time.sleep(1)

    # play youtube video
    def play_video(self):
        # locate the video element using its XPATH and click on it to start playing
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div[2]/iframe').click()
        # wait for 3 seconds after the video starts playing.
        time.sleep(3)
        # locate the submit button and finally clicks 
        self.browser.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[2]/div[1]/div[2]/span').click()
        # wait for 2 second after clicks the "Submit" button
        time.sleep(2)

if __name__ == '__main__':

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
