from collections import namedtuple


class Nibs(object):
    """Commands that interact with the Paper.
    """
    _next_uid = 0
    CREATE_KEY = 4
    DESTROY_KEY = 5
    MOVE_KEY = 10

    @staticmethod
    def next_uid():
        ret = Nibs._next_uid
        Nibs._next_uid += 1
        return ret

    @staticmethod
    def prev_uid():
        return Nibs._next_uid - 1

    @staticmethod
    def Sprite(key, asset, width=None, height=None):
        return (0, key, asset, width, height)

    @staticmethod
    def Text(x, y, chars, font='Times New Roman', size=12, level=5):
        return (13, Nibs.next_uid(), x, y, chars, font, size, level)

    @staticmethod
    def Animate(animation_key, info, period=None, uses_grid=False):
        return (1, animation_key, info, period, uses_grid)

    @staticmethod
    def SwapAnimation(uid, animation_key):
        return (2, uid, animation_key)

    @staticmethod
    def ResetAnimation(uid):
        return (11, uid)

    @staticmethod
    def FreezeAnimation(uid):
        return (12, uid)

    @staticmethod
    def AnimationEnded(uid, animation_key):
        return ('ANIMATIONENDED', uid, animation_key)

    @staticmethod
    def Delete(key):
        return (3, key)

    @staticmethod
    def Create(x, y, asset_key, width=None, height=None, level=5, uid=None):
        return (Nibs.CREATE_KEY, Nibs.next_uid() if uid is None else uid, asset_key, x, y, width, height, level)

    @staticmethod
    def Destroy(uid):
        return (Nibs.DESTROY_KEY, uid)

    @staticmethod
    def Hide(uid):
        return (6, uid)

    @staticmethod
    def HideLastCreated():
        return Nibs.Hide(Nibs.prev_uid())

    @staticmethod
    def Reveal(uid):
        return (7, uid)

    @staticmethod
    def ChangeLevel(uid, level):
        return (8, uid, level)

    @staticmethod
    def OffsetLevel(uid, level_offset):
        return (9, uid, level_offset)

    @staticmethod
    def Move(uid, dx, dy):
        return (Nibs.MOVE_KEY, uid, dx, dy)

    @staticmethod
    def Teleport(uid, x, y):
        return (11, uid, x, y)

    @staticmethod
    def KeyEvent(keycode, keystring, is_pressed, modifiers):
        return ('KEYEVENT', keycode, keystring, is_pressed, modifiers)

    @staticmethod
    def Tell(uid, message_key, *data):
        return (15, message_key, data)

    @staticmethod
    def Kill():
        return ('KILL')

    @staticmethod
    def EndInit():
        return (14,)


class Wells(object):
    """Commands that interact with the Pen.
    """
    _create_constructor = namedtuple('WELL_CREATE', ['type', 'x', 'y', 'assets',
        'constructor', 'width', 'height', 'level', 'child', 'context', 'extra'])
    _delete_constructor = namedtuple('WELL_DESTROY', ['type', 'uid'])
    _text_constructor = namedtuple('WELL_TEXT', ['type', 'x', 'y', 'chars',
        'constructor', 'font', 'font_size', 'level', 'child', 'context', 'extra'])
    _makecontext_constructor = namedtuple('WELL_MAKECONTEXT', ['type', 'name'])
    _setcontext_constructor = namedtuple('WELL_SETCONTEXT', ['type', 'uid', 'name'])
    _swapcontext_constructor = namedtuple('WELL_SWAPCONTEXT', ['type', 'name', 'hide_previous'])

    HIDE_PREVIOUS = 1

    @staticmethod
    def Create(x=None, y=None, assets=None, constructor=None, width=None, height=None,
        level=5, child=False, context=None, **extra):
        return Wells._create_constructor('CREATE', x, y, assets, constructor, width, height, level, child, context, extra)

    @staticmethod
    def Destroy(uid):
        return Wells._delete_constructor('DESTROY', uid)

    @staticmethod
    def Text(x, y, chars, constructor=None, font='Times New Roman', font_size=12,
        level=5, child=False, context=None, **extra):
        return Wells._text_constructor('TEXT', x, y, chars, constructor, font, font_size, level, child, context, extra)

    @staticmethod
    def MakeContext(name):
        return Wells._makecontext_constructor('MAKECONTEXT', name)

    @staticmethod
    def SetContext(uid, name):
        return Wells._setcontext_constructor('SETCONTEXT', uid, name)

    @staticmethod
    def Transition(name, type=HIDE_PREVIOUS):
        return Wells._swapcontext_constructor('TRANSITION', name, type)
