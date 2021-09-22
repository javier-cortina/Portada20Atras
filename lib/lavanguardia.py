import os
import time
from datetime import datetime
import urllib.request
from lib.constants import TIME_BACK, PORTADA_PATH
from lib import twitter
from pdf2image import convert_from_path


def retrieveImage(year: str, month: str, day: str, path: str):
    # URL of front page
    url = 'http://hemeroteca-paginas.lavanguardia.com/LVE01/PUB/' + year + '/' + month + '/' + day + '/LVG' + year + month + day + '001LVB.pdf'

    # download front page to specified path
    urllib.request.urlretrieve(url, path + '.pdf')

    # convert from PDF to image
    image = convert_from_path(path + '.pdf', 400)
    image[0].save(path + '.jpg', 'JPEG')

def tweetLaVanguardia():
    # current date and time
    now = datetime.now()

    # date of front page
    year = str(int(now.strftime("%Y")) - TIME_BACK)
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Path where image will be stored
    image_path = os.path.join(PORTADA_PATH,'lavanguardia' + year + month + day)

    # Download image
    for attempt in range(100):
        try:
            retrieveImage(year, month, day, image_path)
        except:
            print('Error to download La Vanguardia, attempt {}'.format(attempt + 1))
            time.sleep(10)
        else:
            break

    # Tweet text
    tweet_text = 'La Vanguardia ' + day + '/' + month + '/' + year

    # Tweet
    for attempt in range(1):
        try:
            twitter.sendTweet(tweet_text, image_path + '.jpg')
            # Print progress
            print(year + '/' + month + '/'  + day + ' La Vanguardia: Completado')
        except:
            print('Error to tweet La Vanguardia, attempt {}'.format(attempt + 1))
            time.sleep(10)
        else:
            break

    # Delete image and pdf
    try:
        os.remove(image_path + '.pdf')
        os.remove(image_path + '.jpg')
    except:
        # Print progress
        print(year + '/' + month + '/'  + day + ' La Vanguardia: Error :(')
    
    
