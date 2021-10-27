import os
import time
from datetime import datetime
import urllib.request
from lib.constants import TIME_BACK, PORTADA_PATH
from lib import twitter


def retrieveImage(year: str, month: str, day: str, path: str):
    # URL of front page
    url = 'http://img.timeinc.net/time/magazine/archive/covers/' + year + '/1101' + year[-2:] + month + day + '_400.jpg'

    # download front page to specified path
    urllib.request.urlretrieve(url, path + '.jpg')

def tweetTimeMagazine():
    # current date and time
    now = datetime.now()

    # date of front page
    year = str(int(now.strftime("%Y")) - TIME_BACK)
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Path where image will be stored
    image_path = os.path.join(PORTADA_PATH,'timeMagazine' + year + month + day)

    # Download image
    retrieveImage(year, month, day, image_path)

    # Tweet text
    tweet_text = 'Time ' + day + '/' + month + '/' + year

    # Tweet
    for attempt in range(300):
        try:
            twitter.sendTweet(tweet_text, image_path + '.jpg')
        except:
            print('Error to tweet El Pais, attempt {}'.format(attempt + 1))
            time.sleep(10)
        else:
            break

    # Delete image and pdf
    os.remove(image_path + '.jpg')
    
    # Print progress
    print(year + '/' + month + '/'  + day + ' Time: Completado')
