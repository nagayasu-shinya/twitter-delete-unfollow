#!/usr/bin/env python3
"""Delete tweets.

Delete tweets favorites listed in the tweets.js.
The file should contain the favorite ID to be deleted per line.

You can specify maximum number of retweets.
The example below will delete tweets with less than 3000 retweets.

Example:
    $ python delete_tweets.py --retweets=3000

You can specify maximum number of favorites also.
The example below will delete tweets with less than 3000 retweets and less than 1000 favorites.

Example:
    $ python delete_tweets.py --retweets=2000 --favs=1000

If you have tweets you do not want delete,
pass a argument with file of their IDs.

Example:
    $ cat do_not_delete_tweets.txt
    1743159664026783965
    1639522716129853440
    $ python delete_tweets.py --do-not-delete=do_not_delete_tweets.txt
"""
import argparse
import json
import sys
import tweepy
import auth_config

auth = tweepy.OAuth1UserHandler(
    auth_config.CONSUMER_KEY,
    auth_config.CONSUMER_SECRET,
    auth_config.ACCESS_TOKEN,
    auth_config.ACCESS_TOKEN_SECRET
)

if __name__ == "__main__":
    api = tweepy.API(auth)
    user = api.verify_credentials()
    TWEETS_JS='tweets.js'

    parser = argparse.ArgumentParser(description='Delete tweets listed on tweets.js')
    parser.add_argument('--retweets', default=sys.maxsize, type=int,\
                        help='maximum number of retweet')
    parser.add_argument('--favs', default=sys.maxsize, type=int, help='maximum number of favorite')
    parser.add_argument('--dry-run', help='enable dry-run', action='store_true')
    parser.add_argument('--do-not-delete', type=argparse.FileType('r'),
                        help='list file of tweet ID not to delete')
    args = parser.parse_args()

    do_not_delete_tweets = args.do_not_delete.read().splitlines()

    with open(TWEETS_JS, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines[0] = '['
        tweets = json.loads(''.join(lines))
        for tweet_pair in tweets:
            tweet = tweet_pair['tweet']
            id_str         = tweet['id_str']
            full_text      = tweet['full_text']
            favorite_count = tweet['favorite_count']
            retweet_count  = tweet['retweet_count']

            if id_str not in do_not_delete_tweets \
               and (full_text.find('RT @') == 0 \
                    or (int(favorite_count) < args.favs and int(retweet_count) < args.retweets)):
                try:
                    if args.dry_run:
                        print("DRY-RUN : ", end = '')
                    else:
                        api.destroy_status(id=id_str)
                    print(f"Delete tweet {id_str} {full_text}")
                except tweepy.errors.NotFound:
                    print(f"Failed: Not found tweet {id_str}")
                    # Keep going even if it failed.
