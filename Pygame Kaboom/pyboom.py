import pygame, threading, random, time
import sys
from pygctors import *
import tkinter
from tkinter import messagebox
pygame.init()
pygame.mixer.init()
mode = "title"
random.seed(round(time.time()))
width, height = 1200, 650
screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Kaboom 2")
gamescreen1 = pygame.Surface((5000, 5000))
viewport1 = pygame.Rect(0, 0, 800, height)
viewport2 = pygame.Rect(0, 0, 800, height / 2)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
font = pygame.font.SysFont(None, 50)
player = Actor([2500, 2500])
gun1 = Actor(player.pos, "images/gun.png")
player.z = 0
player.life = 100
player.ammo = 100
player2 = Actor([2550, 2550], "images/player2.png")
player2.z = 0
player2.life = 100
player2.ammo = 100
score = 0 #scoreeeeee   
lastscore = 0
fires = []
bullets = []
rounds = 1
sounds = [pygame.mixer.Sound("sounds/check.ogg"), pygame.mixer.Sound("sounds/dmg.wav"), pygame.mixer.Sound("sounds/shooa.wav"), pygame.mixer.Sound("sounds/recharge.ogg"), pygame.mixer.Sound("sounds/fireded.ogg"), pygame.mixer.Sound("sounds/rain.wav")]
def shoot(who, angle):
    if who.ammo > 0:
        bullet = Actor(who.pos.copy(), "images/wotor.png")
        bullet.angle = angle
        bullet.timer = 30
        bullet.pos[0] -= cos(radians(bullet.returnangle())) * -50
        bullet.pos[1] += sin(radians(bullet.returnangle())) * -50
        bullets.append(bullet)
        who.ammo -= 2
        sounds[2].play()

def bulletlogic():
    global score
    for i in range(len(bullets) -1, -1, -1 ):
        if len(fires) > 0:
            if bullets[i].collidelistA(fires) != -1:
                fires_i = bullets[i].collidelistA(fires)
                fires[fires_i].life -= 1
                if fires[fires_i].life <= 0:
                    fires.pop(fires_i)
                    sounds[4].play()
                    score += 100
                bullets.pop(i)
                break
        bullets[i].timer -= 1
        bullets[i].pos[0] -= cos(radians(bullets[i].returnangle())) * -10
        bullets[i].pos[1] += sin(radians(bullets[i].returnangle())) * -10
        if bullets[i].timer <= 0:
            bullets.pop(i)

