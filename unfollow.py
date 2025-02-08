#!/usr/bin/env python3
"""Unfollow the IDs listed on file.

Unfollow IDs listed in the file specified by argument.
The file should contain the ID to be unfollowed per line.
44196397
25073877
137857547

Example:
    Unfollow IDs::
        $ python unfollow.py unfollow-id-list.txt

    Dry-run::
        $ python unfollow.py unfollow-id-list.txt --dry-run
"""

import argparse
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
    my_user = api.verify_credentials()

    parser = argparse.ArgumentParser(description='Unfollow IDs listed on file')
    # refs. https://docs.python.org/3.7/library/argparse.html#metavar
    parser.add_argument('unfollow_id_list_txt', metavar='unfollow-id-list.txt',
                        type=argparse.FileType('r'), default="-", help='IDs file.')
    parser.add_argument('--dry-run', help='Enable dry-run', action='store_true')
    args = parser.parse_args()

    users_id = args.unfollow_id_list_txt.read().splitlines()
    for uid in users_id:
        try:
            user = api.get_user(user_id=uid)
            if args.dry_run:
                print("DRY-RUN : ", end = '')
            else:
                api.destroy_friendship(user_id=uid)
            print(f"Unfollow back {uid: <10} : {user.screen_name} : {user.name}")
        except tweepy.errors.NotFound:
            print(f"Failed: Not found folloing ID {uid}")
            # Keep going even if it failed.
