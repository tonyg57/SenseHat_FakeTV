#!/usr/bin/python3
# SenseHat_FakeTV3 (with sunset/sunrise timer) -- with lots of help from ChatGPT
# Last update: 07-JUL-2023
# ...and yes, this code is overly convoluted.
#-----------------------------------------------
#vs# used to comment out 'sense' and some
# changes needed for Visual Studio Code
#-----------------------------------------------

from sense_hat import SenseHat
import random
import time
from datetime import datetime, time as time_obj
from astral.sun import sun
from astral import LocationInfo

sense = SenseHat()

# Get the latitude and longitude of your location
latitude = 34
longitude = -118

# Function to calculate sunrise and sunset times
def calculate_sunrise_sunset(latitude, longitude):
    # Create a LocationInfo object with latitude, longitude, and timezone
    location = LocationInfo()
    location.latitude = latitude
    location.longitude = longitude
    location.timezone = 'America/Los_Angeles'

    # Get the current local time
    current_time = datetime.now()

    # Calculate sunrise and sunset times using astral library
    s = sun(location.observer, date=current_time.date(), tzinfo=location.timezone)
    sunrise = time_obj(s['sunrise'].hour, s['sunrise'].minute)
    sunset = time_obj(s['sunset'].hour, s['sunset'].minute)

    return sunrise, sunset

# Define colors for TV noise (did experiment with darker colors)
WHT = (255, 255, 255)
BLK = (64, 64, 64) # dark gray
RED = (255, 0, 0)
GRN = (0, 255, 0)
BLU = (0, 0, 255)
YEL = (255, 255, 0)
ORG = (255, 165, 0)
PUR = (255, 0, 255)

# Define random patterns for the TV noise effect
patterns = [
    [BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT],
    [GRN, ORG, YEL, WHT, BLK, RED, BLU, PUR],
    [PUR, BLU, RED, BLK, WHT, YEL, ORG, GRN],
    [WHT, YEL, ORG, GRN, PUR, BLU, RED, BLK],
    [random.choice([BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT]) for _ in range(8)]
]

# (8) random 'moving scenes' to scroll
scenes = [
    '',\
    '.',\
    '#.',\
    '-_-*',\
    '.. $#$.$',\
    'FakeTVfortheRPi',\
    '...---===#@#==--',\
    '.:.::* @ :.:.:-.#'
]

# Assign effect probabilities - must add up to 1.00
noise_prob = 0.125
scene_prob = 0.25
flash_prob = 0.25
fader_prob = 0.375
probabilities = noise_prob + scene_prob + flash_prob + fader_prob

if probabilities != 1.00:
    print('Probabilities = ', probabilities, ', fix effect probabilities to add up to 1.00')
    exit()

sunrise, sunset = calculate_sunrise_sunset(latitude, longitude)

print('\nProgram running. Display on from sunset to sunrise.')
print('\nnoise:', noise_prob * 100, '%, scene:', scene_prob * 100,\
      '%, flash:', flash_prob * 100, '%, fader:', fader_prob * 100, '%\n')

# TV noise effect
def tv_noise():
    for i in range(8):
        for j in range(8):
            color = random.choice(patterns)[j]
            level = random.randint(16, 255)
            color = tuple(int(c * (level / 255.0)) for c in color)
            sense.set_pixel(j, i, color)

# Moving scene effect
def moving_scene():
    scrolltime = (random.randint(1, 6))/40 # '6' was '8'
    randscene = random.randint(0, 7)
    message = scenes[randscene]
    for char in message:
        if char == ' ':
            # dark for spaces. '128' was '64'
            color = (128, 128, 128)
        else:
            # random color for non-spaces
            color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        sense.set_rotation(random.randint(0, 3) * 90)
        sense.show_message(char, text_colour=color, scroll_speed=scrolltime)

# Screen flash effect
def flash_display():
    num_flashes = random.randint(1, 3)
    brightness = random.choice([True, False])
    sense.low_light = brightness   
    for i in range(num_flashes):
        r = random.randint(16, 255)
        g = random.randint(16, 255)
        b = random.randint(16, 255)
        pixels = [(r, g, b) for i in range(64)]
        sense.set_pixels(pixels)
        time.sleep(random.uniform(0.1, 2))
        #sense.clear() # tends to look 'strobe-ish'

# Fading Kaleidoscope effect
# Kaleidoscope.py -- credit to: https://github.com/midijohnny/sensehat
# fade(pixel) used with function fade_and_random_pixel()
def fade(pixel):
    new_pixel=[]
    for comp in pixel:
        if comp > 0:
            new_pixel.append(comp - 1)
        else:
            new_pixel.append(0)
    return new_pixel

# Referenced in console as 'fader'
def fade_and_random_pixel():
        rx = random.randint(0, 3)
        ry = random.randint(0, 3)
        if random.randint(0, 100) < 25:
            col = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ]
#vs#---------------------------------------------------
            if sense.get_pixel(rx,ry) == [0, 0, 0]:
                sense.set_pixel(rx, ry, col)    
                sense.set_pixel(7-rx, ry, col)
                sense.set_pixel(7-rx, 7-ry, col)
                sense.set_pixel(rx, 7-ry, col)
        pixels = sense.get_pixels()    
        new_pixels = []
        for p in pixels:
            new_pixels.append(fade(p))
        sense.set_pixels(new_pixels)
#vs#---------------------------------------------------

# Main loop
try:
    while True:
        # Calculate the current sunrise and sunset times
        sunrise, sunset = calculate_sunrise_sunset(latitude, longitude)

        now = datetime.now().time()
        if now > sunset or now < sunrise:
            # pick a random effect at the defined statistical probabilities
            TV_Screen = random.random() # (0 - 1)

            if TV_Screen < noise_prob:
                LoopNoise = random.randint(3, 16)        
                print(' ', sunset, 'to', sunrise, '  Function: noise   ', end='\r')
                for _ in range(LoopNoise):
                    tv_noise()
                    time.sleep(random.uniform(0.1, 5))

            elif TV_Screen < noise_prob + scene_prob:
                LoopScene = random.randint(1, 2)        
                print(' ', sunset, 'to', sunrise, '  Function: scene   ', end='\r')
                for _ in range(LoopScene):
                    moving_scene()
                    time.sleep(random.uniform(0.1, 5))

            elif TV_Screen < noise_prob + scene_prob + flash_prob:
                LoopFlash = random.randint(1, 3)
                print(' ', sunset, 'to', sunrise, '  Function: flash   ', end='\r')
                for _ in range(LoopFlash):
                    flash_display()
                    time.sleep(random.uniform(0.1, 5))

            else:
                LoopFader = random.randint(300, 900)
                print(' ', sunset, 'to', sunrise, '  Function: fader   ', end='\r')
                for _ in range(LoopFader):
                    fade_and_random_pixel()
                    #no sleep delay required here except in VS
                    #vs#time.sleep(random.uniform(0.1, 5)) #vs# enable for VS
        else:
            # Wait before checking the time again
            print(' ', sunrise, 'to', sunset, '  Function: sleep   ', end='\r')
            sense.clear() #vs#
            time.sleep(600) # 10 minutes

except KeyboardInterrupt:
    sense.clear() #vs#
    print('\n\nSenseHat_FakeTV terminated\n')
    
