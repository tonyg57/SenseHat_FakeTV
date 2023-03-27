# SenseHat_FakeTV -- with help from ChatGPT
# Github: tonyg57 -- Last update: 26-MAR-2023
# Test out at: https://trinket.io/sense-hat
# (above doesn't like end='' type statements)
#---------------------------------------------
## used to comment out for Visual Studio Code
#---------------------------------------------
#
from sense_hat import SenseHat
import random
import time

sense = SenseHat()

# Define colors - black is actually a dark gray
WHT = (255, 255, 255); BLK = (64, 64, 64)
RED = (255, 0, 0); GRN = (0, 255, 0); BLU = (0, 0, 255)
YEL = (255, 255, 0); ORG = (255 ,165 ,0); PUR = (128, 0, 128)

# Define some random patterns for the TV noise effect
patterns = [
    [BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT],
    [GRN, ORG, YEL, WHT, BLK, RED, BLU, PUR],
    [PUR, BLU, RED, BLK, WHT, YEL, ORG, GRN],
    [WHT, YEL, ORG, GRN, PUR, BLU, RED, BLK],
    [random.choice([BLK, RED, BLU, PUR, GRN, ORG, YEL, WHT]) for _ in range(8)]
]

#print(patterns)
print() # line feed for console to separate colour sensor warning...

# (8) random 'moving scenes' to scroll
scenes = ['',\
         '.',\
         '#.',\
         '-_-*',\
         '.. $#$.$',\
         'FakeTVEmulatorfortheRPi',\
         '...=== =|====|o|:..|.Xx..',\
         ' ._-=# - == - ### ==- _ ** _ = - .*.. @@@@@']

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
      r = random.randint(32, 255)
      g = random.randint(32, 255)
      b = random.randint(32, 255)
      pixels = [(r, g, b) for i in range(64)]
      sense.set_pixels(pixels)
      time.sleep(random.uniform(0.1, 2))
      sense.clear()

# Main loop
while True:
    TV = random.randint(1, 3) # pick an effect at random
    print('  Program running:', end='') # for console use to show program is running

    if TV == 1:  
        LoopNoise = random.randint(3, 8)
        print('  noise x ', LoopNoise, end='\r')
        for _ in range(LoopNoise):
          tv_noise()
          time.sleep(random.uniform(0.1, 5))
    
    elif TV == 2:
        LoopScene = random.randint(1, 2)
        print('  scene x ', LoopScene, end='\r')
        for _ in range(LoopScene):
          moving_scene()
          time.sleep(random.uniform(0.1, 5))

    elif TV == 3:
        LoopFlash = random.randint(1, 3)    
        print('  flash x ', LoopFlash, end='\r')
        for _ in range(LoopFlash):
          flash_display()
          time.sleep(random.uniform(0.1, 5))
