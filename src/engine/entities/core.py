from engine.pennpaper.nibs import Wells


class Invisible(object):
    """An entity that is not shown on screen, and is purely used to calculate things in the background.
    """
    def __init__(self, uid, context):
        self.uid = uid
        self.context = context
        self._children = []

    def init(self, *extra):
        return None

    def tick(self, dt):
        return None

    def give_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children


class InputInvisible(Invisible):
    def on_key_press(self, command):
        return False

    def on_key_release(self, command):
        return False


class Drawable(object):
    """An entity that is drawn to the screen.
    """
    def __init__(self, uid, x, y, context):
        self._x = x
        self._y = y
        self.uid = uid
        self.context = context
        self._children = []

    def init(self, asset_key, **extra):
        return [
            Wells.Create(self._x, self._y, asset_key)
        ]

    def tick(self, dt):
        return None

    def give_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children


class InputDrawable(Drawable):
    def on_key_press(self, event):
        return False

    def on_key_release(self, event):
        return False


class Ground(Drawable):
    """A piece of the ground that just provides pretty scenery.
    """
    def init(self, asset_key, width, height):
        return [
            Wells.Create(self._x, self._y, asset_key, width=width, height=height, level=0)
        ]
