from twitter import Api

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

tw_api = Api(consumer_key=CONSUMER_KEY,
             consumer_secret=CONSUMER_SECRET,
             access_token_key=ACCESS_TOKEN_KEY,
             access_token_secret=ACCESS_TOKEN_SECRET)
