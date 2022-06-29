import math
import pygame
import random

from pygame.locals import *

pygame.init()

# Tela...........................................................
screenWidith = 600  # SCREEN SIZE
screenHeight = 600  # SCREEN SIZE
screen = pygame.display.set_mode((screenWidith, screenHeight))  # SCREEN
pygame.display.set_caption("Heart")  # NAME OF SCREEN
pygame.mouse.set_visible(False)  # HIDE MOUSE
bg = pygame.image.load('Sprites/Background.png')  # BACKGROUND


# ..............................................................

# Sistema ...................................................
clock = pygame.time.Clock()
fps = 60
# ............................................................

# Fontes.....................................................
fontsize = 15  # Font Size
font = pygame.font.SysFont('Impact', fontsize)  # Font
color = (255, 255, 255)  # Color

# ...........................................................

# Game Variables.......................................................
pickups = []
monsters = []
demons = []

# Score and Wave

# WAVE HAS  A SPAWN TIME ,  A MAX OF ENIMIES , A MAX OF ENIMEIS AT THE SAME TIME , A MONSTER SPEED
score = 9  # Kills
wave = 1  # Wave
fakeScore = 0  # The Score to get Power Ups
timeWave = 30  # Time to text be on the screen
maxAlive = 10  # Max of that Wave

# Screen Shake
shake = 0  # Timer of the shake
offsett = [0, 0]  # Amount of screen shake

# Pause
pause = False
pausePower = False
clicked = False
clickedTimer = 10

powerlist = []

# Combo
combo = 0
timeCombo = 0
fontCombo = 15

run = True


# ..............................................................................

