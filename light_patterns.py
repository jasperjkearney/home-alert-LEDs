#!/usr/bin/env python3

from time import sleep
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

RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

strip_length = 6
strip = Adafruit_WS2801.WS2801Pixels(strip_length, spi=SPI.SpiDev(0, 0))

def random_flashes():
    for _ in range(150):
        for i in range(strip_length):
            if random.choice([True, False]):
                c = random.choice(RAINBOW + [WHITE])
                strip.set_pixel_rgb(i, *c) 
                strip.show()

        sleep(0.1)
        strip.set_pixels_rgb(*BLACK) 
        strip.show()

def scan():
    colour = random.choice(RAINBOW + [WHITE])
    strip.set_pixel_rgb(0, *colour)
    INTERVAL = 0.1
    sleep(INTERVAL)
    for _ in range(20):
        for i in range(strip_length-1):
            strip.set_pixel_rgb(i, *BLACK)
            strip.set_pixel_rgb(i+1, *colour)
            strip.show()
            sleep(INTERVAL)
        for i in range(strip_length-2, -1, -1):
            strip.set_pixel_rgb(i+1, *BLACK)
            strip.set_pixel_rgb(i, *colour)
            strip.show()
            sleep(INTERVAL)
    strip.set_pixels_rgb(*BLACK)
    strip.show()

def breathe():
    colour = random.choice(RAINBOW + [WHITE])
    INTERVAL = 0.02
    for _ in range(5):
        for b in range(101):
            strip.set_pixels_rgb(*[int((b/100)*i) for i in colour])
            strip.show()
            sleep(INTERVAL)
        for b in range(100, -1, -1):
            strip.set_pixels_rgb(*[int((b/100)*i) for i in colour])
            strip.show()
            sleep(INTERVAL)

def rainbow_fade():
    for _ in range(5):
        for i in range(3):
            for v in range(255):
                colour = [0, 0, 0]
                colour[i] = v
                colour[(i-1)%3] = 255-v
                strip.set_pixels_rgb(*colour)
                strip.show()
                sleep(0.002)
    strip.set_pixels_rgb(*BLACK)
    strip.show()

def rainbow_wipe():
    for _ in range(2):
        for colour in RAINBOW:
            for o in range(6):
                for i in range(strip_length):
                    strip.set_pixel_rgb(i, *RAINBOW[(i+o)%6])
                    strip.show()
                    sleep(0.05)
    strip.set_pixels_rgb(*BLACK)
    strip.show()

def rainbow_strobe():
    for _ in range(20):
        for colour in RAINBOW:
            strip.set_pixels_rgb(*colour)
            strip.show()
            sleep(0.15)
            strip.set_pixels_rgb(*BLACK)
            strip.show()
            sleep(0.05)

def rgb_strobe():
    for _ in range(60):
        for colour in [RED, GREEN, BLUE]:
            strip.set_pixels_rgb(*colour)
            strip.show()
            sleep(0.05)
            strip.set_pixels_rgb(*BLACK)
            strip.show()
            sleep(0.05)


def strobe():
    colour = random.choice(RAINBOW + [WHITE])
    for _ in range(200):
        strip.set_pixels_rgb(*colour)
        strip.show()
        sleep(0.02)
        strip.set_pixels_rgb(*BLACK)
        strip.show()
        sleep(0.04)

def switchy():
    c1 = random.choice(RAINBOW + [WHITE])
    c2 = random.choice(RAINBOW + [WHITE])
    while c2 == c1:
        c2 = random.choice(RAINBOW + [WHITE])

    for _ in range(40):
        for i in range(0, strip_length, 2):
            strip.set_pixel_rgb(i, *c1)
            strip.set_pixel_rgb(i+1, *c2)

        strip.show()
        sleep(0.2)

        for i in range(0, strip_length, 2):
            strip.set_pixel_rgb(i, *c2)
            strip.set_pixel_rgb(i+1, *c1)

        strip.show()
        sleep(0.2)

    strip.set_pixels_rgb(*BLACK)
    strip.show()

def worm():
    colour = random.choice(RAINBOW + [WHITE])
    for _ in range(15):
        for i in range(strip_length):
            for j in range(strip_length):
                strip.set_pixel_rgb((i-j)%strip_length, *[int((1-(j/(strip_length-1)))*p) for p in colour])
            strip.show()
            sleep(0.15)
            strip.set_pixels_rgb(*BLACK)
            strip.show()

def overdrive():
    colour = random.choice(RAINBOW + [WHITE])
    steps = 50
    for step in range(steps):
        for i in range(strip_length):
            strip.set_pixels_rgb(*BLACK)
            strip.set_pixel_rgb(i, *colour)
            strip.show()
            sleep(0.4**(0.25*step))

    strip.set_pixels_rgb(*BLACK)
    strip.show()

def random_pattern():
    patterns = [random_flashes, scan, rainbow_fade, breathe, rainbow_wipe, rainbow_strobe, rgb_strobe, strobe,
                switchy, worm, overdrive]
    choice = random.choice(patterns)
    choice()

