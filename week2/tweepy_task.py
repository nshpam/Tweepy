import tweepy_main
import config
import tweepy   
import time
from threading import Thread
import schedule
import datetime
from dateutil import tz

class ConnectTwitterData():

    def connect_twitter():

        #input the tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        api = tweepy.API(auth)

        return api

class TweetWorker():

    def run_task(self,task_to_do, task_args):

            #start time
            tic = time.perf_counter()

            #create thread
            # thread = Thread(target=task ,args=(1.5))
            # localstorage = local()
            thread = Thread(target=task_to_do, args=(task_args,))

            #start the thread
            thread.start()
            thread.join()

            #stop time
            toc = time.perf_counter()

            #display total time
            print(f"RUN TIME : {toc - tic:0.4f} seconds")

            #timestamp
            print('TIMESTAMP : [',tweepy_main.PullTwitterData().convert_timezone(tz.gettz('UTC'), tz.gettz(config.local_timezone), datetime.datetime.now()),']')

if __name__ == '__main__':

    schedule.every(config.task_period).seconds.do(lambda: TweetWorker().run_task(
        tweepy_main.PullTwitterData().search_twitter,
        ConnectTwitterData.connect_twitter()
        ))

    #start the schedule
    while True:
        schedule.run_pending()
        time.sleep(config.task_delay)