from engine.pennpaper.pen import _init_funcs


def peninit(fn):
    _init_funcs.append(fn)
    return fn
