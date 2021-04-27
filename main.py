#!/usr/bin/python
import os
import sys
import schedule
import time
from lib.constants import postElPais, postABC, postLaVanguardia, postMundoDeportivo
from lib import elpais, abc, lavanguardia, mundodeportivo

def closeApp():
    print('Job done for today! :D')
    sys.exit()

def main():
    # Newspapers
    schedule.every().day.at(postElPais).do(elpais.tweetElPais)
    schedule.every().day.at(postABC).do(abc.tweetABC)
    schedule.every().day.at(postLaVanguardia).do(lavanguardia.tweetLaVanguardia)
    schedule.every().day.at(postMundoDeportivo).do(mundodeportivo.tweetMundoDeportivo)

    # Define time to finalize script
    ep = postElPais.split(':')
    ab = postABC.split(':')
    lv = postLaVanguardia.split(':')
    md = postMundoDeportivo.split(':')
    tmax = max(float(ep[0]) + float(ep[1])/60, float(ab[0]) + float(ab[1])/60, float(lv[0]) + float(lv[1])/60, float(md[0]) + float(md[1])/60)
    hmax = int(tmax)
    mmax = int((tmax - hmax)*60) + 5
    schedule.every().day.at(str(hmax).zfill(2) + ':' + str(mmax).zfill(2)).do(closeApp)

    # Tweet at specific time
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()