import os
import time
from datetime import datetime, timedelta
import urllib.request
from lib.constants import TIME_BACK, PORTADA_PATH
from lib import twitter


def retrieveImage(year: str, month: str, day: str, path: str):
    # URL of front page
    url = 'https://srv00.epimg.net/pdf/elpais/snapshot/' + year + '/' + month + '/eps/' + year + month + day + 'Big.jpg'

    # download front page to specified path
    urllib.request.urlretrieve(url, path + '.jpg')


def tweetElPaisSemanal():
    # current date and time
    now = datetime.now()

    # date of front page
    year = str(int(now.strftime("%Y")) - TIME_BACK)
    month = now.strftime("%m")
    day = now.strftime("%d")

    # If it's sunday, continue
    if datetime.weekday(datetime.strptime(year+month+day, '%Y%m%d')) == 6:
        # Path where image will be stored
        image_path = os.path.join(PORTADA_PATH, 'elpaissemanal' + year + month + day)

        # Download image
        retrieveImage(year, month, day, image_path)

        # Tweet text
        tweet_text = 'El Pais Semanal ' + day + '/' + month + '/' + year

        # Tweet
        for attempt in range(300):
            try:
                twitter.sendTweet(tweet_text, image_path + '.jpg')
            except:
                print('Error to tweet El Pais Semanal, attempt {}'.format(attempt + 1))
                time.sleep(10)
            else:
                break

        # Delete image and pdf
        os.remove(image_path + '.jpg')

        # Print progress
        print(year + '/' + month + '/' + day + ' El Pais Semanal: Completado')