# Classes.....................................................................
class Player:
    def __init__(self, x, y):
        # Images
        self.images = []
        for frame in range(1, 5):
            img = pygame.image.load(f'Sprites/Player{frame}.png')
            self.images.append(img)
        self.image = self.images[0]
        self.animSpeed = 0
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.scalex = False

        # Stats
        self.moveSpeed = 3
        self.hp = 10

        self.mouseX = pygame.mouse.get_pos()[0]
        self.mouseY = pygame.mouse.get_pos()[1]

        # Hud

        self.hud = True
        self.imgSpeed = pygame.image.load('Sprites/speed.png')
        self.imgSpeed = pygame.transform.scale(self.imgSpeed, (25, 25))

        self.bulletSpeedImg = pygame.image.load('Sprites/shootspeed.png')
        self.bulletSpeedImg = pygame.transform.scale(self.bulletSpeedImg, (25, 25))

        # Bullets

        self.clicked = False
        self.timeClicked = 10
        self.bullets = []
        self.sychtes = []
        self.bullet = 0
        self.ammoSpeed = 10

        # Guns
        self.gun = 'ray'
        self.pistolImg = pygame.image.load('Sprites/revolver.png')
        self.pistolImg = pygame.transform.scale(self.pistolImg, (25, 25))

        self.minigunImg = pygame.image.load('Sprites/minigun.png')
        self.minigunImg = pygame.transform.scale(self.minigunImg, (25, 25))

        self.shotgunImg = pygame.image.load('Sprites/shotgun.png')
        self.shotgunImg = pygame.transform.scale(self.shotgunImg, (25, 25))

        self.rayImg = pygame.image.load('Sprites/raygunicon.png')
        self.rayImg = pygame.transform.scale(self.rayImg, (25, 25))

        # Power Ups
        self.power = 'death'

        self.active = 0

        self.freeze = 0
        self.imgFreeze = pygame.image.load('Sprites/freeze.png')
        self.imgFreeze = pygame.transform.scale(self.imgFreeze, (25, 25))

        self.megaspawn = 0
        self.imgMegaspawn = pygame.image.load('Sprites/megaspawn.png')
        self.imgMegaspawn = pygame.transform.scale(self.imgMegaspawn, (25, 25))

        self.slowtime = 0
        self.imgSlowTime = pygame.image.load('Sprites/Ampulheta.png')
        self.imgSlowTime = pygame.transform.scale(self.imgSlowTime, (25, 25))
        self.globalSpeed = 1

        self.death = 0
        self.imgDeath = pygame.image.load('Sprites/deathicon.png')
        self.imgDeath = pygame.transform.scale(self.imgDeath, (25, 25))

        self.imgOmni = pygame.image.load('Sprites/omnishot.png')
        self.imgOmni = pygame.transform.scale(self.imgOmni, (25, 25))

        self.piercing = False
        self.shield = True
        self.shieldAnim = 40

        self.Realgun = Gun(self.rect.x + 20, self.rect.y + 20)
        self.revolverSprite = pygame.image.load('Sprites/Revolver2.png')
        self.shotgunSprite = pygame.image.load('Sprites/Shotgun2.png')
        self.minigunSprite = pygame.image.load('Sprites/Minigun2.png')
        self.raySprite = pygame.image.load('Sprites/raygun.png')

    def update(self):

        # Movimentação
        self.moving()

        # Atirando
        self.shooting()

        if len(self.bullets):
            for b in self.bullets:
                b.update()
        else:
            particle1.particlesBullet.clear()

        # Power
        self.powers()

        # Animação
        anim(self)

        # Morrendo
        if self.hp <= 0:
            restart(20, 5)

        self.image = pygame.transform.flip(self.image, self.scalex, False)
        desenhando(self)
        self.Realgun.update()
        self.hudshow()

    def moving(self):
        if pygame.key.get_pressed()[K_w]:
            if self.rect.y > 0 + self.moveSpeed:
                self.rect.y -= self.moveSpeed

        if pygame.key.get_pressed()[K_a]:
            if self.rect.x > 0 + self.moveSpeed:
                self.rect.x -= self.moveSpeed

        if pygame.key.get_pressed()[K_s]:
            if self.rect.y < screenHeight - self.rect.height:
                self.rect.y += self.moveSpeed

        if pygame.key.get_pressed()[K_d]:
            if self.rect.x < screenWidith - self.rect.width:
                self.rect.x += self.moveSpeed

        if pygame.mouse.get_pos()[0] < self.rect.x:
            self.scalex = True
        else:
            self.scalex = False

        # Particles Walking
        particle1.emit()

        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_d] or \
                pygame.key.get_pressed()[K_s]:
            particle1.add_particles(self.rect.x, self.rect.y + 25, (248, 0, 0))  # Adiciona uma nova particula

    def shooting(self):
        self.mouseX = pygame.mouse.get_pos()[0]
        self.mouseY = pygame.mouse.get_pos()[1]

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            global shake, offsett
            shake = 5
            offsett = [random.randint(-10, 10), random.randint(-10, 10)]


            if player.gun == 'pistol':
                self.hp -= 1
                self.bullet = PlayerProjetctiles(self.Realgun.rect.x + 2, self.Realgun.rect.y, self.mouseX, self.mouseY,
                                                 self.Realgun.angle)
                self.bullets.append(self.bullet)
                self.clicked = True

            elif player.gun == 'shotgun':
                self.hp -= 1
                for x in (-0.2, 0, 0.2):
                    self.bullet = PlayerProjetctiles(self.Realgun.rect.x + 15, self.Realgun.rect.y + 15, self.mouseX,
                                                     self.mouseY,
                                                     self.Realgun.angle + x)
                    self.bullets.append(self.bullet)
                    self.clicked = True

            elif player.gun == 'minigun':
                self.hp -= 1
                self.bullet = PlayerProjetctiles(self.Realgun.rect.x , self.Realgun.rect.y , self.mouseX,
                                                 self.mouseY,
                                                 self.Realgun.angle)
                self.bullets.append(self.bullet)
                self.clicked = True

            elif player.gun == 'ray':
                self.hp -= 2
                self.bullet = PlayerLaser(self.Realgun.rect.x,self.Realgun.rect.y,self.mouseX,self.mouseY)
                self.bullets.append(self.bullet)
                self.timeClicked = 50
                shake = 5
                offsett = [random.randint(-15, 15), random.randint(-15, 15)]
                self.clicked = True

        if self.gun == 'shotgun' or self.gun == 'pistol':
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
        else:
            if self.clicked:
                self.timeClicked -= 1
                if self.timeClicked == 0:
                    self.timeClicked = 10
                    self.clicked = False

    def powers(self):
        if pygame.key.get_pressed()[K_SPACE] and self.power == 'freeze' and self.freeze == 0 and self.active == 0:
            self.freeze = 80
            self.active = 300

        if self.freeze > 0:
            self.freeze -= 1

        if pygame.key.get_pressed()[K_SPACE] and self.power == 'slowtime' and self.slowtime == 0 and self.active == 0:
            self.slowtime = 80
            self.active = 300

        if self.slowtime > 0:
            self.slowtime -= 1

        if pygame.key.get_pressed()[K_SPACE] and self.power == 'omni' and self.active == 0:
            self.hp -= 5
            if self.gun is not 'ray':
                for x in range (-20,0):
                    self.bullet = PlayerProjetctiles(self.Realgun.rect.x + 2, self.Realgun.rect.y, self.mouseX, self.mouseY,
                                             x)
                    self.bullets.append(self.bullet)
            else:
                for x in range(-200, 200):
                    self.bullet = PlayerLaser(self.Realgun.rect.x, self.Realgun.rect.y, self.mouseX + x, self.mouseY + x)
                    self.bullets.append(self.bullet)

            self.active = 300

        if pygame.key.get_pressed()[K_SPACE] and self.power == 'megaspawn' and self.megaspawn == 0 and self.active == 0:
            self.megaspawn = 120
            self.hp = 1
            self.active = 300

        if self.megaspawn > 0:
            self.megaspawn -= 1

        if self.shield:
            if self.shieldAnim < 45:
                self.shieldAnim += 1
            else:
                self.shieldAnim = 40
            pygame.draw.circle(screen,(255,255,255),(self.rect.x + 25,self.rect.y + 30),self.shieldAnim,1)

        if pygame.key.get_pressed()[K_SPACE] and self.power == 'death' and self.death == 0 and self.active == 0:
            self.death = 80
            self.active = 300
            for x in range(0,random.randint(10,60)):
                sychte = Sychte(0,random.randint(0,screenHeight))
                self.sychtes.append(sychte)

        for sychte in self.sychtes:
            sychte.update()



        if self.death > 0:
            self.death -= 1

        if self.active > 0:
            self.active -= 1


    def hudshow(self):
        if self.power == 'freeze':
            if self.active == 0:
                self.imgFreeze.set_alpha(255)
            else:
                self.imgFreeze.set_alpha(100)

            screen.blit(self.imgFreeze, (48, 50))

        if self.power == 'omni':
            if self.active == 0:
                self.imgOmni.set_alpha(255)
            else:
                self.imgOmni.set_alpha(100)

            screen.blit(self.imgOmni, (48, 50))

        elif self.power == 'megaspawn':
            if self.active == 0:
                self.imgMegaspawn.set_alpha(255)
            else:
                self.imgMegaspawn.set_alpha(100)
            screen.blit(self.imgMegaspawn, (48, 50))

        elif self.power == 'slowtime':
            if self.active == 0:
                self.imgSlowTime.set_alpha(255)
            else:
                self.imgSlowTime.set_alpha(100)
            screen.blit(self.imgSlowTime, (48, 50))

        elif self.power == 'death':
            if self.active == 0:
                self.imgDeath.set_alpha(255)
            else:
                self.imgDeath.set_alpha(100)

            screen.blit(self.imgDeath, (48, 50))

        if self.hud:
            screen.blit(self.imgSpeed, (18, 80))
            screen.blit(self.bulletSpeedImg, (18, 110))

        if self.gun == 'pistol':
            screen.blit(self.pistolImg, (18, 50))
        elif self.gun == 'shotgun':
            screen.blit(self.shotgunImg, (18, 50))
        elif self.gun == 'minigun':
            screen.blit(self.minigunImg, (18, 50))
        elif self.gun == 'ray':
            screen.blit(self.rayImg, (18, 50))


