from engine.pennpaper.nibs import Nibs, Wells
from engine.entities.core import Drawable


class Player(Drawable):
    def init(self, asset_key):
        self.moving = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.vel = 210.0
        self.current_anim = asset_key
        return [
            Wells.Create(self._x, self._y, asset_key)
        ]

    def tick(self, dt):
        move = self.vel * dt
        # if move > 1.0:
        #     print "DT: %s" % dt
        dx = 0.0
        dy = 0.0
        ret = []
        if self.left:
            dx -= move
        if self.right:
            dx += move
        if self.up:
            dy += move
        if self.down:
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

    def on_key_press(self, event):
        keystring = event[1]
        if keystring == 'LEFT':
            self.left = True
            return True
        elif keystring == 'RIGHT':
            self.right = True
            return True
        elif keystring == 'UP':
            self.up = True
            return True
        elif keystring == 'DOWN':
            self.down = True
            return True
        return False

    def on_key_release(self, event):
        keystring = event[1]
        if keystring == 'LEFT':
            self.left = False
            return True
        elif keystring == 'RIGHT':
            self.right = False
            return True
        elif keystring == 'UP':
            self.up = False
            return True
        elif keystring == 'DOWN':
            self.down = False
            return True
        return False
