#import file
import tweepy_main  #contain method for scraping the twitter
import config       #contain configuration of the application
import twitterDataProcessing    #contain tokenization, normalization, cleanword

#import library
import tweepy       #use for twitter scrapping
import time         #use for timer
from threading import Thread    #use for dealing with intensive-task by using thread
import schedule     #use for schedule the task
import datetime     #use for timestamp
from dateutil import tz     #use for timestamp
from inputimeout  import inputimeout


#Connect to Twitter API
class ConnectTwitterData():

    #connect Twitter API Method
    def connect_twitter():

        #input consumer_key, consumer_secret, access_token, access_token_secret
        #you can edit those keys in file name "config.py"
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        api = tweepy.API(auth)

        return api

#Use thread to deal with the intesive-task for better performance
class TweetWorker():

    def __init__(self, exit_task=False):
        self.exit_task = exit_task
    
    def terminate_check(self):
        return self.exit_task

    #First thread for running search task
    def run_thread(self, task_to_do, thread_name, *task_args):

            #start the timer
            tic = time.perf_counter()

            #create the thread
            thread = Thread(target=task_to_do, args=(*task_args,))

            #start the thread
            thread.start()

            #wait until the thread terminate
            thread.join()

            #stop the timer
            toc = time.perf_counter()

            print("THREAD : %s"%thread_name)

            #display total work time of this thread
            print(f"RUN TIME : {toc - tic:0.4f} seconds")

            #timestamp
            print('TIMESTAMP : [',tweepy_main.PullTwitterData().convert_timezone(tz.gettz('UTC'), tz.gettz(config.local_timezone), datetime.datetime.now()),']')
        
    def terminate_thread(self):
        thread_exit = ''

        try: 
            thread_exit = inputimeout(prompt="Terminate Thread? (Y/n)", timeout=config.task_terminate_timeout)

            if thread_exit.strip() == 'Y':
                self.exit_task = True
            else:
                self.exit_task = False
            return self.exit_task

        except Exception:
            print('Time Over!')

            self.exit_task = False
            
            return self.exit_task        

if __name__ == '__main__':

    #create the schedule
    #schedule for scarp the twitter every 10 minutes
    #you can edit the period and number of scraping tweet in file name "config.py"
    schedule.every(config.task_period).seconds.do(lambda: TweetWorker().run_thread(
        tweepy_main.PullTwitterData().search_twitter,
        'scraping_task',
        ConnectTwitterData.connect_twitter()
        )).tag('scrap_twitter_task')
    
    # # schedule.every(config.task_period).seconds.do(lambda: TweetWorker().terminate_thread).tag('terminate_thread')

    # #start the schedule
    # #ctrl+c in the terminal to stop the task
    while True:

        if TweetWorker().terminate_thread():
            break
        #do the task
        schedule.run_pending()
        # schedule.run_all(delay_seconds=1)

        #delay 1 second 
        #you can edit the delay in file name "config.py"
        time.sleep(config.task_delay)

    exec(open("./twitterDataProcessing.py").read())

    