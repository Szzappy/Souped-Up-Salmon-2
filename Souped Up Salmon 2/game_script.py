from pygame import mixer
from sprite_library import *
from pygame.sysfont import SysFont


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


class Button:
    def __init__(self, position, size, colour, hover_colour, text, difficulty, callback):
        self.position = position
        self.size = size
        self.colour = colour
        self.hover_colour = hover_colour
        self.text = text
        self.difficulty = difficulty
        self.callback = callback
        self.font = pygame.font.SysFont("comic sans", 45)
        self.hovering = False

    def draw(self, surface):
        if self.hovering:
            pygame.draw.rect(surface, self.hover_colour, (self.position[0],
                                                          self.position[1], self.size[0], self.size[1]))
        else:
            pygame.draw.rect(surface, self.colour, (self.position[0], self.position[1], self.size[0], self.size[1]))

        label = self.font.render(self.text, 30, (40, 180, 250))
        surface.blit(label, self.position)

    def is_mouse_hovering(self, mouse_x, mouse_y):
        return(self.position[0] <= mouse_x <= self.position[0] + self.size[0]
               and self.position[1] <= mouse_y <= self.position[1] + self.size[1])

    def click(self):
        self.callback()

        if too_easy.click():
            EnemyHandler.difficulty = 5
            mixer.music.pause()
            play_game1()

        elif easy.click():
            EnemyHandler.difficulty = 10
            mixer.music.pause()
            play_game2()

        elif medium.click():
            EnemyHandler.difficulty = 20
            mixer.music.pause()
            play_game3()

        elif hard.click():
            EnemyHandler.difficulty = 36
            mixer.music.pause()
            play_game4()

        elif very_hard.click():
            EnemyHandler.difficulty = 54
            mixer.music.pause()
            play_game5()

        elif funny.click():
            EnemyHandler.difficulty = 220
            mixer.music.pause()
            play_game6()


def play_game1():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 5)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/Come_And_Get_Your_Love1.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game2():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 12)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/_78_la-mer_charles-trenet-albert-lasry_gbia0022192a_01_3.5_ET_EQ.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game3():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 24)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/Pirates of the Caribbean - Hes a Pirate.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game4():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 36)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/Bobby-Darin-Beyond-the-Sea.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game5():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 56)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/Under The Sea.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game6():

    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), 200)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/Ocean Man.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


def play_game7():
    x = randint(1, 250)
    print(x)
    while True:
        window2 = UIWindow(Vector(1280, 720), "Souped-up Salmon 2")
        brush = window2.get_brush()

        ship = Ship(Vector(100, 140))
        enemy_handler = EnemyHandler(Vector(1000, 500), x)
        bullet_handler = BulletHandler(Vector(1280, 720))
        star_handler = StarHandler(Vector(1280, 720), 7)
        background2 = Background(Vector(640, 360))
        shipwreck = Shipwreck(Vector(900, 483.75))
        seaweed1 = Seaweed(Vector(100, 517.5))
        seaweed2 = Seaweed(Vector(550, 517.5))
        seaweed3 = Seaweed(Vector(300, 517.5))
        seaweed4 = Seaweed(Vector(425, 517.5))
        sebastian = Sebastian(Vector(690, 360))
        squidward_house = SquidwardHouse(Vector(300, (720 - (629 / 1.5) + 225)))
        # to calculate the position, take your x/y value and divide it by 2 and then do 1280(x) or 720(y) - your value

        score = 0
        score_label = HUDLabel(Vector(100, 50), Vector(150, 100), "Score: 0", SysFont("comic sans", 256),
                               (255, 255, 255))

        lives_label = HUDLabel(Vector(300, 50), Vector(150, 100), "Lives: 5", SysFont("comic sans", 256),
                               (255, 255, 255))

        pygame.mixer.music.load('assets/music/SmashMouth-AllStar.mp3')
        pygame.mixer.music.play(loops=-1)

        while True:
            delta_time = window2.wait() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(-450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_SPACE:
                        ship.fire(bullet_handler)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        ship.add_velocity(Vector(0, 400))
                    elif event.key == pygame.K_a:
                        ship.add_velocity(Vector(450))
                    elif event.key == pygame.K_s:
                        ship.add_velocity(Vector(0, -400))
                    elif event.key == pygame.K_d:
                        ship.add_velocity(Vector(-450))

            ship.update(delta_time)
            bullet_handler.update(delta_time)
            enemy_handler.update(delta_time)
            bullet_handler.check_collisions(enemy_handler)
            star_handler.update(delta_time)

            score += enemy_handler.get_enemy_destroyed()
            score_label.set_text("Score: " + str(score))
            score_label.update_appearance()

            if ship.check_enemy_collision(enemy_handler):
                lives = ship.get_lives_lost(ship)
                lives_label.set_text("Lives: " + str(lives))
                lives_label.update_appearance()

            window2.clear()

            background2.render(brush)
            score_label.render(brush)
            lives_label.render(brush)
            sebastian.render(brush)
            seaweed1.render(brush)
            seaweed2.render(brush)
            seaweed3.render(brush)
            seaweed4.render(brush)
            squidward_house.render(brush)
            enemy_handler.render(brush)
            bullet_handler.render(brush)
            star_handler.render(brush)
            ship.render(brush)
            shipwreck.render(brush)

            print("You achieved a score of: " + str(score))

            window2.show_frame()


window = pygame.display.set_mode((800, 600))
current_state = 0

too_easy = Button((0, 100), (140, 35), (0, 150, 0), (0, 0, 0), "Too Easy", 5, play_game1)
easy = Button((0, 150), (80, 35), (0, 250, 0), (0, 0, 0), "Easy", 10,  play_game2)
medium = Button((0, 200), (115, 35), (220, 255, 10), (0, 0, 0), "Medium", 20, play_game3)
hard = Button((0, 250), (80, 35), (220, 0, 0), (0, 0, 0), "Hard", 36, play_game4)
very_hard = Button((0, 300), (150, 35), (160, 0, 0), (0, 0, 0), "Very Hard", 54,  play_game5)
funny = Button((0, 350), (140, 35), (100, 0, 0), (0, 0, 0), "F U N N Y", 220, play_game6)
random = Button((0, 400), (120, 35), (255, 255, 255), (0, 0, 0), "Random", 100, play_game7)


title_label = Button((0, 0), (140, 35), (0, 0, 0), (0, 0, 0), "Difficulty", 0,  None)
background = DifficultyBackground((0, 0))
buttons = [too_easy, easy, medium, hard, very_hard, funny, random]


def dif_get_input():
    if current_state == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_button = None

        for button in buttons:
            button.hovering = button.is_mouse_hovering(mouse_x, mouse_y)
            if button.hovering:
                hovered_button = button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == pygame.BUTTON_LEFT:
                    if hovered_button:
                        hovered_button.click()


def dif_update():
    if current_state == 0:
        pass


def dif_render():
    if current_state == 0:
        background.draw(window)

        too_easy.draw(window)
        easy.draw(window)
        medium.draw(window)
        hard.draw(window)
        very_hard.draw(window)
        funny.draw(window)
        random.draw(window)

        title_label.draw(window)
    pygame.display.flip()
    pygame.mixer.pause()


pygame.mixer.music.load('assets/music/Come_And_Get_Your_Love1.mp3')
pygame.mixer.music.play(loops=-1)
while True:
    dif_get_input()
    dif_update()
    dif_render()
