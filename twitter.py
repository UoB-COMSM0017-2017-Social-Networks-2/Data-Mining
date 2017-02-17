#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import time


#Variables that contains the user credentials to access Twitter API 
access_token = "2235939553-2Ns7FAID7XjoEzaUEFZ8K1zoWn62GZaQYmaI3F5"
access_token_secret = "x5qs8Ob8jqba2NcDBt8YTdMIQtekWHqMHGZUiZLQ6CoKc"
consumer_key = "ZLAIRyTdGZ1fdtwjOad2xup3J"
consumer_secret = "CL59B3i6RGNkXUnNu7DBSef8FmwHUWQTnJazJQwMB3ea2BNYVb"

# sample woeid code for countries USA, UK, Brazil, Canada, India
#woeidList = ['23424977','23424975','23424768', '23424775', '23424848']
woeidList = ['23424977']

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = API(auth)
    stream = Stream(auth, l) 

    count = 0
    while True:
        count = count + 1
        #This runs every half an hour
        print ('Trends Collected for {0} hours'.format(count / 2))

        for country in woeidList:
            trends1 = api.trends_place(country)
            data = trends1[0]
            # grab the trends
            trends = data['trends']
            # grab the name from each trend
            names = [trend['name'] for trend in trends[:10]]
            # put all the names together with a ' ' separating them
            # trendsName = ' '.join(names)
            #stream.filter(track=['python', 'javascript', 'ruby'])
            #stream.filter(track=names)
            #new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
            stream.filter(track=names)

        time.sleep(60*30)
        
        
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['python', 'javascript', 'ruby'])
