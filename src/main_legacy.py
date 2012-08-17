# Python library code.
import os

# Third party library code.
import pyglet
from pyglet.gl import *

# My code
from managers import texture


WINDOW_SIZE = (640, 480)
window = pyglet.window.Window(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], vsync=True)
pyglet.resource.path = [os.path.abspath('%s/../res' % os.getcwd())]
pyglet.resource.path = ['../res']
pyglet.resource.reindex()
glClearColor(1.0, 1.0, 1.0, 1.0)

texture.cache('ka', 'hiragana/ka.png')
texture.destroy('ku')


def run_game_logic(dt):
    """Runs all the logic required for the game.
    """
    pass
# Call the game logic function 60 times per second.
fps = pyglet.clock.ClockDisplay()


@window.event
def on_draw():
    window.clear()
    dt = pyglet.clock.tick()
    fps.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(run_game_logic, 1 / 60.0)
    pyglet.app.run()
