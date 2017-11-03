'''
@author: Liangji Wang
@Social Media Mining

'''
import json
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import datetime
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import numpy as np
import collections
from textblob import TextBlob

def dataClean(fileName):
    tweets_data = []
    tweets_file = open(fileName, "r")
    for line in tweets_file:
        try:
            temp = json.loads(line)
            if 'http' in temp['text']:
                continue
            # dict.pop('key', None)
            tweet = {}
            # tweet['geo'] = temp['geo']
            # tweet['id'] = temp['id']
            # tweet['place'] = temp['place']
            tweet['text'] = temp['text']
            tweet['location'] = temp['location']
            tweet['timestamp_ms'] = temp['timestamp_ms']
            tweet['lang'] = temp['lang']
            tweets_data.append(tweet)
        except:
            continue
    print len(tweets_data)
    return tweets_data

def dataCount(path):
    tweets_file = open(path, "r")
    count = 0
    for line in tweets_file:
        try:
            temp = json.loads(line)
            # dict.pop('key', None)
            if 'location' in temp:
                count += 1
            # elif 'place' in temp:
            #   if temp['place'] != None:
            #       count += 1
            # elif temp['geo'] != None:
            #   print temp['geo']
            #   count += 1
            # elif temp['user']['location'] != None:
            #   count += 1
            # elif temp['user']['geo'] != None:
            #   count += 1
        except:
            continue
    print count

