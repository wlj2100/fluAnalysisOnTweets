'''
@author: Liangji Wang
@Social Media Mining

'''
import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = 'fluResult.data'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    break
print tweets_data[0].keys()

print len(tweets_data)

print type(tweets_data)
print type(tweets_data[0])
print json.dumps(tweets_data[0])

for key in tweets_data[0]:
    print key
    print tweets_data[0][key]


tweets = pd.DataFrame()
tweets['text'] = map(lambda x: x.get('text', None), tweets_data)
tweets['lang'] = map(lambda x: x.get('lang', None), tweets_data)
tweets['country'] = map(lambda x: x.get('place').get('country', None) if x.get('place', None) != None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
plt.savefig('top5Lang.png')
plt.show()


tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
plt.savefig('top5Country.png')
plt.show()


def check(x, matchWord):
    if x is None:
        return False
    text = x.lower()
    if (matchWord in text):
        return True
    else:
        return False

tweets['flu'] = tweets['text'].apply(lambda x: check(x, 'flu'))
tweets['cough'] = tweets['text'].apply(lambda x: check(x, 'cough'))
tweets['fever'] = tweets['text'].apply(lambda x: check(x, 'fever'))
print tweets['flu'].value_counts()[True]
print tweets['cough'].value_counts()[True]
print tweets['fever'].value_counts()[True]

prg_langs = ['flu', 'cough', 'fever']
tweets_by_prg_lang = [tweets['flu'].value_counts()[True], tweets['cough'].value_counts()[True], tweets['fever'].value_counts()[True]]

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: flu vs. cough vs. fever (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
plt.savefig('rank.png')
plt.show()
