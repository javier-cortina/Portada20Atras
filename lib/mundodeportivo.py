import os
import time
from datetime import datetime
import urllib.request
from lib.constants import TIME_BACK, PORTADA_PATH
from lib import twitter
from pdf2image import convert_from_path

def retrieveImage(year: str, month: str, day: str, path: str):
    # URL of front page
    url = 'http://hemeroteca-paginas.mundodeportivo.com/EMD03/PUB/'+ year + '/' + month + '/' + day + '/EMD' + year + month + day + '001MDP.pdf'

    # download front page to specified path
    urllib.request.urlretrieve(url, path + '.pdf')

    # convert from PDF to image
    image = convert_from_path(path + '.pdf', 400)
    image[0].save(path + '.jpg', 'JPEG')

def tweetMundoDeportivo():
    # current date and time
    now = datetime.now()

    # date of front page
    year = str(int(now.strftime("%Y")) - TIME_BACK)
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Path where image will be stored
    image_path = os.path.join(PORTADA_PATH,'mundodeportivo' + year + month + day)

    # Download image
    retrieveImage(year, month, day, image_path)

    # Tweet text
    tweet_text = 'Mundo Deportivo ' + day + '/' + month + '/' + year

    # Tweet
    for attempt in range(300):
        try:
            twitter.sendTweet(tweet_text, image_path + '.jpg')
        except:
            print('Error to tweet Mundo Deportivo, attempt {}'.format(attempt + 1))
            time.sleep(10)
        else:
            break
    
    # Delete image and pdf
    os.remove(image_path + '.pdf')
    os.remove(image_path + '.jpg')

    # Print progress
    print(year + '/' + month + '/'  + day + ' Mundo Deportivo: Completado')