class Gun:
    def __init__(self, x, y):
        self.image = pygame.image.load('Sprites/Revolver2.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.angle = 0
        self.mouseX = 0
        self.mouseY = 0
        self.imgCopy = self.image
        self.imgCopy2 = self.imgCopy
        self.timerMinigun = 70

    def update(self):
        if player.gun == 'pistol':
            self.image = player.revolverSprite
        elif player.gun == 'shotgun':
            self.image = player.shotgunSprite
        elif player.gun == 'ray':
            self.image = player.raySprite
        elif player.gun == 'minigun':
            self.image = player.minigunSprite
            self.timerMinigun -= 1
            if self.timerMinigun <= 0:
                if player .hp < 10:
                    player.hp += 1
                self.timerMinigun = 70

        self.rect.center = [player.rect.center[0] + 60, player.rect.center[1] + 20]
        self.angle = math.atan2(self.mouseY - self.rect.y, self.mouseX - self.rect.x)
        self.mouseX = pygame.mouse.get_pos()[0]
        self.mouseY = pygame.mouse.get_pos()[1]
        if self.mouseX < player.rect.x:
            self.imgCopy = pygame.transform.flip(self.image, False, True)
        else:
            self.imgCopy = pygame.transform.flip(self.image, False, False)
        self.imgCopy2 = pygame.transform.rotate(self.imgCopy, -math.degrees(self.angle))

        screen.blit(self.imgCopy2,
                    (self.rect.x  - int(self.imgCopy2.get_width() / 2) + offsett[0],
                     self.rect.y  - int(self.imgCopy2.get_height() / 2) + offsett[1]))


class Sychte:
    def __init__(self,x,y):
        self.image = pygame.image.load('Sprites/sychte.png')
        self.rect = self.image.get_rect()
        self.rect.center= [x,y]
        self.imageCopy = self.image
        self.rot = 4
        self.side = random.randint(0,50)

    def update(self):
        self.rect.x += 5
        if self.side < 25:
            self.rot += 30
        else:
            self.rot -= 30

        if self.rot < -360 or self.rot > 360:
            self.rot = 0
        self.imageCopy = pygame.transform.rotate(self.image,self.rot)

        if self.rect.x > screenWidith + 30 and self:

            player.sychtes.remove(self)
        screen.blit(self.imageCopy,(self.rect.x - self.imageCopy.get_width() / 2,self.rect.y - self.imageCopy.get_height() / 2))

        if len(player.sychtes):
            for m in monsters:
                global score, fakeScore, combo, timeCombo, fontCombo, wave, maxAlive, timeWave
                if self.rect.colliderect(m):
                    m.hp -= 1
                    if m.hp <= 0:
                        for x in range(0, random.randint(4, 12)):
                            particle1.add_particlesDeath(self)
                        player.sychtes.remove(self)
                        monsters.remove(m)
                        score += 1
                        combo += 1
                        if score == maxAlive:
                            wave += 1
                            maxAlive = (wave + score + 10)
                            fakeScore = maxAlive
                            timeWave = 50

                        if timeCombo >= 0:
                            timeCombo += 60
                            fontCombo = 25
                    else:
                        for x in range(0, random.randint(4, 12)):
                            particle1.add_particlesDeath(self)
                        player.sychtes.remove(self)


class PlayerProjetctiles:
    def __init__(self, x, y, mouseX, mouseY, angle):
        self.image = pygame.image.load('Sprites/BloodShot.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.x = x
        self.y = y
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = player.ammoSpeed
        self.xVel = math.cos(angle) * self.speed
        self.yVel = math.sin(angle) * self.speed
        if player.gun == 'pistol':
            self.lifeTime = 60
        elif player.gun == 'shotgun':
            self.lifeTime = 30
        elif player.gun == 'minigun':
            self.lifeTime = 40
        self.imgCopy = self.image
        self.angle = angle
        self.timer = 5

    def update(self):
        self.imgCopy = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect.x += int(self.xVel)
        self.rect.y += int(self.yVel)

        if player.gun == 'shotgun':
            self.timer -= 1
            if self.timer == 0:
                particle1.add_particlesBullet(self, (255, 255, 255))  # Adiciona uma nova particula
                self.timer = 5

        elif player.gun == 'pistol':
            particle1.add_particlesBullet(self, (255, 255, 255))  # Adiciona uma nova particula

        elif player.gun == 'minigun':
            self.timer -= 1
            if self.timer == 0:
                particle1.add_particlesBullet(self, (255, 255, 255))  # Adiciona uma nova particula
                self.timer = 2

        self.lifeTime -= 1

        if self.lifeTime < 0:
            player.bullets.remove(self)

        # Colisao
        if len(player.bullets):
            for m in monsters:
                global score, fakeScore, combo, timeCombo, fontCombo, wave, maxAlive, timeWave
                if self.rect.colliderect(m):
                    m.hp -= 1
                    if m.hp <= 0:
                        for x in range(0, random.randint(4, 12)):
                            particle1.add_particlesDeath(self)
                        if not player.piercing and len(player.bullets) and self:
                            player.bullets.remove(self)
                        monsters.remove(m)
                        score += 1
                        combo += 1
                        if score == maxAlive:
                            wave += 1
                            maxAlive = (wave + score + 10)
                            fakeScore = maxAlive
                            timeWave = 50

                        if timeCombo >= 0:
                            timeCombo += 60
                            fontCombo = 25
                    else:
                        for x in range(0, random.randint(4, 12)):
                            particle1.add_particlesDeath(self)
                        player.bullets.remove(self)

        particle1.emitBullet()

        screen.blit(self.imgCopy, (self.rect.x  + offsett[0], self.rect.y  + offsett[1]))


class PlayerLaser:
    def __init__(self, x, y, mouseX, mouseY):
        self.x = x
        self.y = y
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.lifeTime = 60
        self.line = 0
        self.lenght = 20
    def update(self):
        self.lifeTime -= 1

        if self.lifeTime < 0:
            player.bullets.remove(self)
        else:
            self.line = pygame.draw.line(screen, (255, 255, 255), (self.x , self.y ), (self.mouseX , self.mouseY ), self.lenght)
            self.lenght -= 1


        # Colisao
        if len(player.bullets):
            for m in monsters:
                global score, fakeScore, combo, timeCombo, fontCombo, wave, maxAlive, timeWave
                if m.rect.colliderect(self.line):
                    m.hp -= 1
                    if m.hp <= 0:
                        monsters.remove(m)
                        score += 1
                        combo += 1
                        if score == maxAlive:
                            wave += 1
                            maxAlive = (wave + score + 10)
                            fakeScore = maxAlive
                            timeWave = 50

                        if timeCombo >= 0:
                            timeCombo += 60
                            fontCombo = 25
                    else:
                        player.bullets.remove(self)


class Spawner():
    def __init__(self):
        self.pickupTimer = 100
        self.monsterTimer = 100
        self.spawnAmount = 0
        pickup = PickUp(-100, 0)
        pickups.append(pickup)

    def monster(self, x, y):
        global monsters, demons
        self.mobs = [Monster(x, y), Demon(x, y)]
        if wave <= 2:
            mob = Monster(x, y)
            monsters.append(mob)
        elif wave > 2:
            mobrate = random.randint(0, 10)
            if mobrate < 8:
                mob = self.mobs[0]
                monsters.append(mob)
            elif mobrate >= 8:
                mob = self.mobs[1]
                demons.append(mob)
                monsters.append(mob)

    def update(self):
        self.pickupTimer -= 1
        self.monsterTimer -= 1
        if self.pickupTimer <= 0:
            pickup = PickUp(random.randint(100, screenWidith - 100), random.randint(0, screenHeight - 100))
            pickups.append(pickup)
            if player.megaspawn <= 0:
                self.pickupTimer = (90 - wave)
            else:
                self.pickupTimer = 2
            pickups[0].killTime += self.pickupTimer

        if self.monsterTimer == 1:
            self.spawnAmount = random.randint(1, 2)
        if self.monsterTimer <= 0:
            for x in range(self.spawnAmount):
                spot = random.randint(0, 2)
                if spot < 1:
                    self.monster(random.choice((-50, screenWidith + 50)), random.randint(0, screenHeight - 100))
                else:
                    self.monster(random.randint(0, screenWidith), random.choice((-50, screenHeight + 50)))

            if score <= 50:
                self.monsterTimer = 120 - (score + wave) / 2
            else:
                self.monsterTimer = 60


class PickUp():
    def __init__(self, x, y):
        self.image = pygame.image.load('Sprites/BloodPickup.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.killTime = 1000

    def update(self):
        self.killTime -= 1
        if self.killTime <= 0:
            pickups.remove(self)

        # Colisao
        if self.rect.colliderect(player.rect):
            pickups.remove(self)
            player.hp += 1

        # Desenhando
        desenhando(self)


class Cursor():
    def __init__(self):
        self.image = pygame.image.load('Sprites/Cursor.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.imagecopy = self.image
        self.rot = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.rot -= 4
        if self.rot < -360:
            self.rot = 0
        self.imagecopy = pygame.transform.rotate(self.image, self.rot)
        self.rect.x = pygame.mouse.get_pos()[0] - int(self.imagecopy.get_width() / 2)
        self.rect.y = pygame.mouse.get_pos()[1] - int(self.imagecopy.get_height() / 2)
        screen.blit(self.imagecopy, (self.rect.x, self.rect.y))



class ParticlePrinciple:
    def __init__(self):
        self.particles = []  # Lista com as particulas na tela
        self.particlesSkull = []  # Lista com as particulas na tela
        self.particlesBullet = []  # Lista com as particulas na tela
        self.deathParticles = []
        self.radius = 2

    def add_particles(self, x, y, color):
        pos_x = x + 15
        pos_Y = y + 20
        radius = random.randint(2, 5)  # Raio
        direction = -1  # Direção
        paricle_circle = [[pos_x, pos_Y], radius, direction, color]  # Lista com todas as info anteiroroes
        self.particles.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada

    def add_particlesSkull(self, x, y, color, r):
        pos_x = x + 15
        pos_Y = y + 20
        radius = r  # Raio
        direction = -1  # Direção
        paricle_circle = [[pos_x, pos_Y], radius, direction, color]  # Lista com todas as info anteiroroes
        self.particlesSkull.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada

    def emit(self):
        if self.particles:  # Se ja tiver particulas
            for particle in self.particles:  # Para cada particula dentro da lista
                particle[0][1] += particle[2]  # Direção
                if particle[1] > 0:  # Diminuindo o raio
                    particle[1] -= 0.1
                else:
                    self.particles.remove(particle)  # Tirando aquela particula
                pygame.draw.circle(screen, particle[3], particle[0],
                                   int(particle[1]))  # DESENHA NA TELA,COR,POS,INT(RAIO)

        if self.particlesSkull:  # Se ja tiver particulas
            for particle in self.particlesSkull:  # Para cada particula dentro da lista
                particle[0][1] += particle[2]  # Direção
                if particle[1] > 0:  # Diminuindo o raio
                    particle[1] -= 0.1
                else:
                    self.particlesSkull.remove(particle)  # Tirando aquela particula
                pygame.draw.circle(screen, particle[3], particle[0],
                                   int(particle[1]))  # DESENHA NA TELA,COR,POS,INT(RAIO)

    def add_particlesBullet(self, father, color):
        radius = random.randint(5, 6)  # Raio
        direction = 0  # Direção
        paricle_circle = [[father.rect.x + 12, father.rect.y + 20], radius, direction,
                          color]  # Lista com todas as info anteiroroes
        self.particlesBullet.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada

    def emitBullet(self):
        if self.particlesBullet:  # Se ja tiver particulas
            for particle in self.particlesBullet:  # Para cada particula dentro da lista
                if particle[1] <= 0:
                    self.particlesBullet.remove(particle)  # Tirando aquela particula
                else:  # Diminuindo o raio
                    particle[1] -= 0.1
                pygame.draw.circle(screen, particle[3], particle[0],
                                   int(particle[1]))  # DESENHA NA TELA,COR,POS,INT(RAIO)

    def add_particlesDeath(self,father):
        radius = random.randint(30, 40)  # Raio
        direction = 0  # Direção
        down = random.randint(1, 4)
        paricle_circle = [[father.rect.x + 10 + random.randint(-20, 20) , father.rect.y + 8 + random.randint(-20, 20)], radius,
                            direction, down]  # Lista com todas as info anteiroroes
        self.deathParticles.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada

    def emitDeath(self):
        if self.deathParticles:  # Se ja tiver particulas
            for particle in self.deathParticles:  # Para cada particula dentro da lista
                if particle[1] > 0:  # Diminuindo o raio
                    particle[1] -= particle[3]
                else:
                    self.deathParticles.remove(particle)  # Tirando aquela particula
                pygame.draw.circle(screen, (255, 255, 255), particle[0], int(particle[1]),
                                   0)  # DESENHA NA TELA,COR,POS,INT(RAIO)


class Monster():
    def __init__(self, x, y):
        self.images = []
        for frame in range(1, 5):
            img = pygame.image.load(f'Sprites/Skull{frame}.png')
            self.images.append(img)
        self.image = self.images[0]
        self.index = 0
        self.animSpeed = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 3 + (wave / 2) - 2
        if self.speed > 10:
            self.speed = 10
        self.hp = 1

    def update(self):
        # Move
        if player.freeze <= 0:
            self.playerX = player.rect.x
            self.playerY = player.rect.y
            self.dir = math.atan2(self.playerY - self.rect.y, self.playerX - self.rect.x)
            if player.slowtime <= 0:
                self.speed = 3 + (wave / 2) - 2

            elif self.speed >= 0.8:
                self.speed -= 0.2

            self.velX = math.cos(self.dir) * self.speed
            self.velY = math.sin(self.dir) * self.speed
            self.rect.x += self.velX
            self.rect.y += self.velY
            particle1.add_particlesSkull(self.rect.x + 5, self.rect.y + 10, (255, 255, 255), random.randint(2, 5))


        # Animação
        anim(self)

        # Desenhando
        if self.rect.x > player.rect.x:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)

        desenhando(self)

        # Colisao
        if self.rect.colliderect(player.rect):
            monsters.remove(self)
            if not player.shield:
                player.hp -= 1
            else:
                player.shield = False


class Demon():
    def __init__(self, x, y):
        self.images = []
        self.attackImage = pygame.image.load('Sprites/demonAttack.png')
        for frame in range(1, 7):
            img = pygame.image.load(f'Sprites/demon{frame}.png')
            self.images.append(img)
        self.image = self.images[0]
        self.index = 0
        self.animSpeed = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 2
        self.attackTime = 90
        self.bullets = []
        self.bullet = 0
        self.hp = 2

    def update(self):
        # Move
        if player.freeze <= 0 and self.attackTime > 0:

            self.playerX = player.rect.x
            self.playerY = player.rect.y
            self.dir = math.atan2(self.playerY - self.rect.y, self.playerX - self.rect.x)
            if player.slowtime <= 0:
                self.speed = 2

            elif self.speed >= 0.2:
                self.speed -= 0.2
            self.velX = math.cos(self.dir) * self.speed
            self.velY = math.sin(self.dir) * self.speed

            self.rect.x += int(self.velX)
            self.rect.y += int(self.velY)
            particle2.add_particlesSkull(self.rect.x + 15, self.rect.y + 30, (255, 0, 0), random.randint(5, 8))
        # ATTACK
        if player.freeze <= 0:
            self.attack()

        if player.slowtime > 0:
            self.speed = player.globalSpeed

        # Animação
        if self.attackTime > 0:
            anim(self)

        # Desenhando
        if self.rect.x > player.rect.x:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)

        desenhando(self)

        # Colisao
        if self.rect.colliderect(player.rect):
            monsters.remove(self)
            player.hp -= 1

        if self.bullets:
            for bullet in self.bullets:
                bullet.update()
        else:
            self.bullets.clear()

    def attack(self):
        self.attackTime -= 1
        if self.attackTime <= 0:
            self.image = self.attackImage

        if self.attackTime == -10:
            if self.rect.x > player.rect.x:
                self.bullet = MobProjectile(self.rect.x - 5, self.rect.y + 5,
                                            math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x), self)
                self.bullets.append(self.bullet)
            else:
                self.bullet = MobProjectile(self.rect.x + 18, self.rect.y + 15,
                                            math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x), self)
                self.bullets.append(self.bullet)

        if self.attackTime == -30:
            self.attackTime = (random.randint(50, 60)) - (wave + 10)
            if self.attackTime < 20:
                self.attackTime = 20


