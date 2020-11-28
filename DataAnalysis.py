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

#importing the dataset
pol_comments = pd.read_csv("chan_final_data.csv")
pol_comments.head(10)

print(pol_comments)