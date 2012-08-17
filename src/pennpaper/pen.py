import platform
import random
import time
from nibs import Nibs
from entities.player import Player
from entities.testing import RandomMover

# Set an appropriate clock function based on our platform.
try:
    platform.win32_ver()
    clock = time.clock
except:
    pass
try:
    platform.mac_ver
    clock = time.time
except:
    pass
try:
    platform.dist
    clock = time.time
except:
    pass


class Pen(object):
    """'Worker' process. Does all the processing for moving objects, collision, etc.
    """
    _next_uid = 0
    _frame = 0

    def __init__(self):
        self._ents = []
        self._nokey_ents = []
        self._clock = None
        self._running = True
        self._sleep_time = None
        self._event_handlers = {
            'KILL': self._kill,
            'KEYEVENT': self._handle_key,
            'CLOCK': self._init_clock
        }

    def __call__(self, pen, paper):
        self.dip(pen, paper)

    @classmethod
    def get_uid(cls):
        ret = cls._next_uid
        cls._next_uid += 1
        return ret

    def _listen_to_paper(self):
        while self._paper_ear.poll():
            yield self._paper_ear.recv()

    def _tell_paper(self, ink_blob):
        self._pen_mouth.send(ink_blob)

    def _init_clock(self, command):
        print 'Got clock'
        self._sleep_time = command[1]

    def _cache_initial(self):
        self._tell_paper(Nibs.Sprite('player', 'player/sprites_map_claudius.png', width=32, height=64))
        self._tell_paper(Nibs.Animate('player_stand_left',
            [('player', 2, 0)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_stand_right',
            [('player', 0, 0)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_stand_up',
            [('player', 1, 0)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_stand_down',
            [('player', 3, 0)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_walk_left',
            [('player', 2, 2), ('player', 2, 3),
            ('player', 2, 4), ('player', 2, 5)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_walk_right',
            [('player', 0, 2), ('player', 0, 3),
            ('player', 0, 4), ('player', 0, 5)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_walk_up',
            [('player', 1, 2), ('player', 1, 3),
            ('player', 1, 4), ('player', 1, 5)],
            period=0.17, uses_grid=True))
        self._tell_paper(Nibs.Animate('player_walk_down',
            [('player', 3, 2), ('player', 3, 3),
            ('player', 3, 4), ('player', 3, 5)],
            period=0.17, uses_grid=True))
        # for f in os.listdir('../res/hiragana'):
        #     key = f[:f.rindex('.')]
        #     self._tell_paper(Nibs.Sprite(key, 'hiragana/%s' % f))

    def _create_initial(self):
        # self._create_ent(Test, 'ka', 100, 100)
        # self._create_ent(Test, 'tzu', 300, 100)
        self._create_ent(Player, 'player_stand_right', 300, 100)
        for i in xrange(0, 330):
            self._create_ent(RandomMover, 'player_stand_right', 100, 100)

    def _create_ent(self, ent_class, asset_key, x, y):
        uid = Pen.get_uid()
        self._tell_paper(Nibs.Create(uid, asset_key, x, y))
        self._ents.append(ent_class(uid, x, y, 'player_stand_right'))

    def _kill(self, command=None):
        print 'Killing Pen process'
        self._pen_mouth.close()
        self._paper_ear.close()
        exit(0)

    def _handle_key(self, command):
        command = command[1:]
        # print 'Key event - code=%s, string=%s, pressed=%s, modifers=%s' % command
        remove_later = []
        for ent in self._ents:
            try:
                if command[2]:
                    ret = ent.on_key_press(command)
                else:
                    ret = ent.on_key_release(command)
            except AttributeError:
                self._nokey_ents.append(ent)
                remove_later.append(ent)
            if ret is not None:
                if type(ret) == tuple:
                    self._tell_paper(ret)
                else:
                    pass
        for ent in remove_later:
            self._ents.remove(ent)

    def _run_loop(self):
        # Make everything local so that no global lookups occur.
        last_time = clock()
        send_func = self._pen_mouth.send
        clock_func = clock
        listen_func = self._listen_to_paper
        handlers = self._event_handlers
        sleep_time = self._sleep_time
        sleep_func = time.sleep
        num_events = 0
        to_one_sec = 0
        last_frames = 0
        while True:
            dt = clock_func() - last_time
            if dt < 0.0001:
                sleep_func(0.003)
                continue
            to_one_sec += dt
            last_time = clock_func()
            for event in listen_func():
                handlers[event[0]](event)
            # print 'PEN %s' % dt
            # Handle the normal entities.
            for ent in self._ents:
                event = ent.tick(dt)
                if not event == (0.0, 0.0):
                    if type(event) == list:
                        for e in event:
                            num_events += 1
                            send_func(e)
                    else:
                        to_send = (10, ent.uid, event[0], event[1])
                        num_events += 1
                        send_func(to_send)
            # Handle the entities that have been discovered to not be able to handle key events.
            for ent in self._nokey_ents:
                event = ent.tick(dt)
                if not event == (0.0, 0.0):
                    if type(event) == list:
                        for e in event:
                            num_events += 1
                            send_func(e)
                    else:
                        to_send = Nibs.Move(ent.uid, event[0], event[1])
                        num_events += 1
                        send_func(to_send)
            Pen._frame += 1
            last_frames += 1
            if to_one_sec >= 1.0:
                to_one_sec -= 1.0
                print 'FPS: %s' % last_frames
                last_frames = 0
            # if Pen._frame % 120 == 0:
            #     print num_events
            #     num_events = 0
            sleep = sleep_time - (clock() - last_time)
            # if sleep > 0.0083:
            #     sleep_func(sleep)

    def dip(self, pen, paper):
        """Tells the Pen to start processing movement, collision, etc.
        """
        to_close, self._pen_mouth = pen
        to_close.close()
        self._paper_ear, to_close = paper
        to_close.close()

        random.seed()
        while self._sleep_time is None:
            for event in self._listen_to_paper():
                if event[0] == 'CLOCK':
                    self._init_clock(event)
                    break
            time.sleep(0.01)
        self._cache_initial()
        self._create_initial()
        try:
            self._run_loop()
        except EOFError:
            self._kill()
        except IOError:
            self._kill()
