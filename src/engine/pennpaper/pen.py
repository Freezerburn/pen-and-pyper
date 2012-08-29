import platform
import random
import time
from nibs import Nibs

from pyglet.clock import Clock

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
_init_funcs = []


class Pen(object):
    """'Worker' process. Does all the processing for moving objects, collision, etc.
    """
    _frame = 0

    def __init__(self):
        self._ents = {}
        self._nokey_ents = {}
        self._contexts = {}
        self._contexts['start'] = {}
        self._current_context = 'start'
        self._clock = None
        self._running = True
        self._sleep_time = None
        self._event_handlers = {
            'KILL': self._kill,
            'KEYEVENT': self._handle_key,
            'CLOCK': self._init_clock
        }
        self._well_handlers = {
            'CREATE': self._well_create,
            'DESTROY': self._well_destroy,
            'TEXT': self._well_text
        }

    def __call__(self, pen, paper):
        self.dip(pen, paper)

    def _listen_to_paper(self):
        while self._paper_ear.poll():
            yield self._paper_ear.recv()

    def _tell_paper(self, ink_blob):
        self._pen_mouth.send(ink_blob)

    def _init_clock(self, command):
        # print 'Got clock'
        self._clock = Clock()
        self._clock.set_fps_limit(command[1])

    def _run_initial(self):
        for func in _init_funcs:
            for msg in func():
                if hasattr(msg, 'type'):
                    remove_later = []
                    create_later = []
                    self._handle_returned_msgs([msg], None, remove_later, create_later)
                    self._handle_delayed_ents(create_later, remove_later)
                else:
                    self._tell_paper(msg)

    def _kill(self, command=None):
        print 'Killing Pen process'
        # if None in self._contexts:
        #     print 'Something is/was in "None" context.'
        #     if len(self._contexts[None]) > 1:
        #         print 'Stuff in "None" context: %s' % str(self._contexts[None])
        self._pen_mouth.close()
        self._paper_ear.close()
        exit(0)

    def _add_ent(self, ent):
        self._ents[ent.uid] = ent
        if ent.context not in self._contexts:
            self._contexts[ent.context] = {}
        self._contexts[ent.context][ent.uid] = ent

    def _delete_ent(self, ent):
        if ent.uid in self._ents:
            del self._ents[ent.uid]
        else:
            del self._nokey_ents[ent.uid]
            del self._contexts[ent.context][ent.uid]

    def _handle_delayed_ents(self, created, removed):
        for ent in created:
            self._add_ent(ent)
        for ent in removed:
            self._delete_ent(ent)

    def _well_create(self, msg, ent, remove_later, create_later):
        if msg.constructor is None:
            self._tell_paper(Nibs.Create(msg.x, msg.y, msg.assets,
                msg.width, msg.height, msg.level, ent.uid))
        elif msg.x == None and msg.y == None and msg.assets == None:
            uid = Nibs.next_uid()
            new_ent = msg.constructor(uid, msg.context)
            new_ent.init(**msg.extra)
            create_later.append(new_ent)
        else:
            uid = Nibs.next_uid()
            child = msg.constructor(uid, msg.x, msg.y, msg.context)
            try:
                self._handle_returned_msgs(child.init(msg.assets, **msg.extra),
                    child, remove_later, create_later)
            except TypeError:
                # print 'Needed width/height'
                self._handle_returned_msgs(child.init(msg.assets, msg.width, msg.height, **msg.extra),
                    child, remove_later, create_later)
            create_later.append(child)
            if msg.child:
                ent.give_child(child)

    def _well_destroy(self, msg, ent, remove_later, create_later):
        if msg.uid in self._ents:
            to_destroy = self._ents[msg.uid]
        else:
            to_destroy = self._nokey_ents[msg.uid]
        children = to_destroy.get_children()
        remove_later.append(to_destroy)
        remove_later += children
        self._tell_paper(Nibs.Destroy(msg.uid))
        for child in children:
            self._tell_paper(Nibs.Destroy(child.uid))

    def _well_text(self, msg, ent, remove_later, create_later):
        command = Nibs.Text(msg.x, msg.y, msg.chars, msg.font, msg.font_size, msg.level)
        child = msg.constructor(command[1], msg.x, msg.y, msg.context)
        self._tell_paper(command)
        self._handle_returned_msgs(child.init(msg.chars, **msg.extra), child, remove_later, create_later)
        create_later.append(child)
        if msg.child:
            ent.give_child(child)

    def _handle_well_msg(self, msg, ent, remove_later, create_later):
        try:
            self._well_handlers[msg.type](msg, ent, remove_later, create_later)
        except KeyError:
            print "Don't know how to handle: %s" % str(msg)

    def _move_children(self, msg):
        ent = self._ents[msg[1]]
        for child in ent._children:
            child._x += msg[2]
            child._y += msg[3]

    def _handle_returned_msgs(self, msgs, ent, remove_later, create_later):
        if msgs is None:
            return
        if type(msgs) == list:
            for msg in msgs:
                if hasattr(msg, 'type'):
                    self._handle_well_msg(msg, ent, remove_later, create_later)
                elif type(msg) == tuple:
                    if msgs[0] == Nibs.MOVE_KEY:
                        self._move_children(msg)
                    self._tell_paper(msg)
                else:
                    print "Don't know how to handle: %s" % str(msg)
        else:
            if msgs[0] == Nibs.MOVE_KEY:
                self._move_children(msgs)
            self._tell_paper(msgs)

    def _get_key_events(self, command):
        remove_later = []
        for uid, ent in self._ents.iteritems():
            ret = (None, False)
            try:
                if command[2]:
                    ret = (ent, ent.on_key_press(command))
                else:
                    ret = (ent, ent.on_key_release(command))
            except AttributeError:
                self._nokey_ents[ent.uid] = ent
                remove_later.append(ent)
            if type(ret[1]) == bool:
                if ret[1]:
                    print 1, ret
                    break
                else:
                    continue
            else:
                print 2, ret
                break
        self._handle_delayed_ents([], remove_later)
        del remove_later
        return ret

    def _handle_key_events(self, ent, events):
        if type(events) != bool:
            remove_later = []
            create_later = []
            self._handle_returned_msgs(events, ent, remove_later, create_later)
            self._handle_delayed_ents(create_later, remove_later)
            del remove_later
            del create_later

    def _handle_key(self, command):
        command = command[1:]
        # print 'Key event - code=%s, string=%s, pressed=%s, modifers=%s' % command
        self._handle_key_events(*self._get_key_events(command))

    def _tick_current_ents(self, dt):
        handle_msgs = self._handle_returned_msgs
        remove_later = []
        create_later = []
        # Handle the normal entities.
        for uid, ent in self._ents.iteritems():
            event = ent.tick(dt)
            handle_msgs(event, ent, remove_later, create_later)
        # Handle the entities that have been discovered to not be able to handle key events.
        for uid, ent in self._nokey_ents.iteritems():
            event = ent.tick(dt)
            handle_msgs(event, ent, remove_later, create_later)
        self._handle_delayed_ents(create_later, remove_later)

    def _run_loop(self):
        # Make everything local so that no global lookups occur.
        clock_func = self._clock.update_time
        listen_func = self._listen_to_paper
        handlers = self._event_handlers
        sleep_func = self._clock._limit
        while True:
            dt = clock_func()
            for event in listen_func():
                handlers[event[0]](event)
            self._tick_current_ents(dt)
            Pen._frame += 1
            sleep_func()

    def dip(self, pen, paper):
        """Tells the Pen to start processing movement, collision, etc.
        """
        to_close, self._pen_mouth = pen
        to_close.close()
        self._paper_ear, to_close = paper
        to_close.close()

        random.seed()
        while self._clock is None:
            for event in self._listen_to_paper():
                if event[0] == 'CLOCK':
                    self._init_clock(event)
                    break
            time.sleep(0.01)
        self._run_initial()
        self._tell_paper(Nibs.EndInit())
        try:
            self._run_loop()
        except EOFError:
            self._kill()
        except IOError:
            self._kill()
        except OSError:
            self._kill()