def readData(path):
    tweets_data = []
    tweets_file = open(path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    print len(tweets_data)
    return tweets_data

def compare(path1, path2):
    file1 = open(path1, 'r')
    file2 = open(path2, 'r')
    for line1, line2 in zip(file1, file2):
        if line1 != line2:
            # print line1
            pprint.pprint(json.loads(line2))
            break

def write_file(data, fileName):
    with open(fileName, 'w') as outfile:
        for val in data:
            json.dump(val, outfile)
            outfile.write('\n')

def plotGeo(stateDict):
    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    shp_info = m.readshapefile('./st99_d00','states',drawbounds=True)
    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    cmap = plt.cm.Greens # use 'hot' colormap
    # cmap = plt.cm.coolwarm
    vmin = 0; vmax = 14000 # set range.

    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico']:
            pop = stateDict[statename]
            # calling colormap with value between 0 and 1 returns
            # rgba value.  Invert color range (hot colors are high
            # population), take sqrt root to spread out colors more.
            # colors[statename] = cmap(np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
            colors[statename] = cmap(pop * 1.5/ vmax)[:3]
        statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    ATOLL_CUTOFF = 0.005
    for ind,shapedict in enumerate(m.states_info):
        seg = m.states[int(shapedict['SHAPENUM'] - 1)]
        # skip DC and Puerto Rico.
        if statenames[ind] not in ['Puerto Rico', 'District of Columbia']:
        # Offset Alaska and Hawaii to the lower-left corner. 
            if statenames[ind] == 'Alaska':
            # Alaska is too big. Scale it down to 35% first, then transate it. 
                seg = list(map(lambda (x,y): (0.30*x + 1100000, 0.30*y-1300000), seg))
            if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > ATOLL_CUTOFF:
                seg = list(map(lambda (x,y): (x + 5200000, y-1400000), seg))

            color = rgb2hex(colors[statenames[ind]]) 
            poly = Polygon(seg,facecolor=color,edgecolor='black',linewidth=.5)
            ax.add_patch(poly)
    sm = plt.cm.ScalarMappable(cmap="Greens", norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_ticks([0, 3000, 6000, 9000, 14000])
    cbar.set_ticklabels(['0', '1500', '4000', '6000', '10000 or more'])
    # cbar.set_ticklabels(['0', '200', '500', '1000', '3600'])
    plt.title('Filling State Polygons by Density')
    # plt.savefig('geoDistribution.png')
    plt.show()

def getGeoDict(tweets):
    geoTweets = []
    geoDict = {
    'New Jersey':  438.00,
    'Rhode Island':   387.35,
    'Massachusetts':   312.68,
    'Connecticut':    271.40,
    'Maryland':   209.23,
    'New York':    155.18,
    'Delaware':    154.87,
    'Florida':     114.43,
    'Ohio':  107.05,
    'Pennsylvania':  105.80,
    'Illinois':    86.27,
    'California':  83.85,
    'Hawaii':  72.83,
    'Virginia':    69.03,
    'Michigan':    67.55,
    'Indiana':    65.46,
    'North Carolina':  63.80,
    'Georgia':     54.59,
    'Tennessee':   53.29,
    'New Hampshire':   53.20,
    'South Carolina':  51.45,
    'Louisiana':   39.61,
    'Kentucky':   39.28,
    'Wisconsin':  38.13,
    'Washington':  34.20,
    'Alabama':     33.84,
    'Missouri':    31.36,
    'Texas':   30.75,
    'West Virginia':   29.00,
    'Vermont':     25.41,
    'Minnesota':  23.86,
    'Mississippi':   23.42,
    'Iowa':  20.22,
    'Arkansas':    19.82,
    'Oklahoma':    19.40,
    'Arizona':     17.43,
    'Colorado':    16.01,
    'Maine':  15.95,
    'Oregon':  13.76,
    'Kansas':  12.69,
    'Utah':  10.50,
    'Nebraska':    8.60,
    'Nevada':  7.03,
    'Idaho':   6.04,
    'New Mexico':  5.79,
    'South Dakota':  3.84,
    'North Dakota':  3.59,
    'Montana':     2.39,
    'Wyoming':      1.96,
    'Alaska':     0.42}
    for key in geoDict:
        geoDict[key] = 0
    for tweet in tweets:
        if tweet['location']['country'] == "United States":
            if 'state' in tweet['location']:
                if tweet['location']['state'] in geoDict:
                    geoDict[tweet['location']['state']] += 1
                    geoTweets.append(tweet)
                # else:
                #     print tweet['location']['state']
            # else:
            #     print tweet['location']
    return geoDict, geoTweets


def geoExp(dataPath = 'cleanData.json'):
    tweets = readData(dataPath)
    geoDict, geoTweets = getGeoDict(tweets)
    vmin = 0
    vmax = 0
    for key in geoDict:
        print key, geoDict[key]
        if geoDict[key] > vmax:
            vmax = geoDict[key]
    # print vmax
    print 'geo tweets:', np.sum([geoDict[key] for key in geoDict])
    plotGeoDict(geoDict)
    plotGeo(geoDict)

def plotGeoDict(dataDict):
    od = collections.OrderedDict(sorted(dataDict.items()))
    plt.bar(range(len(od.keys())), od.values(), 0.8, color='g')
    plt.xticks(range(len(od.keys())), od.keys(), rotation='vertical')
    plt.rc('xtick', labelsize=10)
    plt.title('geo distribution')
    # plt.savefig('geoDict.png')
    plt.show()

def getTimeDict(dataPath = 'cleanData.json'):
    tweets = readData(dataPath)
    geoDict, tweets = getGeoDict(tweets)
    dateDict = {}
    hourDict = {}
    for i in range(len(tweets)):
        date = datetime.datetime.fromtimestamp(long(tweets[i]['timestamp_ms']) / 1000).strftime('%m-%d')
        hour = datetime.datetime.fromtimestamp(long(tweets[i]['timestamp_ms']) / 1000).strftime('%m-%d-%H')
        if date in dateDict:
            dateDict[date] += 1
        else:
            dateDict[date] = 1
        if date not in hourDict:
            hourDict[date] = {}
            hourDict[date][hour] = 1
        else:
            if hour not in hourDict[date]:
                hourDict[date][hour] = 1
            else:
                hourDict[date][hour] += 1
    return dateDict, hourDict

def plotTimeDict(dataDict):
    od = collections.OrderedDict(sorted(dataDict.items()))
    plt.bar(range(len(od.keys())), od.values(), 0.5, color='g')
    plt.xticks(range(len(od.keys())), [val[-2:] for val in od.keys()])
    plt.title(od.items()[0][0][:-3])
    # plt.savefig('date_'+od.items()[0][0][:-3]+'.png')
    plt.show()

def timeExp(dataPath = 'cleanData.json'):
    dateDict, hourDict = getTimeDict(dataPath)
    plotTimeDict(dateDict)
    for key in hourDict:
        plotTimeDict(hourDict[key])

def getSentDict(dataPath = 'cleanData.json'):
    tweets = readData(dataPath)
    geoDict, tweets = getGeoDict(tweets)
    sentDict = {
    'positive': 0,
    'negative': 0,
    'neutral': 0
    }
    subjDict = {
    'objective': 0,
    'subjective': 0
    }
    for i in range(len(tweets)):
        testimonial = TextBlob(tweets[i]['text'])
        if testimonial.sentiment.polarity > 0.1:
            sentDict['positive'] += 1
        elif testimonial.sentiment.polarity < -0.1:
            sentDict['negative'] += 1
        else:
            sentDict['neutral'] += 1
        if testimonial.sentiment.subjectivity > 0.5:
            subjDict['subjective'] += 1
        else:
            subjDict['objective'] += 1
    return sentDict, subjDict

def plotSentDict(sentDict, subjDict):
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].bar(range(len(sentDict.keys())), sentDict.values(), 0.5, color='g')
    axarr[0, 0].set_xticks(range(len(sentDict.keys())))
    axarr[0, 0].set_xticklabels(sentDict.keys())
    axarr[0, 0].set_title('polarity')
    axarr[0, 1].pie([sentDict[key] for key in sentDict], labels=[key for key in sentDict], autopct='%1.1f%%')
    axarr[0, 1].axis('equal')
    axarr[1, 0].bar(range(len(subjDict.keys())), subjDict.values(), 0.5, color='b')
    axarr[1, 0].set_xticks(range(len(subjDict.keys())))
    axarr[1, 0].set_xticklabels(subjDict.keys())
    axarr[1, 0].set_title('subjectivity')
    axarr[1, 1].pie([subjDict[key] for key in subjDict], labels=[key for key in subjDict], autopct='%1.1f%%')
    axarr[1, 1].axis('equal')
    plt.suptitle('sentiment analysis')
    # plt.savefig('sentiment.png')
    plt.show()

def sentExp():
    sentDict, subjDict = getSentDict()
    plotSentDict(sentDict, subjDict)

def main():
# get input with pre filtered data (remove tweets with hyperlinks, then use carmen library trying to add location for data)
# build a dictionary with american state and extract those tweets based on this dictionary
# then count the amount for each state and plot the distribution
    # geoExp()
# do the same data filtering as previous step
# based on the geo location dictionary, generate a time dictionary with tweets in America
# count the amount based on each day and hour
# plot the distribution

    # timeExp()
# do the same data filtering as previous step
# based on the geo location dictionary, use texbblob to analysis the text for all the tweets in america
# build the sentiment dictionary based on the polarity and subjectivity through the sentimental analysis
# plot the distribution
    sentExp()
    pass
    
main()





# geoPath = 'geo.json'
# dataPath = 'data_clean.json'
# newPath = 'new.json'

# dataCount(geoPath)

# tweets_data = dataClean(geoPath)
# write_file(tweets_data, newPath)
# tweets_data = readData(newPath)
# print type(tweets_data)


# count =0
# country = {}
# for tweet in tweets_data:
#   if tweet['location']['country'] not in country:
#       country[tweet['location']['country']] = 1
#   else:
#       country[tweet['location']['country']] = country[tweet['location']['country']] + 1
#   if tweet['location']['country'] == "United States":
#       count += 1
# print count
# print len(country)
# for key in country:
#   print key, country[key]

# for i in range(10):
#   pprint.pprint(tweets_data[i])

# print(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H'))

# import datetime
# var = 1458365220000
# temp = datetime.datetime.fromtimestamp(var / 1000).strftime('%H:%M:%S')
# print (temp)
