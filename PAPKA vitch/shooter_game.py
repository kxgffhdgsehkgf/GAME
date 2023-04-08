#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_w, player_h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = player_w

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        win.blit(self.image, (self.rect.x, self.rect.y))
    


class Player(GameSprite):
    global num_fire
    def update(self):
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", player.rect.x+35, 385, 5, 10, 10)
        bullets.add(bullet)

            
        
        
        
    

class Enemy(GameSprite):
    def update(self):
        global propush
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(10, 630)
            self.rect.y =0
            propush += 1

    def bossupdate(self):
        self.rect.y += self.speed


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(10, 630)
            self.rect.y =0

sbito = 0
propush = 0

m = 0

canshoot = True

num_fire = 0
rel_time = 0

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

bulletsound = mixer.Sound("fire.ogg")
clock = time.Clock()
fps = 60

font.init()
font1 = font.Font(None, 50)
font2 = font.Font(None, 120)
font3 = font.Font(None, 50)

m = 0

n = 0

run = True

win = display.set_mode((700, 500))
display.set_caption(":)(●'◡'●):-):-)^_^ಥ_ಥ(┬┬﹏┬┬)☆*: .｡. o(≧▽≦)o .｡.:*☆")
bg = transform.scale(image.load("galaxy.jpg") , (700, 500))

player = Player("rocket.png", 330, 385, 8, 80, 100)

hp = GameSprite("hp.png", 10, 80, 0, 240, 50)

bullets = sprite.Group()
ufos = sprite.Group()
for i in range(5):
    ufo = Enemy("ufo.png", randint(1, 610), 10, randint(1, 2), 85, 55)
    ufos.add(ufo)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid("asteroid.png", randint(1, 610), 10, 2, 85, 55)
    asteroids.add(asteroid)
timme = timer()

finish = False
while run:
    for i in event.get():
        if i.type == QUIT:
            run = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE and canshoot == True:
                if finish != True:
                    if num_fire <= 7:
                        player.fire()
                        bulletsound.play()
                        num_fire += 1
                    else:
                        rel_time = True
                        start = timer()
                        canshoot = False

        keys = key.get_pressed()
        if keys[K_r]:
            finish = False
            for i in ufos:
                i.kill()
            for i in range(5):
                ufo = Enemy("ufo.png", randint(1, 610), 10, randint(1, 2), 85, 55)
                ufos.add(ufo)
            for i in asteroids:
                i.kill()
            for i in range(2):
                asteroid = Asteroid("asteroid.png", randint(1, 610), 10, 2, 85, 55)
                asteroids.add(asteroid)
            sbito = 0
            propush = 0
            player = Player("rocket.png", 330, 385, 8, 80, 100)
            for i in bullets:
                i.kill()
            m = 0
            num_fire = 0
            rel_time = False
            timme = timer()
            canshoot = True

    if finish != True:
        
        timmme = timer()

        sbitto = font1.render("Сбито: "+str(sbito), True, (255, 255, 255))
        propushh = font1.render("Пропущенно: "+str(propush), True, (255, 255, 255))
        win.blit(bg, (0, 0))

        if timmme - timme >= 4:
            if n == 0:
                da = GameSprite("da.png" , randint(1, 400), 200, 0, 200, 40)
                n = 1

        win.blit(sbitto, (10, 10))
        win.blit(propushh, (10, 50))

        asteroids.update()
        asteroids.draw(win)
        player.update()
        ufos.draw(win)
        ufos.update()

        if timmme - timme >= 4:
            da.reset()

        bullets.update()
        bullets.draw(win)

        player.reset()

        if sprite.groupcollide(bullets, ufos, True, True):
            ufo = Enemy("ufo.png", randint(1, 610), 10, randint(1, 2), 85, 55)
            ufos.add(ufo)
            sbito += 1

        if sprite.groupcollide(asteroids, bullets, False, True):
            a = 0

        if propush >= 3 or sprite.spritecollide(player, ufos, False):
            YouLose = font2.render("You Lose ", True, (255, 255, 255))
            win.blit(YouLose, (190, 210))
            finish = True
            mixer.music.stop()

        if timmme - timme >= 4:
            if sprite.spritecollide(da, bullets, False):
                num_fire = 0

        if propush >= 3 or sprite.spritecollide(player, asteroids, False):
            YouLose = font2.render("You Lose ", True, (255, 255, 255))
            win.blit(YouLose, (190, 210))
            finish = True
            mixer.music.stop()

        now_time = timer()

        if rel_time == True and now_time - start <= 3:
            reltext = font3.render("Wait, reload...  "+str(round(3- (now_time-start), 2)), True, (255, 0, 0))
            win.blit(reltext, (250, 460))
        elif rel_time == True and now_time - start >= 3:
            rel_time = False
            num_fire = 0
            canshoot = True
        if sbito >= 10:
            
            num_fire = 0

            timme = timer()
            timme = timme+100

            for i in asteroids:
                i.kill()
            
            if m != 1:
                for i in ufos:
                    i.kill()
                ufo = Enemy("ufo.png", randint(1, 540), 10, 1 , 185, 95)
                m = 1

            ufo.reset()
            ufo.bossupdate()

            if sprite.spritecollide(ufo, bullets, True):
                sbito +=1

            if sprite.collide_rect(ufo, player):
                YouLose = font2.render("You Lose ", True, (255, 255, 255))
                win.blit(YouLose, (190, 210))
                finish = True
                mixer.music.stop()
            
            if ufo.rect.y > 400:
                YouLose = font2.render("You Lose ", True, (255, 255, 255))
                win.blit(YouLose, (190, 210))
                finish = True
                mixer.music.stop()
            
            if sbito >= 30:
                YouWin = font2.render("You Win ", True, (255, 255, 255))
                win.blit(YouWin, (190, 210))
                finish = True
                mixer.music.stop()

            if sbito == 15:
                hp.width = 180

            if sbito == 20:
                hp.width = 120
            
            if sbito == 25:
                hp.width = 60
            
            if sbito == 29:
                hp.width = 0

    display.update()
    clock.tick(fps)     
