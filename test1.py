#README.md provided in the folder Twitter-Search-and-filter
#All interface and running details are also provided in README.md

def tweetprint(tweets):
    for tweet in tweets:
        print (tweet['id']) # This is the tweet's id
        print (tweet['created_at']) # when the tweet posted
        print (tweet['text']) # content of the tweet
        print (tweet['retweet_count'])
        print (tweet['favorite_count'])
        hashtags = []
        for hashtag in tweet['entities']['hashtags']:
        	hashtags.append(hashtag['text'])
        print (hashtags)

        
def filterr(retweet_count=None,favorite_count=None,follower_count=None,since=None,retweet_opr=None,favorite_opr=None,follower_opr=None,till=None,keyword=None,sort=None,Order=1):
    MONGO_DB="twit"
    MONGO_USER="bharath1"
    MONGO_PASS="bharath1"
    con = MongoClient("ds143778.mlab.com", 43778)
    db = con[MONGO_DB]
    db.authenticate(MONGO_USER, MONGO_PASS)
    if retweet_count:
        rc={'$'+retweet_opr:retweet_count}
    else:
        rc={'$gte':0}
            
    if favorite_count:
        fc={'$'+favorite_opr:favorite_count}
    else:
        fc={'$gte':0}
            
    if follower_count:
        flc={'$'+follower_opr:follower_count}
    else:
        flc={'$gte':0}
            
    if not keyword:
        tex={"$regex":".*.*"}
    else:
        tex={"$regex":".*"+str(keyword)+".*"}
        
    if not since:
        since='2006-07-15'
        
    if not till:
        till=str(datetime.date.today())
    if not sort:
        tweets=db.twitter.find({
        '$and':[
                {'$or':[
                    {"text" : tex},
                    {"user.name":tex},
                    {"user.screen_name":tex}
                    ]
                },
                {"retweet_count":rc},
                {"favorite_count":fc},
                {"user.followers_count":flc},
                {"date":{'$gte':since,'$lte':till}}
                ] 
            
        })
        tweetprint(tweets)
    else:
        tweets=db.twitter.find({
        '$and':[
                {'$or':[
                    {"text" : tex},
                    {"user.name":tex},
                    {"user.screen_name":tex}
                    ]
                },
                {"retweet_count":rc},
                {"favorite_count":fc},
                {"user.followers_count":flc},
                {"date":{'$gte':since,'$lte':till}}
                ]
            
        }).sort(sort,1)
      
    return tweets    

def dsplit(created):
    word=created.split(" ")
    #print (word)
    dic={"Jan":"03","Feb":"02","Mar":"03","Apr":"04","May":"05","June":"06",
    "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    date=word[5]+'-'+dic[word[1]]+'-'+word[2]
    time=word[3]
    return date

def csv(tweets):
    csv_filename = 'tweets.csv'
    csv_file = open(csv_filename, "w")
    for tweet in tweets:
        csv_file.write(str(tweet["id"])+","+str(tweet["user"]["id"])+","+tweet["created_at"])
    csv_file.close()

    
import twitter    
import json
import datetime    
import os
import pymongo
import sys
from pymongo import MongoClient

api = twitter.api.Api(consumer_key="wBl5KBeeYUbi8amzgZUKTVtGv", consumer_secret="W4jWdwvq6RL2CilRvTLZ5pmCcEmYA3Fku2mKtWxQcrxdJKVXLt",access_token_key= "798125121676288000-qxz9fOtBFMwd2Tuqa0XaeNCkVWpOGjP", access_token_secret="qQZ0W3S8KZM2herGUmztAkmCFx6TNEP0gfsOfO5M0r9ol")
q=input("enter your search query\n")
results = api.GetSearch(term=q,lang="en")
#results=api.GetStreamFilter(track=q,languages="en")
tweets_filename = 'twitter.txt'
orig_stdout = sys.stdout
f = open(tweets_filename, "w")
sys.stdout=f
k=1000
	
for kt in results:
	k-=1
	print (json.dumps(kt._json))
	if k==900:
		break
sys.stdout = orig_stdout
f.close()

MONGO_DB="twit"
MONGO_USER="bharath1"
MONGO_PASS="bharath1"
con = MongoClient("ds143778.mlab.com", 43778)
db = con[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)
tweets_filename = 'twitter.txt'
tweets_file = open(tweets_filename, "r")

for line in tweets_file:
    i=1
    try:
        # Read in one line of the file, convert it into a json object 
        tweet = json.loads(line.strip())
        if 'text' in tweet: # only messages contains 'text' field is a tweet
            tweet["date"]=dsplit(tweet['created_at'])
            db.twitter.insert(tweet)
            
    except:
        # read in a line is not in JSON format (sometimes error occured)
        continue

print("data stored successfully")
k=input("press any key to continue")
tweets=filterr(sort="user.screen_name",keyword="India")

tweetprint(tweets)

c=input("do u want results to export to csv?(y/n)")

if c=="y":
    csv(tweets)
    
    

