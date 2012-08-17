import random
from pennpaper.nibs import Nibs


class RandomMover(object):
    def __init__(self, uid, x, y, current_anim):
        self.uid = uid
        self.x = x
        self.y = y
        self.vel = 210.0
        self.cur_tick = 0
        self.current_anim = current_anim

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
        self.x += dx
        self.y += dy
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