class MobProjectile:
    def __init__(self, x, y, angle, father):
        self.image = pygame.image.load('Sprites/BloodShot.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.x = x
        self.y = y
        self.playerX = player.rect.x + 5
        self.mouseY = player.rect.y + 5
        self.speed = 7
        self.angle = angle
        self.xVel = math.cos(self.angle) * self.speed
        self.yVel = math.sin(self.angle) * self.speed
        self.lifeTime = 140
        self.imgCopy = self.image
        self.angle = angle
        self.timer = 5
        self.father = father

    def update(self):
        self.imgCopy = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        if player.slowtime <= 0:
            self.speed = 7

        elif self.speed >= 0.2:
            self.speed -= 0.2
        self.xVel = math.cos(self.angle) * self.speed
        self.yVel = math.sin(self.angle) * self.speed
        self.rect.x += int(self.xVel)
        self.rect.y += int(self.yVel)
        particle2.add_particlesBullet(self, (255, 0, 0))  # Adiciona uma nova particula
        particle2.emitBullet()

        self.timer -= 1
        if self.timer == 0:
            self.timer = 5

            # Colisaows
            if self.rect.colliderect(player) and len(self.father.bullets):
                if player.shield:
                    player.shield = False
                    self.father.bullets.remove(self)
                else:
                    self.father.bullets.remove(self)
                    player.hp -= 1

        screen.blit(self.imgCopy, (self.rect.x  + offsett[0], self.rect.y + offsett[1]))


class PowerUp():
    def __init__(self, x, y):
        self.powers = random.choice(('Sprites/omnishot.png', 'Sprites/minigun.png', 'Sprites/shotgun.png',
                                     'Sprites/freeze.png', 'Sprites/piercing.png','Sprites/shield.png', 'Sprites/speed.png',
                                     'Sprites/shootspeed.png', 'Sprites/10.png', 'Sprites/megaspawn.png','Sprites/Ampulheta.png','Sprites/raygunicon.png','Sprites/deathicon.png'))
        self.image = pygame.image.load(self.powers)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        global pausePower
        pausePower = True

    def actualPower(self):
        if self.powers == 'Sprites/freeze.png':
            player.power = 'freeze'
        elif self.powers == 'Sprites/megaspawn.png':
            player.power = 'megaspawn'
        elif self.powers == 'Sprites/shotgun.png':
            player.gun = 'shotgun'
        elif self.powers == 'Sprites/minigun.png':
            player.gun = 'minigun'
        elif self.powers == 'Sprites/raygunicon.png':
            player.gun = 'ray'
        elif self.powers == 'Sprites/piercing.png':
            player.piercing = True
        elif self.powers == 'Sprites/shield.png':
            player.shield = True
        elif self.powers == 'Sprites/10.png':
            player.hp += 10
        elif self.powers == 'Sprites/speed.png':
            player.moveSpeed += 0.5
        elif self.powers == 'Sprites/shootspeed.png':
            player.ammoSpeed += 0.5
        elif self.powers =='Sprites/Ampulheta.png':
            player.power = 'slowtime'
        elif self.powers =='Sprites/omnishot.png':
            player.power = 'omni'
        elif self.powers =='Sprites/deathicon.png':
            player.power = 'death'

    def powerup(self):
        global pausePower, fakeScore
        screen.blit(self.image, (self.rect.x, self.rect.y))
        mouse_position = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_position):
            self.actualPower()
            pausePower = False
            fakeScore = 0
            powerlist.clear()
            player.hp += 1


