from socketIO_client import SocketIO, LoggingNamespace
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob
import os
import json



#consumer key, consumer secret, access token, access secret.
ckey=os.environ.get('ckey')
csecret=os.environ.get('csecret')
atoken=os.environ.get('atoken')
asecret=os.environ.get('asecret')
score=0
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)



class listener(StreamListener):

	def __init__(self, cb):
		self.cb=cb

	def on_error(self, status):
		print(status)

	def on_data(self,data):
		all_data = json.loads(data)
		tweet = all_data["text"]
		username = all_data['user']['screen_name']
		analysis = TextBlob(tweet)
		#print(analysis.sentiment.polarity)
		return self.cb(analysis,tweet)


class Namespace(LoggingNamespace):
    _connected = True

    def on_connect(self):
        print('connected')

    def on_error(self, data):
        print('error')



socketIO = SocketIO(os.environ.get('socket_server'),os.environ.get('socker_port'), Namespace)
nsp = socketIO.define(Namespace, '/chat')
    #socketIO.wait(seconds=1)
    #socketIO.wait(seconds=1)
print("invoking ..1")

def cb2(alysys,tweet):
    global score
    #print(float(alysys.sentiment.polarity))
    score+= float(alysys.sentiment.polarity)
    nsp.emit('chat',{'score':score,'tweet':tweet},namespace='/chat')

twitterStream = Stream(auth, listener(cb2))
twitterStream.filter(track=["noteban","demonetisation"],async=True)

print("invoking ..2")

    





