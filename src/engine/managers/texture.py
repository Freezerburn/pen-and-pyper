import pyglet

_cached = {}
_levels = {}
_batch = pyglet.graphics.Batch()


def _get_level_group(level):
    try:
        group = _levels[level]
    except KeyError:
        _levels[level] = pyglet.graphics.OrderedGroup(level)
        group = _levels[level]
    return group


def cache(name, directory, level=0, draw=False):
    try:
        return _cached[name]
    except KeyError:
        group = _get_level_group(level)
        if draw:
            _cached[name] = (pyglet.resource.image(directory), level)
            ret = pyglet.sprite.Sprite(_cached[name][0], batch=_batch, group=group)
            return ret
        else:
            _cached[name] = (pyglet.resource.image(directory), level)


def destroy(name=None, sprite=None):
    try:
        del _cached[name]
    except KeyError:
        pass


def get_sprite(name):
    try:
        ret, level = _cached[name][0]
        group = _get_level_group(level)
        ret = pyglet.sprite.Sprite(ret, batch=_batch, group=group)
        return ret
    except KeyError:
        return None


def set_sprite_level(name, level):
    try:
        _cached[name] = (_cached[name][0], level)
    except KeyError:
        pass


def get_sprite_level(name):
    try:
        return _cached[name][1]
    except KeyError:
        return None


def set_drawable(name, draw=True):
    if draw:
        try:
            sprite, level = _cached[name]
            sprite.batch = _batch
            try:
                sprite.group = _levels[level]
            except KeyError:
                _levels[level] = pyglet.graphics.OrderedGroup(level)
                sprite.group = _levels[level]
        except KeyError:
            pass
    else:
        try:
            sprite, level = _cached[name]
            sprite.batch = None
            sprite.group = None
        except KeyError:
            pass


def draw_all():
    _batch.draw()
