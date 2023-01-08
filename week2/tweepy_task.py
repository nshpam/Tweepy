import concurrent.futures
import tweepy_main
import config
import tweepy   
from tqdm import tqdm
import time
from threading import Thread
import schedule

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
    
    def test(self):
        print('doing task')

    def run_task(self,task):

        # while True:
            #start time
            tic = time.perf_counter()

            #create thread
            # thread = Thread(target=task ,args=(1.5))

            # print('starting task')
            thread = Thread(target=task)

            # thread = Timer(5, Thread(target=task))

            #start the thread
            thread.start()

            thread.join()

            # print('finish task')

            #stop time

            toc = time.perf_counter()
            print(f"Run all task (use thread) in {toc - tic:0.4f} seconds")

        # return thread

        # thread.cancel()
        #wait for the thread to finish
        # thread.join()
        
# def test():
#     print('doing task')

if __name__ == '__main__':

    schedule.every(5).seconds.do(lambda: TweetWorker().run_task(tweepy_main.PullTwitterData().search_twiter(ConnectTwitterData.connect_twitter())))
    # schedule.every(1).minutes.do(TweetWorker().run_task(tweepy_main.PullTwitterData().search_twiter(ConnectTwitterData.connect_twitter())))

    while True:
        schedule.run_pending()
        time.sleep(1)

    # tweepy_main.PullTwitterData().search_twiter(ConnectTwitterData.connect_twitter())

    # timer.start()
    # print('Threading started')  
    # time.sleep(10)#It gets suspended for the given number of seconds  
    # print('Threading finishing')  
    # timer.cancel()

    