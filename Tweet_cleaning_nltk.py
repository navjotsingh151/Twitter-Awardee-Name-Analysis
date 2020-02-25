"""
This program helps to extract the awardee name or the film name which/who received Oscar award from the twitter live tweets (#Oscarwinner)

:return the output file with tweets, tags and Person/Film Received the Oscar awards
"""

# Library Imports
import pandas as pd
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import os
import numpy as np
import warnings
from nltk.stem import WordNetLemmatizer
warnings.filterwarnings("ignore")

# First cleaning of tweet removing stop words and url from tweets
def clean_tag_tweet(tweet, pos=1):
    """
    :param tweet: String conatining tweet text
    :param pos: Return variable if 1 then return clean_tweet else psoition tag for the clean tweet
    :return: return string or tuple
    """
    ## Remove url from tweets
    tweet_clean = re.sub(r"http\S+", "", tweet)
    tweet_clean = re.sub(r"^RT\s@\w+:", "", tweet_clean)

    ## Remove Digits and special character
    tweet_clean = [word for word in word_tokenize(tweet_clean) if word.isalpha()]
    tweet_clean = ' '.join(tweet_clean)

    # tags from the tweet
    tag = pos_tag(word_tokenize(tweet_clean))

    ## clean tweet
    tweet_clean = [word for word in word_tokenize(tweet_clean) if word not in stop_words]
    tweet_clean = ' '.join(tweet_clean)

    if pos == 1:
        return tweet_clean
    else:
        return tag

# Setting new column is_congrats as the name of the awardee is in the tweet which contains congrats in it
def congrats(text, lem_syn):
    """
    This is used to return whether the tweet has any synoym for the "Congrats"
    :param text: Tweet string
    :return: 1 if synoym is present , 0 if it is not present
    """
    for i in text.split():
        if i.lower() in lem_syn:
            return 1
    return 0

# analyse the tweets which contains only congrats in it
def imp_tags(tweet):
    """
    This function is used to return the tags Named Noum : NNP and NNS
    :param tweet: String
    :return: return tuple with word and tag
    """

    imp_tag = []
    for word, tags in tweet:
        # print(word, tags )
        if tags in ['NNS', 'NNP'] and word.lower() != 'oscar':
            imp_tag.append((word, tags))
    return imp_tag

# This function clean the text obtained in NNP tag and re-tagged to remove unwanted words from tweets
def nnp_tag(tweet):
    """
    This function return the NNP Tag for the tweet
    :param tweet: String
    :return: NNP tag for the tweet
    """
    # print(tweet)
    nnp_tag = []
    words = ''
    stop_words_nnp = 'win awesome congratulations congratulation best oscar oscarwinner oscars hairlove wins omg god film short boy girl'.split(
        " ")
    for word, tag in tweet:
        if tag == 'NNP' and word.lower() not in stop_words and word.lower() not in stop_words_nnp:
            words = words + " " + word

    words = [word for word in words.split(" ") if word not in stop_words and word != '']

    tags_nnp = pos_tag(words)
    words = ''
    for word, tag in tags_nnp:
        if tag == 'NNP':
            words = words + " " + word
    for i in words.split(" "):
        if i in stop_words_nnp:
            words = np.nan
            break
    if words == "":
        words=np.nan
    return words

# Main function call
if __name__ =='__main__':

    # File import created from twitter crawler
    data = pd.read_csv("tweet_oscarwinner.csv")

    print("Total tweets parsed for finding the awardee name : ", len(data))
    # Stop words declaration
    stop_words = set(stopwords.words('english') + list('#$%^&*()!<>?":{}+=][;/.,@)'))

    ## Finding synoym for congrats
    synonyms = []

    ## List for congrats
    cong_syn = ["blessing", "compliment", "congratulations", "encouragement", "felicitation", "flattery", "praise"]
    lem_syn = []
    lematizer = WordNetLemmatizer()

    for i in cong_syn:
        lem_syn.append(lematizer.lemmatize(i, 'v'))

    ## Unique Congrats list
    lem_syn = list(set(lem_syn))

    data['clean_tweet'] = data['Tweets'].apply(lambda x: clean_tag_tweet(x, 1))
    data['tag'] = data['Tweets'].apply(lambda x: clean_tag_tweet(x, 0))
    data['is_Congrats'] = data['clean_tweet'].apply(lambda x: congrats(x, lem_syn))
    data.drop('Tweets', axis=1, inplace=True)

    data['imp_tag'] = data[data['is_Congrats'] == 1]['tag'].apply(lambda x: imp_tags(x))
    data_clean = data[data['is_Congrats'] == 1]

    data_clean['Person Received Oscar Award'] = data_clean['imp_tag'].apply(lambda x: nnp_tag(x))

    #Removing unwanted columns
    data_clean.dropna(inplace = True)
    data_clean.drop(['tag', 'imp_tag', 'is_Congrats'], axis = 1, inplace = True)

    print("Total records with the Awardee Name - Person/film : ", len(data_clean))
    data_clean.to_csv("clean_tweets.csv", index = False)
    print("*"*100)
    print(f"Cleaned file is present with Awardee Name is present at : {os.getcwd()}\clean_tweets.csv")
