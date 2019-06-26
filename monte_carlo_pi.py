#   Copyright 2019 Kevin Godden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Monte Carlo Simulation of throwing pebbles onto a circle drawn on the sand
    on a desert island in desperate attempt to estimate Pi to a few places of decimals
    Pi is proportional to the ratio of 'hits' to 'throws'.

    Another method would be to draw some parallel lines in the sand and start throwing
    sticks to see how many land on the lines, a la. the Buffon needle problem, see:

    https://github.com/kgodden/buffon_needle

    This simulation method converges faster and is simpler, but perhaps is not as much fun!

    KG
"""

import matplotlib.pyplot as plt
from random import *
import time


def draw_board(fig, radius, gwidth, gheight):

    circle = plt.Circle((0, 0), radius, color='b', fill=False)
    fig.gca().add_artist(circle)

    # I can never understand pyplot!
    plt.plot(-gwidth / 2, -gheight / 2)
    plt.plot(gwidth / 2, -gheight / 2)
    plt.plot(gwidth / 2, gheight / 2)
    plt.plot(-gwidth / 2, gheight / 2)
    

# The probability (p) that a pebble will land inside
# the circle as opposed to not is the ratio of the
# area of the circle to the area of the bounding box:
#    p = (Pi * r^2) / (4 * r^2),
# so Pi ~= p * 4 = 4 * hits / throws
def estimate_pi(throws, hits):
    return 4.0 * float(hits) / throws
        
    
def throw_pebbles(radius, pebble_radius, number_of_throws, fig, want_graphics):

    # hits
    hits = 0
    
    # Let's get a throwing!
    for throws in range(1, number_of_throws):

        # Random point in bounding box
        x = uniform(-radius, radius)
        y = uniform(-radius, radius)

        # Does this point lie within the circle?
        hit = x ** 2 + y ** 2 <= (radius - pebble_radius) ** 2
        
        if hit:
            # Yep, it's a hit!
            hits += 1

        # draw point if drawing is enabled
        if want_graphics:
            col = 'r' if hit else 'g'
            circle = plt.Circle((x, y), pebble_radius, color=col, fill=False)
            fig.gca().add_artist(circle)

        # Update graphics display
        if want_graphics and throws % 100 == 0:
            plt.pause(0.0001)
            
        # Estimate Pi every 100 throws, and print it out
        if throws % 100 == 0 and throws > 0:
            estimate = estimate_pi(throws, hits)
            print("Throws: %d, hits: %d, estimate: %f" % (throws, hits, estimate))

    estimate = estimate_pi(throws, hits)

    print("Pi is (approx.) %f" % estimate)


def monte_carlo_pi():

    # radius of circle onto which we will
    # throw our 'pebbles'
    radius = 100

    # Graphics width & Height
    gwidth = gheight = 2 * radius

    # The radius of the pebble that
    # we will throw, smaller values yield
    # better approximations of Pi (i.e. grains
    # of sand rather than rocks)
    pebble_radius = .2
    
    # Set this to True if you want to
    # draw the pebbles on the board
    # it runs (much) slower when we draw..
    want_graphics = True

    # How many times should we throw the
    # pebble?
    number_of_throws = 9000

    # Some drawing stuff
    fig = plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    draw_board(fig, radius, gwidth, gheight)
    
    # run simulation
    throw_pebbles(radius, pebble_radius, number_of_throws, fig, want_graphics)
    
    # Show the graphics for a bit
    # before exiting
    if want_graphics:
        time.sleep(20)


if __name__ == "__main__":
    monte_carlo_pi()
