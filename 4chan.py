# importing packages
import re
from bs4 import BeautifulSoup
from datetime import datetime as dt
import urllib
import requests
from mongoengine import *

# connecting to mongodb with the help of mongoengine library
uri = "mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
connect(
    db='trial',  # this the name of our database for storing the 4chan data
    # The db is already present in the mongodb community server edition(mongodb compass),if not it will create one
    host=uri
)


# now entering into collection class of the db which is threads class
class Threads(DynamicDocument):

    # time stamp
    def t_func(self, DateTimeField):
        self.time_stamp = DateTimeField
        return self.time_stamp

    time_stamp = DateTimeField(default=dt.utcnow)

    # post number in 4chan data
    no = StringField(min_length=2, required=False)
    # creators comment for each particular thread
    com = StringField(min_length=1, required=False)
    # Title of thread creator
    semantic_url = StringField(min_length=None, required=False, primary_key=True)

    # count no of comments
    def commcount(self):
        pass

    meta = {
        'indexes': [{
            'fields': ['$no', '$ids'],
            'default_language': 'none',
        }],
        "ordering": "no",
        'collection': 'threads',
    }


# utility class for parsing the 4chan page and doing filtering 
class utillabstract(object):

    # method(function) for substituting text with the help of regular expressions methods(re.sub)
    def text_pattern_replacement(self, pattern, to_replace, text):
        # takes pattern, and what to replace and text(which is to be replaced) as arguments to sub method
        text = re.sub(pattern, to_replace, text)
        substitued_text = str(text)
        return substitued_text

    # parsing the html content and stripping the special characters in it if exists
    # calling the re expression replace function 
    def parse_remove(self, cd):
        # taking the content of html 4chan page into beautifulsoup object using lxml
        soup_object = BeautifulSoup(str(cd), 'lxml')
        cd = self.text_pattern_replacement(r'>|>>|>>>|>>>>|>>>>>|>>>>>>|>>>>>>>|\d[0-9]', '', soup_object.get_text())
        return cd


# calling the 4chandata

class getting_chan_data(utillabstract):
    _page = {}
    page_number = None

    def catalog_page_generator(self, x):
        for page_num in x[self.page_number]['threads']:
            yield page_num

    def catalog_generator(self, x):
        for idx, page in enumerate(x):
            for thread in x[idx]['threads']:
                yield thread

    # getting the json format of catalog page of pol data from 4chan
    def get_catalog_page(self, board='pol', page_num=7):
        r = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
        self.page_number = page_num

        for threads in self.catalog_page_generator(r):
            self._page['no'] = str(threads.get('no'))
            self._page['com'] = threads.get('com')
            self._page['semantic_url'] = threads.get('semantic_url')

            thread_pages = Threads(
                postnum=self._page['no'],
                com=self._page['com'],
                semantic_url=self._page['semantic_url']
            ).save()

        print('Updated')

        return self._page


# calling the 4chandata called class

c = getting_chan_data()
# invoking the method
c.get_catalog_page('pol', 7)
