# SenseHat_FakeTV -- with help from ChatGPT
# Github: tonyg57 -- Last update: 27-MAR-2023
# Test out at: https://trinket.io/sense-hat
# (above doesn't like end='' or end='\r' in print)
# ...and yes, this is overly complicated.
#----------------------------------------------------
#vs# used to comment out lines for Visual Studio Code
#----------------------------------------------------

from sense_hat import SenseHat
import random
import time

sense = SenseHat()

# Define colors
WHT = (255, 255, 255)
BLK = (64, 64, 64) # dark gray
RED = (255, 0, 0)
GRN = (0, 255, 0)
BLU = (0, 0, 255)
YEL = (255, 255, 0)
ORG = (255 ,165 ,0)
PUR = (128, 0, 128)

# Define random patterns for the TV noise effect
patterns = [
    [BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT],
    [GRN, ORG, YEL, WHT, BLK, RED, BLU, PUR],
    [PUR, BLU, RED, BLK, WHT, YEL, ORG, GRN],
    [WHT, YEL, ORG, GRN, PUR, BLU, RED, BLK],
    [random.choice([BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT]) for _ in range(8)]
]

#print(patterns)
print() # line feed for console to separate from colour sensor warning...

# (8) random 'moving scenes' to scroll
scenes = ['',\
         '.',\
         '#.',\
         '-_-*',\
         '.. $#$.$',\
         'FakeTVfortheRPi',\
         '...== =|==|o|:.|.Xx..',\
         ' ._-=# -==-==. _ = -.@@.@@']

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
    scrolltime = (random.randint(1, 8))/40
    randscene = random.randint(0, 7)
    #print(' - Scene:', randscene, ', Scroll time: ',scrolltime)
    message = scenes[randscene]
    for char in message:
        if char == ' ':
            # dark for spaces
            color = (64, 64, 64)
        else:
            # random color for non-spaces
            color = (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255))
        #print('Character:', char, ', Color:', color)
        sense.set_rotation(random.randint(0, 3) * 90)
        sense.show_message(char, text_colour=color, scroll_speed=scrolltime)

# Screen flash effect
def flash_display():
    num_flashes = random.randint(1, 3)
    #print('Flashes:', num_flashes)
    for i in range(num_flashes):
      r = random.randint(128, 255)
      g = random.randint(128, 255)
      b = random.randint(128, 255)
      pixels = [(r, g, b) for i in range(64)]
      sense.set_pixels(pixels)
      time.sleep(random.uniform(0.1, 2))
      sense.clear()

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

# Main loop
while True:
    TV = random.randint(1, 4) # pick an effect at random

    if TV == 1:
      LoopNoise = random.randint(3, 9)        
      print('  Function: noise', end='\r')
      for _ in range(LoopNoise):
        tv_noise()
        time.sleep(random.uniform(0.1, 5))
    
    elif TV == 2:
      LoopScene = random.randint(1, 2)        
      print('  Function: scene', end='\r')
      for _ in range(LoopScene):
        moving_scene()
        time.sleep(random.uniform(0.1, 5))

    elif TV == 3:
      LoopFlash = random.randint(1, 3)
      print('  Function: flash', end='\r')       
      for _ in range(LoopFlash):
        flash_display()
        time.sleep(random.uniform(0.1, 5))
          
    elif TV == 4:
      LoopFader = random.randint(200, 800)
      print('  Function: fader', end='\r')      
      for _ in range(LoopFader):
        fade_and_random_pixel()
        #no sleep delay required here
