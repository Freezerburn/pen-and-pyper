import random
from engine.pennpaper.nibs import Nibs, Wells
from engine.entities.core import Drawable, Invisible


class RandomMover(Drawable):
    def init(self, asset_key):
        self.vel = 210.0
        self.cur_tick = 0
        self.current_anim = asset_key
        return [
            Wells.Create(self._x, self._y, asset_key)
        ]

    def tick(self, dt):
        move = self.vel * dt
        dx = 0.0
        dy = 0.0
        ret = []
        self.cur_tick += 1
        if self.cur_tick > 19:
            self.cur_tick = 0
            rand_val = random.randint(0, 99)
            if rand_val < 24:
                dx -= move
            if rand_val < 49 and rand_val >= 25:
                dx += move
            if rand_val < 74 and rand_val >= 50:
                dy += move
            if rand_val < 99 and rand_val >= 75:
                dy -= move
        self._x += dx
        self._y += dy
        if dx > 0:
            if dy > 0:
                new_animation = 'player_walk_up'
            elif dy < 0:
                new_animation = 'player_walk_down'
            else:
                new_animation = 'player_walk_right'
        elif dx < 0:
            if dy > 0:
                new_animation = 'player_walk_up'
            elif dy < 0:
                new_animation = 'player_walk_down'
            else:
                new_animation = 'player_walk_left'
        elif dy > 0:
            new_animation = 'player_walk_up'
        elif dy < 0:
            new_animation = 'player_walk_down'
        elif self.current_anim == 'player_walk_left':
            new_animation = 'player_stand_left'
        elif self.current_anim == 'player_walk_right':
            new_animation = 'player_stand_right'
        elif self.current_anim == 'player_walk_up':
            new_animation = 'player_stand_up'
        elif self.current_anim == 'player_walk_down':
            new_animation = 'player_stand_down'
        else:
            new_animation = None
        if new_animation is not None and new_animation != self.current_anim:
            ret.append(Nibs.SwapAnimation(self.uid, new_animation))
            self.current_anim = new_animation
        if dx != 0 or dy != 0:
            ret.append(Nibs.Move(self.uid, dx, dy))
        return ret

class TestSpawned(Drawable):
    DIE_TIME = 0.8
    Y_ACCEL = -67.0

    DEFAULT_X_VARIANCE = 50.0
    DEFAULT_Y_VARIANCE = 60.0

    DECEL = 70.0

    LIVE_TIME = 1.5
    DROP_TIME = 0.37
    DROP_TIME_VARIANCE = 0.24

    def init(self, asset_key):
        self._timer = 0.0
        if random.randrange(0, 100) < 49:
            self._vel_x = random.random() * TestSpawned.DEFAULT_X_VARIANCE
        else:
            self._vel_x = random.random() * -TestSpawned.DEFAULT_X_VARIANCE
        if random.randrange(0, 100) < 79:
            self._vel_y = random.random() * TestSpawned.DEFAULT_Y_VARIANCE
        else:
            self._vel_y = random.random() * -TestSpawned.DEFAULT_Y_VARIANCE
        self._drop_time = TestSpawned.DROP_TIME + random.random() * TestSpawned.DROP_TIME_VARIANCE
        return [
            Wells.Create(self._x, self._y, asset_key)
        ]

    def tick(self, dt):
        ret = []
        self._timer += dt
        if self._timer > self._drop_time:
            self._vel_x = 0.0
            self._vel_y = 0.0
        else:
            self._vel_y += TestSpawned.Y_ACCEL * dt
            ret.append(Nibs.Move(self.uid, self._vel_x * dt, self._vel_y * dt))
        if self._timer > TestSpawned.DIE_TIME:
            ret.append(Wells.Destroy(self.uid))
        return None if ret == [] else ret


class TestSpawner(Invisible):
    SPAWN_DELAY = 1 / 20.0

    def init(self):
        self._active = False
        self._timer = 0.0
        self._x = 300
        self._y = 300

    def tick(self, dt):
        if self._active:
            self._active = False
            # self._timer += dt
            # if self._timer > TestSpawner.SPAWN_DELAY:
            self._timer = 0.0
            ret = []
            for i in xrange(0, 120):
                ret.append(Wells.Create(self._x, self._y, 'gem', constructor=TestSpawned, child=True))
            return ret
            # return [
            # ]
        return None

    def on_key_press(self, command):
        if command[1] == 'J':
            self._active = True
            return True
        elif command[1] == 'K':
            self._x += 5
            return Nibs.Move(self.uid, 5.0, 0.0)
        return False

    def on_key_release(self, command):
        if command[1] == 'J':
            self._active = False
            return True
        return False
