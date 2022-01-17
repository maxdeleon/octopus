from os import linesep
import feedparser
from datetime import datetime
from time import mktime
import requests
import sys



# reads a text file and returns an array
def parseFile(filename:str):
    f = open(filename, "r")
    lines = []
    for line in f:
        line = line.rstrip()
        line = line.split(',')
        lines.append(line)
    return lines

def getRSS(RSS_FILE:str,verbose=True):
    publications = []
    file_data = parseFile(filename=RSS_FILE) # parse file data into array
    for i in range(len(file_data)): # iterate through array
        current_news_feed = feedparser.parse(file_data[i][1]) # get rss feed url
        for entry in current_news_feed.entries[::-1]: # iterate through all the entries in the rss feed
            publication = [datetime.fromtimestamp(mktime(entry.updated_parsed)),
                            entry.link,
                            entry.title,
                            file_data[i][1]]
            publications.append(publication)
            # print out news stuff for each entry in each rss feed
            if verbose:
                print('Date: {}'.format(publication[0])) 
                print("Link: {}".format(publication[1]))
                print('-----------')
                print('Source:{}\nTitle: {}'.format(file_data[i][4],publication[2]))
                print('Summary: \n{}'.format(publication[3]))
                print('===========')
    return publications # return data

def sortList(sub_li,index):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[index])
    return sub_li

# fetches the news feeds
def fetch():
    DEBUG = False
    publication_data = getRSS(RSS_FILE='./rssFeeds/rssFeedURLS.txt',verbose=DEBUG)
    publication_data = sortList(publication_data,0)
    today = datetime.today()
    # dd/mm/YY
    current_date = today.strftime("%Y-%m-%d")

    f = open('./rssFeeds/todaysArticles.txt','r+')
    file_data = f.readlines()
    file_data = [line.strip('\n') for line in file_data]

    if len(file_data) == 0:
        f.write(current_date+'\n')
        f.close()
    else:
        if current_date not in file_data:
            f.truncate()
            f.write(str(current_date)+'\n')
            f.close()
        else:
            f.close()

    
    f = open('./rssFeeds/todaysArticles.txt','r+')
    file_data = f.readlines()
    file_data = [url.strip('\n') for url in file_data]
    print_data = []
    for i in range(len(publication_data)):
        url = publication_data[i][1]
        publication_date = publication_data[i][0].strftime("%Y-%m-%d")
        if url not in file_data and publication_date == current_date:
            current_data = 'Date: {}\nTitle: {}\nURL: {}\n'.format(publication_data[i][0],publication_data[i][2],publication_data[i][1])
            print_data.append(current_data)
            f.write(url+'\n')
        else: pass
    return print_data
if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)

    print('type=FILE')
    print('')