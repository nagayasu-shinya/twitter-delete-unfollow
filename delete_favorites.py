#!/usr/bin/env python3
"""Delete favorites.

Delete favorites listed in the file specified by argument.
The file should contain the favorite ID to be deleted per line.

Example:
    $ python delete_favorites.py favorite_id_list
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

    parser = argparse.ArgumentParser(description='Delete favorite listed on file')
    parser.add_argument('favorite_id_list', type=argparse.FileType('r'),
                        default="-", help='favorite list file.')
    parser.add_argument('--dry-run', help='enable dry-run', action='store_true')
    args = parser.parse_args()

    fav_id = args.favorite_id_list.read().splitlines()
    for fid in fav_id:
        try:
            if args.dry_run:
                print("DRY-RUN : ", end = '')
            else:
                api.destroy_favorite(id=fid)
            print(f"Delete favorite {fid}")
        except tweepy.errors.NotFound:
            print(f"Failed: Not found favorite {fid}")
            # Keep going even if it failed.
