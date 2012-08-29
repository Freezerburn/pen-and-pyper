import pyglet
from pyglet.image import AnimationFrame, Animation
from nibs import Nibs


class Paper(object):
    width = 640
    height = 480

    """'Drawing' process. Communicates with worker for changes in graphics, then draws everything.
    """
    def __init__(self, width=640, height=480):
        Paper.width = width
        Paper.height = height
        self._textures = {}
        self._levels = {}
        self._ents = {}
        self._hidden = {}
        self._batch = pyglet.graphics.Batch()
        self._texts = []
        self._frame = 0
        self._init = False
        self._command_callbacks = [
            self._sprite,
            self._animate,
            self._swap_animation,
            self._delete,
            self._create,
            self._destroy,
            self._hide,
            self._reveal,
            self._change_level,
            self._offset_level,
            self._move,
            self._reset_animation,
            self._freeze_animation,
            self._text,
            self._endinit
        ]
        self._window = pyglet.window.Window(Paper.width, Paper.height, visible=False, vsync=False)
        self._fps = pyglet.clock.ClockDisplay()
        pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)

    def __call__(self):
        self.unfurl()

    def _tell_pen(self, ink_blob):
        self._paper_mouth.send(ink_blob)

    def _listen_to_pen(self):
        while self._pen_ear.poll():
            yield self._pen_ear.recv()

    def _handle_command(self, command):
        try:
            self._command_callbacks[command[0]](command)
        except KeyError:
            print 'Error handling: %s' % str(command)

    def _get_level_group(self, level):
        try:
            group = self._levels[level]
        except KeyError:
            self._levels[level] = pyglet.graphics.OrderedGroup(level)
            group = self._levels[level]
        return group

    def _sprite(self, command):
        key, asset, width, height = command[1:]
        # print 'Caching - key=%s, asset=%s, level=%s, slice width=%s, slice height=%s' % (key, asset, level, width, height)
        if key not in self._textures:
            self._textures[key] = pyglet.resource.image(asset)
            if width is not None and height is not None:
                tex = self._textures[key]
                cols = tex.width / width
                rows = tex.height / height
                tex = pyglet.image.ImageGrid(tex, rows, cols).get_texture_sequence()
                self._textures[key] = tex

    def _text(self, command):
        uid, x, y, chars, font, size, level = command[1:]
        # print 'Text - uid=%s, x=%s, y=%s chars=%s, font=%s, size=%s, level=%s' % (uid, x, y, chars, font, size, level)
        self._ents[uid] = ((pyglet.text.Label(chars,
            color=(0, 0, 0, 255),
            x=x,
            y=y,
            font_name=font,
            font_size=size,
            batch=self._batch,
            group=self._get_level_group(level)), level))

    def _animate(self, command):
        frames = []
        anim_key, info, period, uses_grid = command[1:]
        # print 'Creating animation - key=%s, period=%s, uses_grid=%s, info=%s' % (anim_key, period, uses_grid, info)
        try:
            if period is not None:
                if uses_grid:
                    for key, x, y in info:
                        frames.append(AnimationFrame(self._textures[key][(x, y)], period))
                else:
                    for key in info:
                        frames.append(AnimationFrame(self._textures[key], period))
            elif uses_grid:
                for key, x, y, timing in info:
                    frames.append(AnimationFrame(self._textures[key][(x, y)], timing))
            else:
                for key, timing in info:
                    frames.append(AnimationFrame(self._textures[key], timing))
            anim = Animation(frames)
            self._textures[anim_key] = anim
        except KeyError:
            print 'whoops'

    def _swap_animation(self, command):
        uid, animation_key = command[1:]
        # print 'Swapping animation - uid=%s, animation key=%s' % (uid, animation_key)
        try:
            tex = self._textures[animation_key]
            sprite, _ = self._ents[uid]
            sprite.image = tex
        except ValueError:
            pass

    def _reset_animation(self, command):
        pass

    def _freeze_animation(self, command):
        pass

    def _delete(self, command):
        # print 'Delete - key=%s'
        try:
            del self._textures[command[1]]
        except KeyError:
            pass

    def _create(self, command):
        uid, key, x, y, width, height, level = command[1:]
        # print 'Creating - uid=%s, asset_key=%s, x=%s, y=%s, width=%s, height=%s' % (uid, key, x, y, width, height)
        tex = self._textures[key]
        group = self._get_level_group(level)
        sprite = pyglet.sprite.Sprite(tex, batch=self._batch, group=group)
        sprite.x = x
        sprite.y = y
        if width is not None and height is not None and width == height:
            sprite.scale = width / sprite.width
        self._ents[uid] = (sprite, level)

    def _destroy(self, command):
        uid = command[1]
        # print 'Destroy - uid=%s' % uid
        ent, _ = self._ents[uid]
        del self._ents[uid]
        ent.delete()

    def _hide(self, command):
        uid = command[1]
        # print 'Hiding - uid=%s' % uid
        to_hide = self._ents[uid]
        del self._ents[uid]
        self._hidden[uid] = to_hide
        to_hide[0].batch = None
        to_hide[0].group = None

    def _reveal(self, command):
        uid = command[1]
        # print 'Revealing - uid=%s' % uid
        to_reveal, level = self._hidden[uid]
        del self._hidden[uid]
        self._ents[uid] = (to_reveal, level)
        to_reveal.group = self._get_level_group(level)
        to_reveal.batch = self._batch

    def _change_level(self, command):
        # print 'Changing level - uid=%s, level=%s'
        self._ents[command[1]][0].group = self._get_level_group(command[2])

    def _offset_level(self, command):
        # print 'Offset level - uid=%s, offset=%s'
        sprite, level = self._ents[command[1]]
        level += command[2]
        sprite.group = self._get_level_group(level)
        self._ents[command[1]] = (sprite, level)

    def _move(self, command):
        # print 'Moving - uid=%s, dx=%s, dy=%s' % command[1:]
        sprite, _ = self._ents[command[1]]
        sprite.x += command[2]
        sprite.y += command[3]

    def _endinit(self, command):
        self._init = True

    def on_draw(self):
        self._window.clear()
        self._dt = pyglet.clock.tick()
        self._batch.draw()
        self._fps.draw()

    def on_key_press(self, symbol, modifiers):
        self._tell_pen(Nibs.KeyEvent(symbol, pyglet.window.key.symbol_string(symbol), True, modifiers))

    def on_key_release(self, symbol, modifiers):
        self._tell_pen(Nibs.KeyEvent(symbol, pyglet.window.key.symbol_string(symbol), False, modifiers))

    # Coroutine! :D
    def _run_logic(self):
        callbacks = self._command_callbacks
        listen_func = self._listen_to_pen
        frame = self._frame
        try:
            while True:
                dt = (yield)
                possible_msgs = listen_func()
                for msg in possible_msgs:
                    try:
                        callbacks[msg[0]](msg)
                    except KeyError:
                        print 'Error handling: %s' % str(msg)
                    del msg
                del possible_msgs
                frame += 1
        except EOFError:
            self._tell_pen(Nibs.Kill())
            pyglet.app.exit()
        except IOError:
            self._tell_pen(Nibs.Kill())
            pyglet.app.exit()

    def unfurl(self, pen, paper):
        """Tells the Paper to begin looking for commands from the Pen and draw everything.
        """
        self._pen_ear, to_close = pen
        to_close.close()
        to_close, self._paper_mouth = paper
        to_close.close()

        self._window.event(self.on_draw)
        self._window.event(self.on_key_press)
        self._window.event(self.on_key_release)
        self._tell_pen(('CLOCK', 120.0))
        while not self._init:
            msgs = self._listen_to_pen()
            for msg in msgs:
                self._command_callbacks[msg[0]](msg)
        callback = self._run_logic()
        callback.next()
        pyglet.clock.schedule_interval(callback.send, 1 / 120.0)
        self._window.set_visible()
        pyglet.app.run()

        self._pen_ear.close()
        self._paper_mouth.close()