firetypes = ["still", "moving", "flying", "stiller", "faster", "camoflage", "strong", "camoflage2"]
joysticksensor = [Actor([0, 0]), Actor([0, 0])]
if pygame.joystick.get_count() > 0:  joystick = pygame.joystick.Joystick(0)
collision_sound = pygame.mixer.Sound("sounds/dmg.wav")
collision_occurred = False
clock = pygame.time.Clock()
pygame.mixer.music.load("music/title.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)
def show_error():
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showerror("Error", "No hay mando conectado, por favor conecta un mando y reinicia el juego. (el ok no cierra la ventanita usa la X)")
    root.destroy()
def playmaintheme():
    pygame.mixer.music.load("music/game.wav")
    pygame.mixer.music.play(-1)
MUSIC_PLAY = pygame.USEREVENT + 1
players1button = pygame.Rect(700, 400, 200, 50)
players2button = pygame.Rect(700, 500, 200, 50)
heightimages = [pygame.image.load("images/placeholder.png"), pygame.image.load("images/placeholder2.png"), pygame.image.load("images/cursor.png"), pygame.image.load("images/life.png"), pygame.image.load("images/wotor.png")]
heightimages[2] = pygame.transform.scale(heightimages[2], (200, 200))
steps = []
var = 0
timer = 0 
lastpos = [2700, 2500, 1]
steps.append(Actor([lastpos[0], lastpos[1]], "images/step.png"))
steps[0].z = lastpos[2]
for o in range(1):
    i = len(steps) - 1
    steps.append(Actor([random.choice((100, -100)) +  lastpos[0], random.choice((100, -100)) +  lastpos[1]], "images/step.png"))
    while True:
        if steps[i + 1].collidelistA(steps) != -1:
            steps[i + 1].pos = [random.choice((100, -100)) + lastpos[0], random.choice((100, -100)) + lastpos[1]]
        else:  
            break
    steps[i + 1].z = lastpos[2] + random.choice((-1, 0, 1))
    lastpos[0] = steps[i + 1].pos[0]
    lastpos[1] = steps[i + 1].pos[1]
    lastpos[2] = steps[i + 1].z
        

    steps[i].z 
cursor = Actor([0, 0], "images/cursor.png")
cursor.original_image.set_alpha(125)
relcursor = Actor([0, 0])
rects = [pygame.Rect(800, 0, 400, height / 2), pygame.Rect(800, height / 2, 400, height / 2)]
def addfires(amount):
    for i in range(amount):
        fire = Actor([random.randint(1900, 3100), random.randint(1900, 3100)], "images/s0.png")
        fire.frames = [pygame.image.load("images/s0.png"), pygame.image.load("images/s2.png")]
        fire.tipe = random.choice(firetypes)
        fire.timer = 0
        fire.z = 0
        fire.life = 2
        fires.append(fire)
    for ii in range(len(fires)):
        for i in range(len(fire.frames)):
            if fires[ii].tipe == "stiller" or fires[ii].tipe == "strong":
                fires[ii].frames[i] = pygame.transform.scale(fires[ii].frames[i], (75, 75))
                fires[ii].life = 5
            if fires[ii].tipe == "faster":
                fires[ii].life = 1
        fires[ii].image = fires[ii].frames[0]
addfires(3)
def draw():
    global var, timer, lastscore
    timer += 1 / 60
    a = pygame.mouse.get_pos()
    cursor.pos = (a[0] - 25, a[1] - 25)
    relcursor.pos = (viewport1.topleft[0] + cursor.pos[0], viewport1.topleft[1] + cursor.pos[1])
    gun1.changecenter(player.returncenter())
    if mode != 'title':
        screen.fill("lightgray")
        gamescreen1.fill("gray")
        for i in range(len(steps)):
            if steps[i].colliderect(viewport1) or steps[i].colliderect(viewport2):
                steps[i].draw(gamescreen1)
        for i in range(len(fires)):
            if fires[i].colliderect(viewport1) or fires[i].colliderect(viewport2):
                fires[i].draw(gamescreen1)
                if fires[i].tipe == "camoflage":
                    gamescreen1.blit(player.image, fires[i].pos)
                elif fires[i].tipe == "camoflage2":
                    gamescreen1.blit(player2.image, fires[i].pos)
        if timer > .05:
            var = (var + 1) % 2
            for i in range(len(fires)):
                lvar = var
                fires[i].image = fires[i].frames[lvar]
                timer = 0
        for i in range(len(bullets)):
            if bullets[i].colliderect(viewport1) or bullets[i].colliderect(viewport2):
                bullets[i].draw(gamescreen1)

    if mode == 'game':
        screen.blit(heightimages[0], (800, 200))
        player2.pos = player.pos.copy()
        cursor.angle = ((degrees(atan2(400 - a[0], 325 - a[1])) + 90) % 360) + 180
        pygame.draw.rect(screen, "darkgray", pygame.Rect(800, 400, 200, 650))
        step_index = relcursor.collidelistA(steps)
        if step_index != -1:
            z_value = steps[step_index].z
        else:
            z_value = 0
        pygame.draw.rect(
            screen,
            (64, 64, 64),
            pygame.Rect(1000, 400 + ((player.z - z_value)  * 100), 200, 1000)
        )
        screen.blit(heightimages[2], (1000, 200 + ((player.z - z_value) * 100)))
        player.draw(gamescreen1)
        gun1.angle = player.angle_to(relcursor) + 180
        gun1.draw(gamescreen1)
        pygame.draw.rect(screen, "black", pygame.Rect(800, 0, 10, 650))
        viewport1.center = player.center
        screen.blit(gamescreen1, (0, 0), viewport1)
        cursor.draw(screen)
        text1 = font.render(str(player.life), True, "black")
        screen.blit(text1, (50, 10))
        screen.blit(heightimages[3], (0, 0))
        text1 = font.render(str(player.ammo), True, "black")
        screen.blit(text1, (50, 60))
        screen.blit(heightimages[4], (0, 50))
        if score == lastscore:
            text1= font.render(str(score), True, "black")
        else:
            lastscore = score
            text1 = font.render(str(score), True, "yellow")
        screen.blit(text1, (1000, 0))
    if mode == 'game2':
        
        screen.blit(heightimages[0], (800, 0))
        pygame.draw.rect(screen, "darkgray", pygame.Rect(800, 200, 200, 125))
        cursor.angle = ((degrees(atan2(400 - a[0], 162.5 - a[1])) + 90) % 360) + 180
        step_index = relcursor.collidelistA(steps)
        if step_index != -1:
            z_value = steps[step_index].z
        else:
            z_value = 0
        pygame.draw.rect(
            screen,
            (64, 64, 64),
            pygame.Rect(1000, 400 + ((player.z - z_value)  * 100), 200, 1000)
        )
        screen.blit(heightimages[2], (1000, 200 + ((player.z - z_value) * 100)))
        player.draw(gamescreen1)
        player2.draw(gamescreen1)
        gun1.angle = player.angle_to(relcursor) + 180
        gun1.draw(gamescreen1)
        pygame.draw.rect(screen, "black", pygame.Rect(800, 0, 10, 650))
        viewport1.center = player.center


        viewport2.center = player2.center
        screen.blit(gamescreen1, (0, 0), viewport1)
        screen.blit(gamescreen1, (0, height / 2), viewport2)
        pygame.draw.rect(screen, "black", pygame.Rect(0, height / 2, 1200, 5))
        cursor.draw(screen)
        text1 = font.render(str(player.life), True, "black")
        screen.blit(text1, (50, 10))
        screen.blit(heightimages[3], (0, 0))
        text1 = font.render(str(player.ammo), True, "black")
        screen.blit(text1, (50, 60))
        screen.blit(heightimages[4], (0, 50))

    elif mode == 'title':
        title_screen = pygame.image.load("images/title.png")
        screen.blit(title_screen, (0, 0))
        pygame.draw.rect(screen, 'black', players1button)
        pygame.draw.rect(screen, 'black', players2button)
        text1 = font.render('1 player', True, 'white')
        text2 = font.render('2 players', True, 'white')
        screen.blit(text1, (players1button.x + 25, players1button.y + 10))
        screen.blit(text2, (players2button.x + 25, players2button.y + 10))

target = Actor([0, 0])
player_speed = 5
def firelogic():
    global mode
    for i in range(len(fires)):
        if mode == "game":
            target.pos = player.pos.copy()
        elif mode == "game2":
            if fires[i].distance_to_actor(player2) < fires[i].distance_to_actor(player):
                target.pos = player2.pos.copy()
            else:
                target.pos = player.pos.copy()
        lastpos = fires[i].pos.copy()
        if fires[i].tipe == "still" or fires[i].tipe == "strong":
            fires[i].timer += 1 / 60
            if fires[i].timer > 5:
                fires[i].timer = 0
                fire = Actor(fires[i].pos.copy(), "images/s0.png")
                fire.frames = [pygame.image.load("images/s0.png"), pygame.image.load("images/s2.png")]
                fire.tipe = "moving"
                fire.timer = 0
                fire.z = fires[i].z
                fire.life = 2
                fires.append(fire)
        if fires[i].tipe == "stiller":
            fires[i].timer += 1 / 60
            if fires[i].timer > 5:
                fires[i].timer = 0
                for o in range(3):
                    fire = Actor([fires[i].pos[0] + random.randint(-50, 50), fires[i].pos[1] + random.randint(-50, 50)], "images/s0.png")
                    fire.frames = [pygame.image.load("images/s0.png"), pygame.image.load("images/s2.png")]
                    fire.tipe = random.choice(["faster", "moving", "flying", "camoflage", "camoflage2"])
                    fire.timer = 0
                    fire.z = 0
                    fire.life = 2
                    if fire.tipe == "faster":
                        fire.life = 1
                    fires.append(fire)
        if fires[i].collidelistA(steps) == -1 and fires[i].tipe == "moving" or fires[i].tipe == "strong" or fires[i].tipe == "camoflage" or fires[i].tipe == "camoflage2":
            fires[i].pos[0] -= cos(radians(fires[i].angle_to(target))) * -3
            fires[i].pos[1] += sin(radians(fires[i].angle_to(target) )) * -3
            if fires[i].collidelistA(steps) != -1:
                step_index = fires[i].collidelistA(steps)
                if steps[step_index].z - fires[i].z <= 1:
                    fires[i].z = steps[step_index].z
                else:
                    fires[i].pos = lastpos
            else:
                fires[i].z = 0
        if fires[i].tipe == "faster":
            fires[i].pos[0] -= cos(radians(fires[i].angle_to(target))) * -4.5
            fires[i].pos[1] += sin(radians(fires[i].angle_to(target))) * -4.5
            if fires[i].collidelistA(steps) != -1:
                step_index = fires[i].collidelistA(steps)
                if steps[step_index].z - fires[i].z <= 1:
                    fires[i].z = steps[step_index].z
                else:
                    fires[i].pos = lastpos
            else:
                fires[i].z = 0
        elif fires[i].tipe == "flying":
            fires[i].pos[0] -= cos(radians(fires[i].angle_to(target))) * -3
            fires[i].pos[1] += sin(radians(fires[i].angle_to(target))) * -3
            fires[i].timer += 10 / 60
            fires[i].angle = sin(fires[i].timer) * 45
def playerlogic():
    global collision_occurred
    keys = pygame.key.get_pressed()
    player.lastpos = player.pos.copy()
    if keys[pygame.K_a]:
        player.pos[0] -= player_speed
        player.angle = 180
    if keys[pygame.K_d]:
        player.pos[0] += player_speed 
        player.angle = 0
    if keys[pygame.K_w]:
        player.pos[1] -= player_speed
        player.angle = 90
    if keys[pygame.K_s]:
        player.pos[1] += player_speed
        player.angle = 270
    if player.collidelistA(steps) != -1:
        step_index = player.collidelistA(steps)
        if steps[step_index].z - player.z <= 1:
            player.z = steps[step_index].z
        else:
            player.pos = player.lastpos
    else:
        player.z = 0

def player2logic():
    global collision_occurred
    if abs(round(joystick.get_axis(0), 1)) > 0.1:
        joysticksensor[1].pos[0] = round(joystick.get_axis(0), 1) * 100
    else:
        joysticksensor[1].pos[0] = 0
    if abs(round(joystick.get_axis(1), 1)) > 0.1:
        joysticksensor[1].pos[1] = round(joystick.get_axis(1), 1) * 100
    else:
        joysticksensor[1].pos[1] = 0
    player2.pos[0] += (joysticksensor[1].pos[0] / 100) * player_speed
    player2.pos[1] += (joysticksensor[1].pos[1] / 100) * player_speed
    if abs(round(joystick.get_axis(1), 1)) + abs(round(joystick.get_axis(0), 1)) > 0.1: 
        player2.angle = round(joysticksensor[0].angle_to(joysticksensor[1].pos) / 90) * 90

while True:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MUSIC_PLAY:
            playmaintheme()
            pygame.time.set_timer(MUSIC_PLAY, 0)  # Stop the timer after it fires
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "game" or mode == "game2":
                if event.button == 1:
                    shoot(player, gun1.returnangle() + 180)
            
    if mode == "title":
        if event.type == pygame.MOUSEBUTTONDOWN:
            if players1button.collidepoint(event.pos):
                mode = "transition"
                pygame.mixer.music.load("sounds/start.wav")
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(1)
                pygame.time.set_timer(MUSIC_PLAY, 5550) 
                mode = "game"
                pygame.mouse.set_visible(False)

            elif players2button.collidepoint(event.pos) and pygame.joystick.get_count() > 0:
                mode = "transition"
                pygame.mixer.music.load("sounds/start.wav")
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(1)
                pygame.time.set_timer(MUSIC_PLAY, 5550)  
                viewport1 = pygame.Rect(0, 0, 800, height/2)
                mode = "game2"
                pygame.mouse.set_visible(False)

            else:
                show_error()
    if mode == "game":
        playerlogic()
        firelogic()
        bulletlogic()
    elif mode == "game2":
        playerlogic()
        player2logic()
        firelogic()
        bulletlogic()

    pygame.display.flip()

    clock.tick(60)

