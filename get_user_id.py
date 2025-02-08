"""Get user ID and screen name.

Get user ID and screen name from ID or screen name.

Example:
    $ python get-user-id.py --id=2656985876
    $ python get-user-id.py --screen-name=hangstuck
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

    parser = argparse.ArgumentParser(description='Get user ID and screen name.')
    mutal = parser.add_mutually_exclusive_group(required=True)
    mutal.add_argument('--screen-name', help='screen name')
    mutal.add_argument('--id', help='ID')
    args = parser.parse_args()

    user = api.get_user(user_id=args.id, screen_name=args.screen_name)
    print(f"{user.id} : {user.screen_name}")