# ............................................................................................

# Instances....................................................
player = Player(500, 200)

spawner = Spawner()
cursor = Cursor()
particle1 = ParticlePrinciple()  # Instancias
particle2 = ParticlePrinciple()  # Instancias


# ..............................................................

# Functions..................................................
def drawText(text, font, color, x, y):
    img = font.render(text, True, color)  # Transforming the text in a image
    screen.blit(img, (x, y))  # Drawing the Text


def anim(self):
    self.animSpeed += 1  # Incresing time of the animation
    if self.animSpeed == 10:  # Max of the speed of animation
        if self.index < len(self.images) - 1:  # If can go more one frame
            self.index += 1  # Change Farame
            self.animSpeed = 0  # Reset time of animation
        else:
            self.index = 0  # Reset to the first frame
            self.animSpeed = 0  # Reset the time of animation
    self.image = self.images[self.index]  # Making the actual frame update


def desenhando(self):
    if player.freeze > 0:
        for m in monsters:
            m.image.set_alpha(180)
    elif player.freeze <= 0:
        for m in monsters:
            m.image.set_alpha(255)

    screen.blit(self.image,
                (self.rect.x + offsett[0] , self.rect.y + offsett[1]))  # Drawing on the screen ( With the Screen Shake)


def restart(time, x):
    # Restar Everthing
    global pickups, monsters, player, spawner, cursor, particle1, score, combo, timeCombo, wave, fakeScore, timeWave, maxAlive
    pickups = []
    monsters = []
    score = 0
    player = Player(screenWidith / 2, screenHeight / 2)
    spawner = Spawner()
    cursor = Cursor()
    particle1 = ParticlePrinciple()  # Instancias
    powerlist.clear()
    combo = 0
    timeCombo = 0
    score = 0
    wave = 1
    fakeScore = 0
    timeWave = 30
    maxAlive = 10


