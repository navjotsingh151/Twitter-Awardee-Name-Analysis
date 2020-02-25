"""

This program help to scrap twitter data and bring some insights

"""
import twitter # Load the Twitter Library
import tweepy
import pandas as pd


#consumer key, consumer secret, access token, access secret.
ckey="#############"
csecret="##################"
atoken="######################"
asecret="#####################"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
# csvFile = open('ua.csv', 'a')
# #Use csv Writer
# csvWriter = csv.writer(csvFile)
create_date = []
tweets = []
for tweet in tweepy.Cursor(api.search,q="#Oscarwinner",count=100,
                           lang="en",
                           since="2020-02-02").items():
    print (tweet.created_at, tweet.text)

    create_date.append(tweet.created_at)
    tweets.append(tweet.text)
data = pd.DataFrame({ 'Create_Date' : create_date,
                      'Tweets': tweets})
data['date'] = data['Create_Date'].apply( lambda x : str(x).split(" ")[0])
data.drop('Create_Date', axis = 1, inplace=True)
data.drop_duplicates(inplace=True)
data.to_csv("tweet_oscarwinner.csv", index=False)
print("Data Export done")
