import os, math, random
os.environ['SDL_VIDEO_WINDOW_POS'] = "100,10"
from pgzero.actor import Actor
from time import sleep as wait
import pgzrun
music.set_volume(0.1)
mode = "game"
WIDTH = 1200
HEIGHT = 699
TITLE = "KABOOM"
life = 100
ammo = 100
rain = Actor('rain')
player = Actor("player", (400, 300))
player.z = 0
gun = Actor("gun")
gun.angle += 180
sensor = Actor("player", (400, 300))
sensor.z = 0
status = Actor("player status")
status.x = WIDTH / 2
status.bottom = 710
status.timer = 0
status.beep = 0
heightdisplay = Actor("placeholder", (900, 400))
waterdisplay = Actor('wotor', (300, 650))
waterdisplay.angle -= 90
firesleft = Actor('s1', (50, 650))
lifedisplay = Actor('life', (175, 650))
ground = []
starterpos = []
bullets = []
fires = []
coli = Actor("player", player.pos)
tipos = ['still', 'moving', 'moving', 'fly']
rounds = 1
step = Actor("step", (600, 300))
step.z = 1
lastx = step.x
lasty = step.y
lastz = step.z
ground.append(step)
lastlife = None
for i in range(25):
    randomx = lastx + random.choice([-200, 200])
    randomy = lasty + random.choice([-200, 200])
    step = Actor("step", (randomx, randomy))
    soup = step.pos
    step.z = lastz + random.choice([-1, 1])
    if step.z == 0:
        step.z += 2
    lastx = step.x
    lasty = step.y
    lastz = step.z    
    ground.append(step)
for actor in ground:
    actor.start = actor.pos
def addfire(times):
    for i in range(times):
        fire = Actor("s1", (random.randint(-1000, 1000), random.randint(-1000, 1000)))
        fire.life = 2
        fire.tipo = random.choice(tipos)
        if fire.collidelist(ground) != -1:
            fire.z = ground[fire.collidelist(ground)].z
        else:
            fire.z = 0 
        if fire.tipo != 'still':
            fire.timer = random.randint(0, 100)
        else:
            fire.timer = 0
        fire.semiangle = 0
        fires.append(fire)
def addwatir():
    for i in range((round(1 + rounds / 3))): 
        watir = Actor('watir', (random.randint(-100, 1300), random.randint(-100, 800)))
        watir.z = 0
        if watir.collidelist(ground) != -1:
            while watir.collidelist(ground) != -1:
                watir.pos = (random.randint(-100, 100), random.randint(-100, 100))
        watir.start = watir.pos
        ground.append(watir) 
        sounds.rain.play()
        rain.y = -1200

addfire(rounds * 2)
FPS = 60
oldvalue = None
def onvariablechange(variable):
    global oldvalue
    if variable != oldvalue:
        return True
    oldvalue = variable
def moveindirection(actor, angle, amount):
        actor.x -= math.cos(math.radians(angle + 0)) * amount
        actor.y += math.sin(math.radians(angle + 0)) * amount
def draw():
    global WIDTH
    screen.fill("#858585") #game
    if mode == "game":
        for i in range(len(ground)):
            ground[i].draw()
        for i in range(len(bullets)):
            bullets[i].draw()
        for i in range(len(fires)):
            fires[i].draw()
            screen.draw.text(str(fires[i].z), center=(fires[i].pos), color='orange')
        gun.draw()
        player.draw()
        rain.draw()
        screen.draw.filled_rect(Rect(800, 0, 600, 600), "#858585")
        screen.draw.filled_rect(Rect(800, 0, 10, 600), "black") #height
        screen.draw.filled_rect(Rect(810, (500 - (player.z * 50)), 200, (100 + (player.z * 50))), "white")
        screen.draw.text("HEIGHT:" + str(player.z), fontsize=40, center=(900, 550), color="black")
        heightdisplay.draw()
        heightdisplay.y = 400 - (player.z * 50)
        screen.draw.filled_rect(Rect(1010, (500 - (sensor.z * 50)), 200, (100 + (sensor.z * 50))), "grey")
        screen.draw.text("HEIGHT:" + str(sensor.z), fontsize=40, center=(1100, 550), color="black")
        screen.blit("pointer", (1010, 300 - (sensor.z * 50)))
        screen.draw.filled_rect(Rect(0, 600, 1200, 10), "black")#hud
        screen.draw.filled_rect(Rect(0, 610, 1200, 500), "#858585")
        status.draw()
        waterdisplay.draw()
        firesleft.draw()
        screen.draw.text(str(ammo), midleft=(waterdisplay.x + 50, waterdisplay.y), fontsize = 40, color='black')
        lifedisplay.draw()
        screen.draw.text(str(life), midleft=(lifedisplay.x + 50, lifedisplay.y), fontsize = 40, color='black')
        screen.draw.text(str(len(fires)), midleft=(firesleft.x + 50, firesleft.y), fontsize = 40, color='black')
    else:
        screen.draw.text("GAME OVER Apreta R para reiniciar", center=(600, 400), fontsize=50, color="red")
