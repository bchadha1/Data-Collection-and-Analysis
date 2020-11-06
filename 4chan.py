import re
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import date
import urllib
import requests
from mongoengine import *

uri = "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"
connect(
    db='A5',
    host=uri,
)

class Threads(DynamicDocument):

    def commcount(self):
        pass

    # time stamp
    def t_func(self, DateTimeField):
        self.time_stamp = DateTimeField
        return self.time_stamp

    time_stamp = DateTimeField(default=dt.utcnow)

    # post number of 4chan
    no = StringField(min_length=2, required=False)
    # creators comment for each particular thread
    com = StringField(min_length=1, required=False)
    # Title of thread creator
    semantic_url = StringField(min_length=None, required=False, primary_key=True)

    meta = {
        'indexes': [{
            'fields': ['$no', '$ids'],
            'default_language': 'none',
        }],
        "ordering": "no",
        'collection': 'threads',
    }


class BaseMetaAbstract(object):

    def _substitute_text_pattern(self, pat, replacement, text):
        text = re.sub(pat, replacement, text)
        return str(text)

    def _parse_html_and_strip_special_chars(self, df):
        soup = BeautifulSoup(str(df), 'lxml')
        df = self._substitute_text_pattern(r'>|>>|>>>|>>>>|\d{9}', '', soup.get_text())
        return df


class GetChan(BaseMetaAbstract):
    _page = {}
    _page_num = 0

    def _catalog_page_generator(self, x):
        for page_num in x[self._page_num]['threads']:
            yield page_num

    def _catalog_generator(self, x):
        for idx, page in enumerate(x):
            for thread in x[idx]['threads']:
                yield thread

    def get_catalog_page(self, board='pol', page_num=9):
        r = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
        self._page_num = page_num

        for threads in self._catalog_page_generator(r):
            self._page['no'] = str(threads.get('no'))
            self._page['com'] = threads.get('com')
            # self._page['user_id'] = threads.get('user_id')
            self._page['semantic_url'] = threads.get('semantic_url')

            thread_pages = Threads(
                postnum=self._page['no'],
                com=self._page['com'],
                # ids=self._page['user_id'],
                semantic_url=self._page['semantic_url']
            ).save()

        print('Complete..Updating...')
        print('Update Complete...')
        return self._page


c = GetChan()
c.get_catalog_page('pol', 9)
