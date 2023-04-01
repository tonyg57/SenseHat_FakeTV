# SenseHat_FakeTV.py

Simulate a TV left on in the room on a Raspberry Pi and Sense Hat.

I came up with this program because I couldn't find anything like it that uses the SenseHat here on GitHub.
The program is designed to somewhat emulate the FakeTV hardware device as seen here: https://faketv.com/

I have a DIY prismatic acrylic cube on top of the SenseHat to diffuse the LED matrix.
Running the Raspberry Pi a few feet from a window with the blinds down gives the appearance from outside of a TV left on (i.e. somebody's home).

Feel free to tweak, optimize, and simplify the code for your own use. Recommend using https://trinket.io/sense-hat to test your code.
Be advised that the trinket.io web site objects to the print statements that contain end='' and end='\r'. Just comment them out.
The print statements are for the console so I can see what's going on and that the program is running correctly.

The code is certainly sloppy and I needed some help via ChatGPT because I don't natively speak Python.
