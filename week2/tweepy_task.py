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

        #start time
        # tic = time.perf_counter()

        #input the tokens
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
        )
        api = tweepy.API(auth)

        #stop time
        # toc = time.perf_counter()

        # print(f"Run connect_twitter in {toc - tic:0.4f} seconds")

        return api

class TweetWorker():

    def run_task(self,task):

        # while True:
            #start time
            tic = time.perf_counter()

            #create thread
            # thread = Thread(target=task ,args=(1.5))

            thread = Thread(target=task)

            #start the thread
            thread.start()

            thread.join()

            #stop time
            toc = time.perf_counter()

            #display total time
            print(f"Run all task (use thread) in {toc - tic:0.4f} seconds")

            #timestamp
            print('[',tweepy_main.PullTwitterData().convert_timezone(tz.gettz('UTC'), tz.gettz(config.local_timezone), datetime.datetime.now()),']')

if __name__ == '__main__':

    schedule.every(config.task_period).seconds.do(lambda: TweetWorker().run_task(tweepy_main.PullTwitterData().search_twiter(ConnectTwitterData.connect_twitter())))

    while True:
        schedule.run_pending()
        time.sleep(config.task_delay)
    