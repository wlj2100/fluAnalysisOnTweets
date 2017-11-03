'''
@author: Liangji Wang
@Social Media Mining

'''
import csv
import matplotlib.pyplot as plt
import numpy as np

def readFiles(files):
	dates = []
	for file in files:
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=';')
			csvfile.readline()
			for row in reader:
				dates.append(row[1])
	return dates

def getYearMonth(dates):
	yearMonth = []
	for date in dates:
		tempTuple = []
		tempDate = date.split(' ')[0].split('-');
		tempTuple.append(tempDate[0])
		tempTuple.append(tempDate[1])
		yearMonth.append(tempTuple)
	return yearMonth

def getDate(dates):
	yearMonth = []
	for date in dates:
		tempTuple = []
		tempDate = date.split(' ')[0].split('-');
		tempTuple.append(tempDate[1])
		tempTuple.append(tempDate[2])
		yearMonth.append(tempTuple)
	return yearMonth

def tweetCount(yearMonth):
	dateCounts = {}
	for date in yearMonth:
		timeStamp = date[0] + '-' + date[1]
		if timeStamp in dateCounts:
			dateCounts[timeStamp] += 1
		else:
			dateCounts[timeStamp] = 1

	return dateCounts

if __name__ == '__main__':
	# files = ['oldTweets_cold.csv']
	# files = ['oldTweets_flu.csv']
	# files = ['flu-2017-4.csv']

	files = ['./output_got.csv']

	dates = readFiles(files)
	print dates[0]
	yearMonth = getDate(dates)
	print len(yearMonth)
	x = []
	y = []
	dateCounts = tweetCount(yearMonth)
	print dateCounts

	for key in sorted(dateCounts.iterkeys()):
		x.append(key)
		y.append(dateCounts[key])


	# x = x[1:]
	# y = y[1:]
	y_pos = np.arange(len(x))

	plt.bar(y_pos, y, align='center', alpha=0.5)
	plt.xticks(y_pos, x)
	plt.ylabel('Count')
	plt.title('Distribution of tweets')

	plt.show()
	# fig = plt.figure()
	# fig.plot(dates, counts)
