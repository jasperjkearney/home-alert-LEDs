#!/usr/bin/env python3

import pyowm  # Checking weather
import os
from time import sleep
from datetime import datetime, date, time, timedelta
import requests
import random
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 130, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 60)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def internet_connected():
    url = 'http://google.com/'
    try:
        _ = requests.get(url, timeout=10)
    except:
        return False
    return True

def ping_high():
    url = 'http://google.com/'
    try:
        for _ in range(3):
            __ = requests.get(url, timeout=0.2)
    except:
        return True
    return False

def recycling_needs_taking_out():
    day_of_week = datetime.now().weekday()
    return day_of_week == 3  # Recycling has to be taken out on Thursdays

def bins_need_taking_out():
    # Bins have to be taken out every other Thursday (collected on Fridays)
    known_collection_date = date(2017, 6, 16)
    period_between_collections = timedelta(weeks=2)
    extrapolated_collection_date = known_collection_date
    today = date.today()
    while extrapolated_collection_date < today:
        extrapolated_collection_date += period_between_collections
    return today + timedelta(days=1) == extrapolated_collection_date 

def rain_today(forecast):
    today = datetime.combine(date.today(), time(hour=12, minute=1))
    return forecast.will_be_rainy_at(today)

def rain_tomorrow(forecast):
    tomorrow = pyowm.timeutils.tomorrow()
    return forecast.will_be_rainy_at(tomorrow)

def snow_forecasted(forecast):
    today = datetime.combine(date.today(), time(hour=12, minute=1))
    tomorrow = pyowm.timeutils.tomorrow()
    return forecast.will_be_snowy_at(tomorrow) or forecast.will_be_snowy_at(today)

if __name__ == '__main__':

    strip_length = 6
    strip = Adafruit_WS2801.WS2801Pixels(strip_length, spi=SPI.SpiDev(0, 0))

    LED_index = {'internet': 0,
                 'rain today': 1,
                 'rain tomorrow': 2,
                 'recycling': 3,
                 'bins': 4,
                 'snow': 5}

    if random.random() < 0.01: # sometimes flashes in a random pattern
        from light_patterns import random_pattern
        random_pattern()

    if not internet_connected():
        strip.set_pixel_rgb(LED_index['internet'], *RED)
        strip.show()

    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        API_key = open('{}/API_key.txt'.format(dir_path), 'r').read().strip()
        owm = pyowm.OWM(API_key)
        f = owm.daily_forecast('Bristol,uk')

        ping_state = ping_high()

        strip.clear()
        strip.show()
        sleep(0.2)

        if ping_state:
            strip.set_pixel_rgb(LED_index['internet'], *ORANGE)
        else:
            strip.set_pixel_rgb(LED_index['internet'], *GREEN)


        strip.show()
        sleep(0.2)

        if rain_today(f):
            strip.set_pixel_rgb(LED_index['rain today'], *BLUE)
            strip.show()

        sleep(0.2)

        if rain_tomorrow(f):
            strip.set_pixel_rgb(LED_index['rain tomorrow'], *PURPLE)
            strip.show()

    sleep(0.2)

    if recycling_needs_taking_out():
        strip.set_pixel_rgb(LED_index['recycling'], *GREEN)
        strip.show()

    sleep(0.2)

    if bins_need_taking_out():
        strip.set_pixel_rgb(LED_index['bins'], *ORANGE)
        strip.show()

    sleep(0.2)

    if snow_forecasted(f):
        strip.set_pixel_rgb(LED_index['snow'], *WHITE)
        strip.show()