def Combo():
    global combo, fontCombo
    if combo > 2:  # If player have two or more kills
        if fontCombo > 15:  # Changing the size of Font Size
            fontCombo -= 1  # Reducing the size of the font
        font = pygame.font.SysFont('Impact', fontCombo)  # Creating the Font
        drawText('COMBO : ' + str(combo), font, (255, 0, 0), screenWidith - 100, screenHeight / 2 - 100)  # Draw Text
        drawText('COMBO : ' + str(combo), font, (255, 255, 255), screenWidith - 100, screenHeight / 2 - 98)  # Draw Text


def waveManager():
    global timeWave, wave, monsters
    font = pygame.font.SysFont('Impact', 30)  # Font
    if timeWave > 0:
        monsters.clear()  # Remove all the monsters of the field
        player.bullets.clear()  # Remove all the bullets
        timeWave -= 1  # Reducing timer
        drawText('WAVE ' + str(wave), font, (255, 0, 0), (screenWidith / 2) - 50,  # Text
                 (screenHeight / 2) - random.choice((98, 100, 99)))
        drawText('WAVE ' + str(wave), font, (255, 255, 255), (screenWidith / 2) - 50,  # Text
                 (screenHeight / 2) - random.choice((95, 99, 97)))


def shakeScreen():
    global shake, offsett
    if shake >= 0:
        shake -= 1
        if offsett[0] >= 0:
            offsett[0] -= 1  # Shake
        if offsett[1] >= 0:
            offsett[1] -= 1  # Shake
    else:
        offsett = [0, 0]  # Reset Shake


