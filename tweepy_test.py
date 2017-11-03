'''
@author: Liangji Wang
@Social Media Mining

'''
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# http://pythoncentral.io/introduction-to-tweepy-twitter-for-python/

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key='65t98Koic5nxyqrOyXGEXXwDv'
consumer_secret='dIhnqgcbNYOTxNSMrTQiReM5PU86cQuwZ1rel2DAps9EB1FPpK'


# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token='822174744690774021-kAUf42FmU8wFzaqDLbc6z1YSPNzLqRJ'
access_token_secret='ZKYZC7u7dRz2ErNtlh6ArzRve7AcXZn8QgPyn9UHdXTQH'

# consumer_key='wYmJtaDs2bjWnxiotQotC7StY'
# consumer_secret='BGg4x8m6UCNIUdPbftVai7W03oK29ZUqcj1Ei9fhPmZZR7QzGr'
#
#
# access_token='822174744690774021-fYQsjxhIBqfs4VmijZb41VwRvmMlTJD'
# access_token_secret='VKZCvXcvhRLjGWhsKj4aYnfPLcN6fATZBDoVF8jLgTeR5'

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        try:
            print(data)
            with open('TwitterAPI.csv','a') as f:
                f.write(data)
        except:
            pass


    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['United', 'Asian'])
