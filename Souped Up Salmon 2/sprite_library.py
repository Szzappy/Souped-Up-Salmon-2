from random import randint

from hud_library import *
pygame.mixer.init()


class Sprite(UIElement):
    def __init__(self, position, size):
        UIElement.__init__(self, position, size)
        brush = UIBrush(self._surface)
        self._velocity = Vector()
        self.should_delete = False
        self.destroyed_by_bullet = False
        self.life_loss = False
        self.difficulty = 20

    def add_velocity(self, velocity_to_add):
        self._velocity.add(velocity_to_add)

    def update(self, delta_time: float):
        move_distance = Vector(self._velocity.x, self._velocity.y)
        move_distance.scale(delta_time)
        self._position.add(move_distance)

    def get_position(self):
        return self._position

    def left(self):
        return self._position.x - self._size.x / 2

    def right(self):
        return self._position.x + self._size.x / 2

    def top(self):
        return self._position.y - self._size.y / 2

    def bottom(self):
        return self._position.y + self._size.y / 2

    def does_collide_with(self, other_sprite):
        return (self.left() <= other_sprite.right()
                and self.right() >= other_sprite.left()
                and self.top() <= other_sprite.bottom()
                and self.bottom() >= other_sprite.top())


class Enemy(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(127, 78))
        image = pygame.image.load("assets/images/bear.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class EnemyBullet(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(75, 65))
        image = pygame.image.load("assets/images/panda.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class EnemyHandler(UIElement):
    def __init__(self, size, difficulty):
        UIElement.__init__(self, Vector(), size)
        self.__enemies = []
        self.__difficulty = difficulty
        self.add_enemies(difficulty)

    def add_enemies(self, difficulty):
        for count in range(difficulty):
            x = 1400
            y = randint(0, self._size.y)
            vx = randint(-200, -100)
            vy = randint(-50, 50)
            enemy = Enemy(Vector(x, y))
            enemy.add_velocity(Vector(vx, vy))
            self.__enemies.append(enemy)

    def update(self, delta_time: float):
        for enemy in self.__enemies:
            enemy.update(delta_time)

        self.__enemies[:] = [enemy for enemy in self.__enemies if enemy.get_position().x > 0
                             and not enemy.should_delete]
        self.__enemies[:] = [enemy for enemy in self.__enemies if 720 > enemy.get_position().y > 0
                             and not enemy.should_delete]

        difference = self.__difficulty - len(self.__enemies)

        if difference > 0:
            self.add_enemies(difference)

    def render(self, brush: UIBrush):
        for bullet in self.__enemies:
            bullet.render(brush)

    def add_enemy(self, enemy_to_add):
        self.__enemies.append(enemy_to_add)

    def get_enemies(self):
        return self.__enemies

    def get_enemy_destroyed(self):
        score = 0
        for enemy in self.__enemies:
            if enemy.destroyed_by_bullet:
                score += 1
        return score


class Bullet(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(36, 24))
        image = pygame.image.load("assets/images/reverse.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class BulletHandler(UIElement):
    def __init__(self, size):
        UIElement.__init__(self, Vector(), size)
        self.__bullets = []

    def update(self, delta_time: float):
        for bullet in self.__bullets:
            bullet.update(delta_time)
        self.__bullets[:] = [bullet for bullet in self.__bullets if bullet.get_position().x < self._size.x and not bullet.should_delete]
        self.__bullets[:] = [enemy for enemy in self.__bullets if bullet.get_position().x > 0 and not bullet.should_delete]

    def render(self, brush: UIBrush):
        for bullet in self.__bullets:
            bullet.render(brush)

    def add_bullet(self, bullet_to_add):
        self.__bullets.append(bullet_to_add)

    def check_collisions(self, enemy_handler):
        enemies = enemy_handler.get_enemies()
        for bullet in self.__bullets:
            for enemy in enemies:
                if bullet.does_collide_with(enemy):
                    bullet.should_delete = True
                    enemy.should_delete = True
                    enemy.destroyed_by_bullet = True


class Ship(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(125, 50))
        image = pygame.image.load("assets/images/salmon.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)
        self.lives = 5
        self.assault = False

    def fire(self, bullet_handler):
        bullet = Bullet(Vector(self._position.x, self._position.y))
        bullet.add_velocity(Vector(1500))
        bullet_handler.add_bullet(bullet)

    def assault(self, enemy, ship):
        if enemy.does_collide_with(ship):
            self.assault = True
        if EnemyBullet.does_collide_with(ship):
            self.assault = True

    def get_lives_lost(self, ship):
        if self.assault:
            self.lives = self.lives - 1
            self.assault = False
        if self.lives <= 0:
            pygame.quit()
            quit(0)
        return self.lives

    def check_enemy_collision(self, enemy_handler):
        for enemy in enemy_handler.get_enemies():
            if enemy.does_collide_with(self):
                enemy.should_delete = True
                self.assault = True
                return True
        return False


class Star(Sprite):
    MIN_SPEED = 60
    MAX_SPEED = 250
    MIN_WIDTH = 20
    MAX_WIDTH = 32

    def __init__(self, position, velocity):
        v_scale = (velocity - Star.MIN_SPEED) / (Star.MAX_SPEED - Star.MIN_SPEED)
        w_scale = (Star.MAX_WIDTH - Star.MIN_WIDTH) * v_scale
        width = Star.MIN_WIDTH + w_scale
        size = Vector(width, 5)

        Sprite.__init__(self, position, Vector(40, width))
        image = pygame.image.load("assets/images/fish1.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)
        self.add_velocity(Vector(velocity * -1))


class StarHandler(UIElement):
    def add_stars(self, amount, outside_bounds=True):
        for count in range(amount):
            y = randint(0, self._size.y)
            if outside_bounds:
                x = self._size.x + 20
            else:
                x = randint(0, self._size.x)
            velocity = randint(Star.MIN_SPEED, Star.MAX_SPEED)
            self.__stars.append(Star(Vector(x, y), velocity))

    def __init__(self, size, density):
        UIElement.__init__(self, Vector(), size)
        self.__density = density
        self.__stars = []
        self.add_stars(density, False)

    def render(self, brush: UIBrush):
        for star in self.__stars:
            star.render(brush)

    def update(self, delta_time: float):
        for star in self.__stars:
            star.update(delta_time)
            self.__stars[:] = [star for star in self.__stars if star.get_position().x > 0]
            difference = self.__density - len(self.__stars)
            self.add_stars(difference)


class Background(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(1280, 720))
        image = pygame.image.load("assets/images/ocean.jpg")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class Shipwreck(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(787.5, 472.5))
        image = pygame.image.load("assets/images/shipwreck.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class Seaweed(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(218.25, 405))
        image = pygame.image.load("assets/images/seaweed.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class Sebastian(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector(75, 85))
        image = pygame.image.load("assets/images/sebastian10.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class SquidwardHouse(Sprite):
    def __init__(self, position):
        Sprite.__init__(self, position, Vector((355 / 1.5), (629 / 1.5)))
        image = pygame.image.load("assets/images/pin.png")
        brush = UIBrush(self._surface)
        brush.draw_image((0.5, 0.5), (1, 1), image, scaled_mode=True)


class DifficultyBackground:
    def __init__(self, position):
        self.position = position
        self.image = pygame.image.load("assets/images/reef.jpeg")

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def render(self, brush):
        pass