def shoot(tipo, sonido, offset):
    drop = Actor(tipo, gun.pos)
    sonido()
    drop.angle = gun.angle + 180
    drop.timer = 2.5
    moveindirection(drop, drop.angle, -offset)
    bullets.append(drop)
def on_key_down(key):
    global ammo
    if keyboard.SPACE and ammo >= 5:
            shoot('wotor', sounds.shooa.play, 80)
            ammo -= 5
def on_mouse_down(button, pos):
    global ammo
    if mouse.LEFT and ammo >= 5:
            shoot('wotor', sounds.shooa.play, 80)
            ammo -= 5
def playerlogic():
    gun.pos = player.pos
    global oldvalue, ammo
    if player.collidelist(ground) != -1 and ground[player.collidelist(ground)].image == 'watir':
        ground.pop(player.collidelist(ground))
        ammo += 25
        sounds.recharge.play()
    if keyboard.A:
        player.angle = 180
        coli.x = player.x - math.cos(math.radians(player.angle + 0)) * -10
        coli.y = player.y + math.sin(math.radians(player.angle + 0)) * -10
        if coli.collidelist(ground) == -1 or ground[coli.collidelist(ground)].z - player.z <= 1:
            for i in range(len(ground)):
                moveindirection(ground[i], player.angle, 5)
            for i in range(len(bullets)):
                moveindirection(bullets[i], player.angle, 5)
            for i in range(len(fires)):
                moveindirection(fires[i], player.angle, 5)
    elif keyboard.D:
        player.angle = 0
        coli.x = player.x - math.cos(math.radians(player.angle + 0)) * -10
        coli.y = player.y + math.sin(math.radians(player.angle + 0)) * -10
        if coli.collidelist(ground) == -1 or ground[coli.collidelist(ground)].z - player.z <= 1:
            for i in range(len(ground)):
                moveindirection(ground[i], player.angle, 5)
            for i in range(len(bullets)):
                moveindirection(bullets[i], player.angle, 5)
            for i in range(len(fires)):
                moveindirection(fires[i], player.angle, 5)
    if keyboard.W:
        player.angle = 90
        coli.x = player.x - math.cos(math.radians(player.angle + 0)) * -10
        coli.y = player.y + math.sin(math.radians(player.angle + 0)) * -10
        if coli.collidelist(ground) == -1 or ground[coli.collidelist(ground)].z - player.z <= 1:
            for i in range(len(ground)):
                moveindirection(ground[i], player.angle, 5)
            for i in range(len(bullets)):
                moveindirection(bullets[i], player.angle, 5)
            for i in range(len(fires)):
                moveindirection(fires[i], player.angle, 5)
    elif keyboard.S:
        player.angle = -90
        coli.x = player.x - math.cos(math.radians(player.angle + 0)) * -10
        coli.y = player.y + math.sin(math.radians(player.angle + 0)) * -10
        if coli.collidelist(ground) == -1 or ground[coli.collidelist(ground)].z - player.z <= 1:
            for i in range(len(ground)):
                moveindirection(ground[i], player.angle, 5)
            for i in range(len(bullets)):
                moveindirection(bullets[i], player.angle, 5)
            for i in range(len(fires)):
                moveindirection(fires[i], player.angle, 5)

    if player.collidelist(ground) != -1:
        if (ground[player.collidelist(ground)].z - player.z) <= 1:
            player.z = ground[player.collidelist(ground)].z
    else:
        player.z = 0

    if onvariablechange(player.z):
        sounds.footstep.play()
    oldvalue = player.z
