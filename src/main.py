import cProfile
import os
import sys
from engine.pennpaper import artbox, decorators
from engine.pennpaper.nibs import Nibs, Wells
from engine.entities.core import Ground
from engine.entities.testing import RandomMover, TestSpawner
from game.entities.player import Player
from game.entities.japanese import Character


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


@decorators.peninit
def cache_initial():
    yield Nibs.Sprite('player', 'player/sprites_map_claudius.png', width=32, height=64)
    yield Nibs.Sprite('grass', 'ground/grass.jpg')
    yield Nibs.Sprite('gem', 'SpriteGem.png')
    yield Nibs.Animate('player_stand_left',
        [('player', 2, 0)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_stand_right',
        [('player', 0, 0)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_stand_up',
        [('player', 1, 0)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_stand_down',
        [('player', 3, 0)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_walk_left',
        [('player', 2, 2), ('player', 2, 3),
        ('player', 2, 4), ('player', 2, 5)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_walk_right',
        [('player', 0, 2), ('player', 0, 3),
        ('player', 0, 4), ('player', 0, 5)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_walk_up',
        [('player', 1, 2), ('player', 1, 3),
        ('player', 1, 4), ('player', 1, 5)],
        period=0.17, uses_grid=True)
    yield Nibs.Animate('player_walk_down',
        [('player', 3, 2), ('player', 3, 3),
        ('player', 3, 4), ('player', 3, 5)],
        period=0.17, uses_grid=True)
    for f in os.listdir('../res/hiragana'):
        key = f[:f.rindex('.')]
        yield Nibs.Sprite(key, 'hiragana/%s' % f)


@decorators.peninit
def create_initial():
    # yield (Player, 300, 100, 'player_stand_right')
    yield Wells.Create(300, 100, 'player_stand_right', constructor=Player, context='start')
    # yield Wells.Create(WINDOW_WIDTH / 2.0 - 50.0, WINDOW_HEIGHT - 100.0, ['ka'],
    #     constructor=Character, chars='ka', active=True, context='start')
    for y in xrange(0, WINDOW_HEIGHT / 96.0):
        for x in xrange(0, WINDOW_WIDTH / 32.0):
            yield Wells.Create(x * 32.0, y * 32.0, 'grass', height=32.0, width=32.0, constructor=Ground, context='start')
    for i in xrange(0, 1):
        yield Wells.Create(100, 100, 'player_stand_right', constructor=RandomMover, context='start')
    yield Wells.Create(constructor=TestSpawner, context='start')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    box = artbox.ArtBox(WINDOW_WIDTH, WINDOW_HEIGHT)
    box.add_resource_folder('../res')
    box.open()
    # cProfile.run('box.open()')
