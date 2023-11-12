from pygame import *
init()
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(sprite_image), (WIDTH // 19, HEIGHT // 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "right"

    def reset(self):
        if self.direction == "right":
            window.blit(self.image, (self.rect.x, self.rect.y))
        else:
            window.blit(transform.flip(self.image, True, False), (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.direction = "left"
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - self.rect.width:
            self.direction = "right"
            self.rect.x += self.speed


class Enemy(GameSprite):
    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.x <= int(WIDTH / 1.4):
            self.direction = "right"
        if self.rect.x >= WIDTH - WIDTH // 20:
            self.direction = "left"


class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, color=(84, 182, 92)):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


info = display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
FPS = 60
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Лaбiринт")
background = transform.scale(image.load("images/background.jpg"), (WIDTH, HEIGHT))
clock = time.Clock()
mixer.music.load("sounds/jungles.ogg")
mixer.music.set_volume(0.3)
mixer.music.play()
kick = mixer.Sound("sounds/kick.ogg")
kick.set_volume(0.3)
money = mixer.Sound("sounds/money.ogg")
money.set_volume(0.3)
font_finish = font.Font(None, HEIGHT // 3)
text_win = font_finish.render("You WIN!", True, (206, 214, 92))
text_lose = font_finish.render("You LOSE!", True, (206, 100, 92))
text_pause = font_finish.render("Pause", True, (100, 100, 200))
player = Player("images/hero.png", WIDTH // 10, HEIGHT // 5, WIDTH // 150)
monster = Enemy("images/cyborg.png", WIDTH - WIDTH // 5, HEIGHT - HEIGHT // 3, WIDTH // 150)
treasure = GameSprite("images/treasure.png", WIDTH - WIDTH // 8, HEIGHT - HEIGHT // 5, 10)

wall_top = Wall(WIDTH // 20, HEIGHT // 20, WIDTH - WIDTH // 10, HEIGHT // 50)
wall_bottom = Wall(WIDTH // 20, HEIGHT - HEIGHT // 20, WIDTH - WIDTH // 10, HEIGHT // 50)
wall_1 = Wall(WIDTH // 5, HEIGHT // 20, HEIGHT // 50, HEIGHT - HEIGHT // 3)
wall_2 = Wall(int(WIDTH / 2.85), int(HEIGHT / 3.5), HEIGHT // 50, HEIGHT - HEIGHT // 3)
wall_3 = Wall(WIDTH // 2, HEIGHT // 20, HEIGHT // 50, HEIGHT - HEIGHT // 3)
wall_4 = Wall(int(WIDTH / 1.5), int(HEIGHT / 3.5), HEIGHT // 50, HEIGHT - HEIGHT // 3)
wall_5 = Wall(int(WIDTH / 1.5), int(HEIGHT / 3.5), WIDTH // 5, HEIGHT // 50)
game = True
pause = False
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_p:
                if not pause:
                    pause = True
                else:
                    pause = False
            if e.key == K_r:
                player.rect.x = WIDTH // 10
                player.rect.y = HEIGHT // 5
                finish = False
    if not finish:
        if not pause:
            window.blit(background, (0, 0))
            player.reset()
            player.update()

            monster.reset()
            monster.update()

            treasure.reset()

            wall_top.reset()
            wall_bottom.reset()

            wall_1.reset()
            wall_2.reset()
            wall_3.reset()
            wall_4.reset()
            wall_5.reset()

            if sprite.collide_rect(player, treasure):
                finish = True
                window.blit(text_win, (WIDTH // 4, HEIGHT // 3))
                money.play()

            if sprite.collide_rect(player, monster) \
                    or sprite.collide_rect(player, wall_top) \
                    or sprite.collide_rect(player, wall_bottom) \
                    or sprite.collide_rect(player, wall_1) \
                    or sprite.collide_rect(player, wall_2) \
                    or sprite.collide_rect(player, wall_3) \
                    or sprite.collide_rect(player, wall_4) \
                    or sprite.collide_rect(player, wall_5):

                finish = True
                window.blit(text_lose, (WIDTH // 5, HEIGHT // 3))
                kick.play()
        else:
            window.blit(text_pause, (WIDTH // 3, HEIGHT // 3))

        clock.tick(FPS)
        display.update()