def bulletslogic():
    for i in range(len(bullets) -1, -1, -1):
        moveindirection(bullets[i], bullets[i].angle, -10)
        bullets[i].timer -= .1
        if bullets[i].timer <= 0:
            bullets.pop(i)
lastpos = (0, 0)
def firelogic():
    global life
    global lastpos
    global rounds
    for i in range(len(fires)-1, -1, -1):
        helpme = fires[i].collidelist(ground)
        lastpos = fires[i].pos
        fires[i].image = 's' + str(round(abs(math.sin(fires[i].timer) * 2)))
        fires[i].timer += .05
        if fires[i].tipo == 'moving':
            fires[i].semiangle = math.degrees(math.atan2(-(player.y - fires[i].y), player.x - fires[i].x + 0))
            fires[i].y += math.sin(fires[i].timer) * .5
            moveindirection(fires[i], fires[i].semiangle, -2.5)
            if fires[i].collidelist(ground) == -1:
                fires[i].z = 0
            elif (ground[fires[i].collidelist(ground)].z - fires[i].z) <= 1:
                fires[i].z = ground[fires[i].collidelist(ground)].z
            elif (ground[helpme].z - fires[i].z) > 1:
                fires[i].pos = lastpos
        elif fires[i].tipo == 'fly':
            fires[i].semiangle = math.degrees(math.atan2(-(player.y - fires[i].y), player.x - fires[i].x + 0))
            fires[i].y += math.sin(fires[i].timer) * .5
            moveindirection(fires[i], fires[i].semiangle, -2.5)
            fires[i].angle = math.sin(fires[i].timer * 2) * 45
        else:
            if fires[i].timer >= 15:
                fire = Actor("s1", fires[i].pos)
                fire.life = 2
                fire.timer = random.randint(0, 100)
                fire.tipo = tipos[random.randint(1, 2)]
                fire.z = 0
                fires.append(fire)
                fires[i].timer = 0
            else:
                fires[i].timer += 1 / 60
        if fires[i].collidelist(bullets) != -1:
            bullets.pop(fires[i].collidelist(bullets))
            fires[i].life -= 1
        if fires[i].life <= 0:
            fires.pop(i)
            sounds.fireded.play()
        if len(fires) == 0:
            rounds += 1
            addfire(rounds * 2)
            sounds.check.play()
def on_mouse_move(pos):
    angle = math.degrees(math.atan2(-(pos[1] - gun.y), pos[0] - gun.x + 0))
    gun.angle = (angle + 180) % 360
    sensor.pos = pos
    if sensor.collidelist(ground) != -1:
        sensor.z = ground[sensor.collidelist(ground)].z
    else:
        sensor.z = 0
def update():
    global FPS, life, lastlife, mode, fires
    if mode == "game":
        playerlogic()
        bulletslogic()
        firelogic()
        if abs(gun.angle) == 360:
            gun.angle = 0     
        rain.y += 25
        if abs(gun.angle) == 180:
            gun.angle = 180
        sensor.pos = player.pos

        if lastlife != life:
            status.image = 'dmg'
            status.timer = 0
            sounds.dmg.play()
        lastlife = life
        if status.timer > .5:
            if life > 20:
                status.image = 'player status'
            else:
                status.image = 'lowhp'
        status.timer += 1 /60
        status.beep += 1 / 60
        if player.collidelist(fires) != -1:
            moveindirection(fires[player.collidelist(fires)], fires[player.collidelist(fires)].semiangle, 200)
            life -= 10
        if life <= 0:
            mode = 2
        if life <= 20 and status.beep >= 1:
            sounds.tone.play()
            status.beep = 0
    else:
        if keyboard.R:
            for i in range(len(ground)):
                ground[i - 1].pos = ground[i - 1].start
            fires = []
            bullets = []
            rounds = 1
            life = 100
            ammo = 100
            addfire((rounds * 2) -1)
            mode = "game"
#sounds.start.play()

def musicplay():
    music.play("game.wav")
clock.schedule_unique(musicplay, 5.7)
clock.schedule_interval(addwatir, 10)

pgzrun.go()
