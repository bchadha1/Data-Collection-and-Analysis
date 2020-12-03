import requests
import json
import pymongo
from pymongo import MongoClient

MONGO_HOST = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = MONGO_HOST.sw


# connection class
def connection_to_twitt(url, headers):
    url_response = requests.get(url, headers=headers, stream=True)
    if url_response.status_code == 200:
        for every_response in url_response.iter_lines():
            if every_response:
                response_loaded = json.loads(every_response)
                dic = {}
                dic['text'] = response_loaded['data']['text']
                dic['author_id'] = response_loaded['data']['author_id']
                dic['created_at'] = response_loaded['data']['created_at']
                # dic['attachments'] = response_loaded['data']['attachemnts']
                # dic['entities'] = response_loaded['data']['entities']
                # dic['geo'] = response_loaded['data']['geo']
                # dic['in_reply_to_user_id'] = response_loaded['data']['in_reply_to_user_id']
                dic['lang'] = response_loaded['data']['lang']
                dic['possibly_sensitive'] = response_loaded['data']['possibly_sensitive']
                dic['public_metrics'] = response_loaded['data']['public_metrics']
                # dic['referenced_tweets'] = response_loaded['data']['referenced_tweets']

                # calling into mongodb
                db.twitts.insert_one(dic)
                # print(json.dumps(response_loaded, indent = 4, sort_keys = True))
                print('loading into databases')
    # for url not found exception
    elif (url_response.status_code == 404):
        raise Exception("Requested url not found error. The ERROR 404")

    # for all other exceptions 
    else:
        print('excecption occured')


# twitter api creditintials 
# logging into the twitter api using twitter account bearer_token 
twitter_bearer_token = "AAAAAAAAAAAAAAAAAAAAAO2HJAEAAAAA0rFFB1GJyzQKRx%2Bj%2BWCjg%2Bfdfjc%3Di8W4jMhJgHI0EmsbB8F32rtMIctbggR1DTxF9pB8OoHtmTJK4S"


def main():
    bearer_token = twitter_bearer_token
    # Authorization of headers using bearer_token
    headers = {f'Authorization': f'Bearer {bearer_token}'}

    # the url with along whatever tweet fields required
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=attachments,author_id,context_annotations," \
          "created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets," \
          "source,text,withheld&expansions=referenced_tweets.id "
    timerem = 0
    
    while connection_to_twitt(url, headers):
        timerem = timerem + 1


# intrepeting or calling  main class
if __name__ == "__main__":
    main()
