from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
 
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self): 
        if ball.rect.x <= screen_width-80 and ball.x_speed > 0 or ball.rect.x >= 0 and ball.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) 
        if ball.rect.y <= screen_height-80 and ball.y_speed > 0 or ball.rect.y >= 0 and ball.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0

                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

screen_width = 700
screen_height = 500
display.set_caption("maze")
screen = display.set_mode((screen_width, screen_height))
back = (119, 210, 223)

bg = transform.scale(image.load("bg.jpg"), (screen_width, screen_height))
barriers = sprite.Group()

w1 = GameSprite('wall.png',screen_width/2 - screen_width/3, screen_height/2, 300, 50)
w2 = GameSprite('wall_w.png', 370, 100, 50, 400)

barriers.add(w1)
barriers.add(w2)

ball = Player('ball.png', 5, screen_height - 80, 80, 80, 0, 0)
hole = GameSprite('hole.png', screen_width - 80, 180, 80, 80)
final_sprite = GameSprite('kegla.png', screen_width - 85, screen_height - 100, 80, 80)

finish = False
run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                ball.x_speed = -5
            elif e.key == K_RIGHT:
                ball.x_speed = 5
            elif e.key == K_UP :
                ball.y_speed = -5
            elif e.key == K_DOWN :
                ball.y_speed = 5
 
        elif e.type == KEYUP:
            if e.key == K_LEFT :
                ball.x_speed = 0
            elif e.key == K_RIGHT:
                ball.x_speed = 0
            elif e.key == K_UP:
                ball.y_speed = 0
            elif e.key == K_DOWN:
                ball.y_speed = 0
    if not finish:
        screen.blit(bg,(0,0))
        barriers.draw(screen)
    
    hole.reset()
    final_sprite.reset()
    ball.reset()
    ball.update()
    if sprite.collide_rect(ball, hole):
        finish = True
        img = image.load('gg.png')
        d = img.get_width() // img.get_height()
        screen.fill((255, 255, 255))
        screen.blit(transform.scale(img, (screen_height * d, screen_height)), (90, 0))

    if sprite.collide_rect(ball, final_sprite):
        finish = True
        img = image.load('strike.png')
        screen.fill((255, 255, 255))
        screen.blit(transform.scale(img, (screen_width, screen_height)), (0, 0))
    time.delay(50)
    display.update()