# Delete all tweets, favorites and unfollow back

Delete your tweets, favorites and unfollow.

* Delete all your favorites
* Delete all your tweets
 * You can specify minimum retweets and favs count to be deleted tweets  
 * You can specify which tweets you do not want to delete
* Unfollow account that do not follow you
　* You can specify accounts you do not want to unfollow
* Dry-run mode

## Disclaimer

I often use the scripts myself, but I make no warranty of any kind.

## Reauirement

* Python3
* Twitter developer acount
  * only Twitter API v1.1 supported, v2 is not suppported  
* Twitter archive data

## Preparetion

### Get keys for Twitter API v1.1

Get consumer key pair, access token pair.
Refer official site.

https://developer.x.com/docs/authentication/oauth-1-0a

### Download Twitter archive data

Access https://x.com/settings/download_your_data and log in.

Click **Requcst archive**.

![twitter-download-archive](https://github.com/user-attachments/assets/581a1e38-0a87-4609-880e-6a2742ff99b7)

You’ll receive an email or nortification of app a few days later when your archive is ready.
Download your archive by desctop browser.

If you need more detail, refer official site:
https://help.x.com/en/managing-your-account/accessing-your-x-data

## Get twitter data files

Unzip your archive file and you find some json files in data directory.
This script need `tweets.js`, `like.js`, `follows.js`, `following.js` in them.

## How to use

### Environment

Clone scripts and activate venv as below. 

```shell
$ git clone https://github.com/nagayasu-shinya/anti-akabare.git
$ cd anti-akabare
$ python3 -m venv .
$ source bin/activate
$ pip3 install -r requirements.txt
```
And set your develop keys at `auth_config.py`.

```python
CONSUMER_KEY    = "Please set your key"
CONSUMER_SECRET = "Please set your key"
ACCESS_TOKEN        = "Please set your key"
ACCESS_TOKEN_SECRET = "Please set your key"
#USER_ID = "Dont use"
```

### Unfollow back

Unfollow accounts that are not followers. This script requires following.js and follower.js of Twitter archive data.
And you should set ID you do not want unfollow, example for some official accounts at `do_not_unfollow.txt`.

Confirm with **dry-run** before actually executing the unfollowing.

example:

```shell
$ file following.js follower.js 
following.js: ASCII text
follower.js:  ASCII text
$ cat do_not_unfollow.txt
14306062
2656985876
$ bash ./unfollow_back.sh --dry-run
DRY-RUN : Unfollow back 96785342   : tamakiyuichiro : 
DRY-RUN : Unfollow back 765096391  : stdaux : 
$ bash ./unfollow_back.sh
Unfollow back 96785342   : tamakiyuichiro : 
Unfollow back 765096391  : stdaux : 
```

### Delete favorites

Delete all favorites. This script requires `like.js` of Twitter archive data. 
Confirm with **dry-run** before actually executing the deletion.

```shell
$ file like.js 
like.js: Unicode text, UTF-8 text
$ bash ./delete_favorites.sh --dry-run
DRY-RUN : Delete favorite 1314025986711642112
DRY-RUN : Delete favorite 1314004965879291905
DRY-RUN : Delete favorite 1314017709823205382
$ bash ./delete_favorites.sh --dry-run
Delete favorite 1314025986711642112
Delete favorite 1314004965879291905
Delete favorite 1314017709823205382
```

### Delete tweets

Delete all tweets. The script requires `tweets.js` of Twitter archive data.
And you should set to `do_not_delete_tweets.txt` tweet ID you do not want delete.
Also, The minimum number of retweets and minimum number of favourites of a tweet to be deleted can also be specified as arguments.
In the example below, tweets with less than 1000 retweets and less than 2000 favourites, as well as tweets not listed in `do_not_delete_tweets`, are deleted.
Confirm with **dry-run** before actually executing the deletion.

```shell
$ file tweets.js 
tweets.js: HTML document, Unicode text, UTF-8 text
$ cat do_not_delete_tweets.txt
1743159664026783965
1639522716129853440
$ bash ./delete_tweets.sh --favs=2000 --retweets=1000 --dry-run
DRY-RUN : Delete tweet 1851357206266200371
DRY-RUN : Delete tweet 1839951673873313988
$ bash ./delete_favorites.sh --favs=2000 --retweets=1000 
Delete tweet 1851357206266200371
Delete tweet 1839951673873313988
```