def pauseGame():
    global clicked, pause, clickedTimer
    if pygame.key.get_pressed()[K_p] and not clicked:
        if not pause:
            clicked = True
            pause = True
        else:
            clicked = True
            pause = False

    if clicked:
        clickedTimer -= 1
    if clickedTimer == 0:
        clickedTimer = 10
        clicked = False


#FAZER VOLTAR A TELA COM BAGULHO LA A BARRINHA



# ...............................................................


while run:
    screen.blit(bg, (offsett[0],offsett[1]))  # Background
    # Updates
    if not pause and not pausePower and timeWave <= 0:
        # Player and Spawner Updates
        player.update()
        spawner.update()
        particle1.emitDeath()

        # Monster and Pick Ups updates
        if len(monsters):
            for m in monsters:
                m.update()
        if len(pickups):
            for pickup in pickups:
                pickup.update()

    # UI
    drawText("HP: " + str(player.hp), font, color, 20, 20)
    drawText("Score : " + str(score), font, color, screenWidith - 100, 20)

    if pause:
        drawText("PAUSE", font, color, screenWidith / 2 - 20, screenHeight / 2 - 20)


    # Combo Beaker
    if timeCombo > 0:
        Combo()
        timeCombo -= 1
    if timeCombo == 0:
        combo = 0
        fontCombo = 25

    # SHake
    shakeScreen()

    # WINDOW POWER UP
    if fakeScore == maxAlive and timeWave <= 0:
        powers = PowerUp(screenWidith / 2 - 120, screenHeight / 2 - 80)  # Pos
        powers2 = PowerUp(screenWidith / 2 - 40, screenHeight / 2 - 80)  # Pos
        powers3 = PowerUp(screenWidith / 2 + 40, screenHeight / 2 - 80)  # Pos

        powerlist.append(powers)
        powerlist.append(powers2)
        powerlist.append(powers3)
        fakeScore += 1

    if fakeScore == maxAlive + 1:
        powers.powerup()  # Catch a power
        powers2.powerup()  # Catch a power
        powers3.powerup()  # Catch a power

    # Pause
    pauseGame()

    # Wave Handlera
    waveManager()

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Screen and Mouse Update
    cursor.update()
    clock.tick(fps)
    pygame.display.update()


pygame.quit()
