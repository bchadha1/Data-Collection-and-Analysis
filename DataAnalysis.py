import inline as inline
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from textblob import TextBlob
import re, string, unicodedata
import nltk
# import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import seaborn as sns

# importing the dataset
pol_comments = pd.read_csv("4chan_final_data.csv")
pol_comments.head(10)
# seeing the available columns in the dataset
pol_comments.columns
# checking the shape of dataset
pol_comments.shape
# assigning the dataset to dataframe
df = pd.DataFrame(pol_comments)
df.shape
# converting the comments into text
df['com'] = df['com'].astype(str)
# checking for one row
df['com'][2]
# to lowercase everything
df['com'] = df['com'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['com']
# removing the punctuation
df['com'] = df['com'].str.replace('[^\w\s]', '')
df['com']


def senti(x):
    return TextBlob(x).sentiment


df['senti_score'] = df['com'].apply(senti)
mw = df['senti_score']
mw

sns.distplot([mw])
[mw].mean()