class Nibs(object):
    @staticmethod
    def Sprite(key, asset, level=5, width=None, height=None):
        return (0, key, asset, level, width, height)

    @staticmethod
    def Animate(animation_key, info, level=5, period=None, uses_grid=False):
        return (1, animation_key, info, level, period, uses_grid)

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
    def Create(uid, asset_key, x, y):
        return (4, uid, asset_key, x, y)

    @staticmethod
    def Destroy(uid):
        return (5, uid)

    @staticmethod
    def Hide(uid):
        return (6, uid)

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
        return (10, uid, dx, dy)

    @staticmethod
    def Teleport(uid, x, y):
        return (11, uid, x, y)

    @staticmethod
    def KeyEvent(keycode, keystring, is_pressed, modifiers):
        return ('KEYEVENT', keycode, keystring, is_pressed, modifiers)

    @staticmethod
    def Kill():
        return ('KILL')
