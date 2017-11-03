'''
@author: Liangji Wang
@Social Media Mining

'''
import json
import pandas as pd

def read_data_file(fileName):
	tweets_data = []
	tweets_file = open(fileName, "r")
	for line in tweets_file:
	    try:
	    	tweet = json.loads(line)
	    	if 'http' not in tweet['text']:
	    		tweets_data.append(tweet)
	    except:
	        continue
	print len(tweets_data)
	return tweets_data


def write_file(data, fileName):
	with open(fileName, 'w') as outfile:
		json.dump(data, outfile)

def main():
	data_without_spam = read_data_file('data.json')
	write_file(data_without_spam, 'data_clean.json')

if __name__ == "__main__":
    main()


