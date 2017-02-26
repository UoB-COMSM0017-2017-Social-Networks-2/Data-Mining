#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from html.parser import HTMLParser
import json
import subprocess
import time


#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# sample woeid code for countries USA, UK, Brazil, Canada, India
#woeidList = ['23424977','23424975','23424768', '23424775', '23424848']
woeidList = ['23424975'] #Used to fetch trending topics
# sample location bounding box coordinates of london
location = [-0.351468,51.38494,0.148271,51.672343] #Used to fetch all tweets for this location
TrendingTopics = []

count = 0
startTime = time.time()
timeLimit = 5 # five second limit

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    #On every tweet arrival
    def on_data(self, data):
        if ((time.time() - startTime) < timeLimit):
            #Convert the string data to pyhton json object.
            data = json.loads(HTMLParser().unescape(data))
            #Gives the content of the tweet.
            tweet = data['text']
            #If tweet content contains any of the trending topic.
            for topic in TrendingTopics:
                if topic in tweet: 
                    #Add trending topic and original bounding box as attribute
                    data['TrendingTopic'] = topic
                    data['QueriedBoundingBox'] = location[0]
                    #Convert the json object again to string 
                    dataObj = json.dumps(data)
                    #Appending the data in tweetlondon.json file
                    with open('tweetlondon.json','a') as tf:
                       tf.write(dataObj)
                    #prints on console
                    print (dataObj)        
            return True
        else:
            return False

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = API(auth)
    stream = Stream(auth, l) 
    # send data to s3 every 5th hour
    if (count%5 == 0):
        # This runs the system command of transfering file to s3 bucket
        proc = subprocess.Popen(["aws", "s3", "cp","tweetlondon.json", "s3://sentiment-bristol"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print ("program output:", out)
    while True:
        count = count + 1
        #This runs every an hour
        print ('Tweets Collected for {0} hours'.format(count))
        print(count)
        
        # for country in location:
        for country in woeidList:
            trends1 = api.trends_place(country)
            data = trends1[0]
            # grab the trends
            trends = data['trends']
            # grab the name from each trend
            TrendingTopics = [trend['name'] for trend in trends[:10]]
            # put all the names together with a ' ' separating them
            #trendsName = ' '.join(names)
            print(TrendingTopics)
            #Stream the tweets for given location coordinates
            stream.filter(locations= [location[0],location[1],location[2],location[3]])

        time.sleep(timeLimit)
        
