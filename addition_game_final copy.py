from platform import machine
import time
import pygame
import os
import random
import sys
def game_play():
    pygame.init()
    pygame.mixer.init()
    FPS = 60
    WIDTH = 500
    HEIGHT = 600
    BACKGROUND_COLOR = (0,0,0)
    GREEN = (0,255,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)         
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("第一個遊戲")
    #載入圖片
    background_img = pygame.image.load(os.path.join("img","background.png")).convert()
    player_img = pygame.image.load(os.path.join("img","player.png")).convert()
    player_mini_img = pygame.transform.scale(player_img,(25,19))
    player_mini_img.set_colorkey(BLACK)
    #rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
    bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
    rock_imgs = []
    for i in range(7):
        rock_imgs.append(pygame.image.load(os.path.join("img","rock%d.png"%i)).convert())

    explode_annimation = dict()
    explode_annimation["lg"] = []
    explode_annimation["sm"] = []
    explode_annimation["player"] = []

    for j in range(9):
        explode_img = pygame.image.load(os.path.join("img","expl%d.png"%j)).convert()
        explode_img.set_colorkey(BLACK)
        explode_annimation["lg"].append(pygame.transform.scale(explode_img,(75,75)))
        explode_annimation["sm"].append(pygame.transform.scale(explode_img,(30,30)))
        player_expl_img = pygame.image.load(os.path.join("img","player_expl%d.png"%j)).convert()
        player_expl_img.set_colorkey(BLACK)
        explode_annimation["player"].append(player_expl_img)
    power_imgs = dict()
    power_imgs["shield"] = pygame.image.load(os.path.join("img","shield.png")).convert()
    power_imgs["gun"] = pygame.image.load(os.path.join("img","gun.png")).convert()
    #載入音樂
    shoot_sound1 = pygame.mixer.Sound(os.path.join("sound","shoot1.wav"))
    shoot_sound2 = pygame.mixer.Sound(os.path.join("sound","shoot2.wav"))
    gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
    shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
    expl_sounds = [
        pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
        pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
    ]
    pygame.mixer.music.load(os.path.join("sound","background.ogg"))
    pygame.mixer.music.set_volume(0.5)
    die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
    #載入字體
    font_name = os.path.join("font.ttf")

    def draw_text(surf,text,size,x,y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text,True,WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface,text_rect)

    def new_rock():
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)
        
    def draw_health(surf,hp,x,y):
        if hp < 0:
            hp = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp/100)*BAR_LENGTH
        outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
        fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
        pygame.draw.rect(surf,GREEN,fill_rect)
        pygame.draw.rect(surf,WHITE,outline_rect,2)

    def draw_lives(surf,lives,img,x,y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x+30*i
            img_rect.y = y
            surf.blit(img,img_rect)

    def draw_init():
        screen.blit(background_img,(0,0))
        draw_text(screen,"太空生存戰",64,WIDTH/2,HEIGHT/4)
        draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
        draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False
    class Player1(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = player_img
            self.image = pygame.transform.scale(player_img,(50,38))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 20
            #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
            self.rect.centerx = WIDTH/1.25
            self.rect.bottom = HEIGHT - 10
            self.speedx = 4
            self.health = 100
            self.lives = 3
            self.hidden = False
            self.hide_time = 0
            self.gun = 1
            self.gun_time = 0
        def update(self):
            now = pygame.time.get_ticks()
            if self.gun > 1 and now - self.gun_time > 8000:
                self.gun -= 1
            if self.hidden and pygame.time.get_ticks() - self.hide_time > 500:
                self.hidden = False
                self.rect.centerx = WIDTH/1.25
                self.rect.bottom = HEIGHT - 10
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += self.speedx
            elif key_pressed[pygame.K_LEFT]:
                self.rect.x -= self.speedx
            elif key_pressed[pygame.K_UP]:
                self.rect.y -= self.speedx
            elif key_pressed[pygame.K_DOWN]:
                self.rect.y += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            elif self.rect.top < 0:
                self.rect.top = 0

        def shoot1(self):
            if not(self.hidden):
                if self.gun == 1:
                    bullet = Bullet1(self.rect.centerx,self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound1.play()
                elif self.gun >= 2:
                    bullet1 = Bullet1(self.rect.left,self.rect.centery)
                    bullet2 = Bullet1(self.rect.right,self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound1.play()

        
        def hide(self):
            self.hidden = True
            self.hide_time = pygame.time.get_ticks()
            self.rect.center = (WIDTH/1.25,HEIGHT+500)
        def gunup(self):
            self.gun += 1
            self.gun_time = pygame.time.get_ticks()

    class Player2(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img,(50,38)) 
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 20
            #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
            self.rect.centerx = WIDTH/4
            self.rect.bottom = HEIGHT - 10
            self.speedx = 4
            self.health = 100
            self.lives = 3
            self.hidden = False
            self.hide_time = 0
            self.gun = 1
            self.gun_time = 0
        def update(self):
            now = pygame.time.get_ticks()
            if self.gun > 1 and now - self.gun_time > 8000:
                self.gun -= 1
            if self.hidden and pygame.time.get_ticks() - self.hide_time > 500:
                self.hidden = False
                self.rect.centerx = WIDTH/4
                self.rect.bottom = HEIGHT - 10
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_d]:
                self.rect.x += self.speedx
            elif key_pressed[pygame.K_a]:
                self.rect.x -= self.speedx
            elif key_pressed[pygame.K_w]:
                self.rect.y -= self.speedx
            elif key_pressed[pygame.K_s]:
                self.rect.y += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            elif self.rect.top < 0:
                self.rect.top = 0

        def shoot2(self):
            if not(self.hidden):
                if self.gun == 1:
                    bullet = Bullet2(self.rect.centerx,self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound1.play()
                elif self.gun >= 2:
                    bullet3 = Bullet2(self.rect.left,self.rect.centery)
                    bullet4 = Bullet2(self.rect.right,self.rect.centery)
                    all_sprites.add(bullet3)
                    all_sprites.add(bullet4)
                    bullets.add(bullet3)
                    bullets.add(bullet4)
                    shoot_sound1.play()
            
        def hide(self):
            self.hidden = True
            self.hide_time = pygame.time.get_ticks()
            self.rect.center = (WIDTH/4,HEIGHT+500)
        def gunup(self):
            self.gun += 1
            self.gun_time = pygame.time.get_ticks()

    class Rock(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image_ori = random.choice(rock_imgs)
            self.image_ori.set_colorkey(BLACK)
            self.image = self.image_ori.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * 0.825 / 2)
            #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-180,-100)
            self.speedy = random.randrange(1,5)
            self.speedx = random.randrange(-1,1)
            self.total_degree = 0
            self.rot_degree = random.randrange(-3,3)
        def rotate(self):
            self.total_degree += self.rot_degree
            self.total_degree = self.total_degree % 360
            self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
        def update(self):
            self.rotate()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
                self.rect.x = random.randrange(0,WIDTH-self.rect.width)
                self.rect.y = random.randrange(-100,-40)
                self.speedy = random.randrange(1,3)
                self.speedx = random.randrange(-1,1)
        
            
    class Bullet1(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10
            
        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Bullet2(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10
            
        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Explosion(pygame.sprite.Sprite):
        def __init__(self,center,size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = explode_annimation[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50
            
        def update(self):
            now = pygame.time.get_ticks()
            if (now - self.last_update) > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explode_annimation[self.size]):
                    self.kill()
                else:
                    self.image = explode_annimation[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    class Power(pygame.sprite.Sprite):
        def __init__(self,center):
            pygame.sprite.Sprite.__init__(self)
            self.type = random.choice(["shield","gun"])
            self.image = power_imgs[self.type]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 3
            
        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.kill()
    start_time = time.process_time()
    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player1 = Player1()
    player2 = Player2()
    powers = pygame.sprite.Group()
    all_sprites.add(player1,player2)
    # for i in range(8):
    #     new_rock()
    pygame.mixer.music.play(-1)    
    score = 0
    running = True
    show_init = True
    while running:
        if show_init:
            close = draw_init()
            if close:
                break
            show_init =False
            all_sprites = pygame.sprite.Group()
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player1 = Player1()
            player2 = Player2()
            powers = pygame.sprite.Group()
            all_sprites.add(player1,player2)
            for i in range(8):
                new_rock()
            pygame.mixer.music.play(-1)    
            score = 0       
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    player1.shoot1()
                if event.key == pygame.K_SPACE:
                    player2.shoot2()

        #更新遊戲
        all_sprites.update()
        hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
        for hit in hits:
            random.choice(expl_sounds).play()
            score += hit.radius
            expl = Explosion(hit.rect.center,"lg")
            all_sprites.add(expl)
            if random.random() < 0.05: #寶物機率
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
            new_rock()
        #判斷寶物相撞
        hits1 = pygame.sprite.spritecollide(player1,powers,True)
        for hit1 in hits1:
            if hit1.type == "shield":
                shield_sound.play()
                player1.health += 20
                if player1.health > 100:
                    player1.health = 100
            elif hit1.type == "gun":
                player1.gunup()
                gun_sound.play()
        hits2 = pygame.sprite.spritecollide(player2,powers,True)
        for hit2 in hits2:
            if hit2.type == "shield":
                shield_sound.play()
                player2.health += 20
                if player2.health > 100:
                    player2.health = 100
            elif hit2.type == "gun":
                player2.gunup()
                gun_sound.play()
        hits1 = pygame.sprite.spritecollide(player1,rocks,True,pygame.sprite.collide_circle)
        for hit1 in hits1:
            new_rock()
            player1.health -= hit1.radius*5
            expl = Explosion(hit1.rect.center,"sm")
            all_sprites.add(expl)
            if player1.health <= 0:
                death_expl = Explosion(player1.rect.center,"player")
                all_sprites.add(death_expl)
                die_sound.play()
                #running = False 
                player1.lives -= 1
                player1.health = 100
                player1.hide()
        
        hits2 = pygame.sprite.spritecollide(player2,rocks,True,pygame.sprite.collide_circle)
        for hit2 in hits2:
            new_rock()
            player2.health -= hit2.radius*5
            expl = Explosion(hit2.rect.center,"sm")
            all_sprites.add(expl)
            if player2.health <= 0:
                death_expl = Explosion(player2.rect.center,"player")
                all_sprites.add(death_expl)
                die_sound.play()
                #running = False 
                player2.lives -= 1
                player2.health = 100
                player2.hide()
        if player1.lives == 0 or player2.lives == 0:
            pygame.quit()
            
        elif player1.lives == 0 and not(death_expl.alive()):
            show_init = False    
        elif player2.lives == 0 and not(death_expl.alive()):
            show_init = False
        
        #畫面顯示        
        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_img,(0,0))
        all_sprites.draw(screen)
        draw_text(screen,str(score),18,WIDTH/2,10)
        draw_health(screen,player1.health,5,15)
        draw_health(screen,player2.health,5,35)
        draw_lives(screen,player1.lives,player_mini_img,WIDTH - 100,15)
        draw_lives(screen,player2.lives,player_mini_img,WIDTH - 100,35)
        pygame.display.update()
    
    end = time.process_time()
    if end-start_time >= 20:
        pygame.quit()
    

def annimation(x=10,y=0.2):
    for i in range(1,x):
        time.sleep(y)
        print((x-i)*" "+"* "*i)
def digit_conditions():
    try:#小朋友有時別出心裁，會亂輸入，故一開始就讓他TRY
        while True:#輸入5+5=某數，如錯誤請更正直到正確的答案，ex 5+5=100 直到輸入１０
            n1,n2 = input().split("+")#利用+號來SPLIT輸入，ex:5+5=10 得5和5=10
            n3 = n2.split("=")#利用=號來SPLIT，得到答案，ex:5=10 得10
            if int(n1)+int(n3[0]) == int(n3[1]):#如果5+5=10正確，關閉迴圈並呼叫動畫和遊戲函式
                annimation()
                game_play()
                print("%d+%d=%d"%(int(n1),int(n3[0]),int(n3[1])))
                break
            else:
                print("%d+%d=?"%(int(n1),int(n3[0])))    
                n = int(input())
                if n == int(n3[0])+int(n1):
                    annimation()
                    game_play()
                    print("%d+%d=%d"%(int(n1),int(n3[0]),n))
                    break
                else:
                    print("%d+%d=?"%(int(n1),int(n3[0])))    
                    n = int(input())
                    if n == int(n1)+int(n3[0]):
                        annimation()
                        game_play()
                        print("%d+%d=%d"%(int(n1),int(n3[0]),n))
                        break
                    else:
                        print("%d+%d=?"%(int(n1),int(n3[0])))
                        while True:
                            n = int(input())
                            if n == int(n1)+int(n3[0]):
                                annimation()
                                game_play()
                                print("%d+%d=%d congrats"%(int(n1),int(n3[0]),n))
                                break
                            else:
                                print("%d+%d=?"%(int(n1),int(n3[0])))
                        break
    
    except ValueError:
        print("type error,please type again the equation")
        digit_conditions()  
    except IndexError:
        print("type error,please type again the equation")
        digit_conditions()  
  

digit_conditions()
#os.system('python "C:\\Users\\kevin\\OneDrive\\桌面\pygame\\addition_game_final copy.py"')

   # "C:\Users\kevin\OneDrive\桌面\pygame\addition_game_final copy.py"