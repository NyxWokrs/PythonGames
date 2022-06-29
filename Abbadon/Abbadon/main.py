import pygame,random
from pygame.locals import *


#Sistema
pygame.init()
run = True
clock = pygame.time.Clock()
fps = 60


#Font
size=30
font = pygame.font.SysFont('Impact', size) # Fonte
white = (255,255,255) #Cor do Texto


#Tela

screenWidith = 600
screenHeight = 600

scroll = [0,-100]

screen = pygame.display.set_mode((screenWidith,screenHeight))
pygame.display.set_caption("Abbadon")

bg = pygame.image.load('Sprites/bg.png')




#Game
score = 0
spawner = 20

#Classes

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        """Inicializa as var do player"""
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image = pygame.image.load('Sprites/Foice.png')
        self.rect = self.image.get_rect()
        self.rect.center =[x,y]
        self.rot = 0
        self.images.append(self.image)
        self.active = False
        self.ponto = self.rect.topleft
        self.timer = 10

    def update(self):
        """Roda a cada frame"""
        self.rect = self.image.get_rect()
        #Girando A Foice
        if pygame.mouse.get_pressed()[0] == 1:
            self.active = True
            self.rot -= 60
            if self.rot <= -360:
                self.rot = 0
        elif self.rot < 0:
            self.rot += 10
            self.active = False

        self.image = pygame.transform.rotate(self.images[0], self.rot)
        #Posição da foice

        posX = pygame.mouse.get_pos()[0]
        posY = pygame.mouse.get_pos()[1] -15
        self.rect.x = posX
        self.rect.y = posY
        self.rect.topright = [posX,posY]
        self.timer -= 1

        #Criando os ponto de onde deve sair a particula
        if self.timer == 9:
            self.ponto = self.rect.midright
        if self.timer == 8:
            self.ponto = self.rect.midbottom
        if self.timer == 7:
            self.ponto = self.rect.midleft
        if self.timer == 6:
            self.ponto = self.rect.midtop
        if self.timer <= 5:
            self.timer = 10

class Inimigos(pygame.sprite.Sprite):
    def __init__(self , x, y):
        """Inicializa as var do inimigo"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Clovis.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.timer = 10
        self.move = random.choice(('Up','Down','Left','Right'))

    def update(self):
        """Roda a cada frame"""
        global score

        #Movendo
        self.timer -=1
        if self.timer <= 0:
            walkParticle.add_particles(self.move, self.rect.x+15, self.rect.y+50)

        if self.move  == 'Up':
            self.rect.y -= 2

        elif self.move == 'Down':
            self.rect.x += 2

        elif self.move == 'Left':
            self.rect.x -=2

        elif self.move == 'Right':
            self.rect.x += 2


        #Destruindo se sair da tela
        if self.rect.x < 0 or self.rect.x > screenWidith or self.rect.y < 0 or self.rect.y > screenHeight  :
            self.kill()
            score -=1

class ParticleFoice:
    def __init__(self):
        self.particles = [] # Lista com as particulas na tela

    def emit(self):
        if self.particles: # Se ja tiver particulas
            for particle in self.particles: # Para cada particula dentro da lista
                particle[0][1] += particle[2] +1   # Direção
                if particle[1] > 0: #Diminuindo o raio
                    particle[1] -= 0.7
                else:
                    self.particles.remove(particle) # Tirando aquela particula
                pygame.draw.circle(screen,(255,236,214),particle[0],int(particle[1])) #DESENHA NA TELA,COR,POS,INT(RAIO)

    def add_particles(self):
        if player.active == True:
            pos_x = player.ponto[0]
            pos_Y = player.ponto[1]
            radius = random.randint(10,15) # Raio
            direction = -5 #Direção
            paricle_circle = [[pos_x , pos_Y], radius, direction] # Lista com todas as info anteiroroes
            self.particles.append(paricle_circle) # Passa para a lista dee particulas essa recem formada
        else:
            pos_x = player.rect.x + 10
            pos_Y = player.rect.y
            radius = random.randint(5, 15)  # Raio
            direction = -3  # Direção
            paricle_circle = [[pos_x, pos_Y], radius, direction]  # Lista com todas as info anteiroroes
            self.particles.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada


class ParticleWalk:
    def __init__(self):
        self.particles = []  # Lista com as particulas na tela
        self.move = 'Left'

    def emit(self):
        if self.particles:  # Se ja tiver particulas
            for particle in self.particles:  # Para cada particula dentro da lista
                if particle[3] == 'Left':
                    particle[0][0] -= particle[2]  # Direção
                elif particle[3] == 'Right':
                    particle[0][0] += particle[2]  # Direção
                elif particle[3] == 'Up':
                    particle[0][1] -= particle[2]  # Direção
                elif particle[3] == 'Down':
                    particle[0][1] += particle[2]  # Direção


                if particle[1] > 0:  # Diminuindo o raio
                    particle[1] -= 0.1
                else:
                    self.particles.remove(particle)  # Tirando aquela particula
                pygame.draw.circle(screen, (255, 255, 255), particle[0],
                                   int(particle[1]))  # DESENHA NA TELA,COR,POS,INT(RAIO)

    def add_particles(self, move,x,y):
        self.move = move
        radius = random.randint(2, 5)  # Raio
        direction = -1  # Direção
        paricle_circle = [[x, y], radius, direction,move]  # Lista com todas as info anteiroroes
        self.particles.append(paricle_circle)  # Passa para a lista dee particulas essa recem formada
        self.emit()

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color) #Converte o texto para uma imagem
    screen.blit(img, (x, y)) # Desenha na tela o texto


player = Player(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
playerGroup = pygame.sprite.Group()

inimigoGroup = pygame.sprite.Group()

playerGroup.add(player)


particula = ParticleFoice()
walkParticle = ParticleWalk()


while run:
    clock.tick(fps)
    screen.fill((18, 35, 50))
    screen.blit(bg,(scroll[0],scroll[1]))

    draw_text(str(score), font, white, int(screenWidith / 2), 0)  # Desenhando texto na tela
    scroll[0] -= 4
    if abs(scroll[0]) > screenWidith + 600:
        scroll[0] = screenWidith + 500
    print(scroll)
    particula.add_particles()
    particula.emit()

    inimigoGroup.draw(screen)
    playerGroup.draw(screen)


    player.update()
    inimigoGroup.update()

    #Colisões
    if player.active == True:
         if pygame.sprite.groupcollide(playerGroup, inimigoGroup, False, True):
            score +=1
            size-= 10
            font = pygame.font.SysFont('Impact', size)  # Fonte
            walkParticle.particles.clear()
    if size < 30 :
        size += 1
        font = pygame.font.SysFont('Impact', size)  # Fonte

    #spawner
    spawner -= 1
    if spawner <=0:
        inimigo = Inimigos(random.randint(200,screenHeight-100), random.randint(200, screenHeight-100))
        inimigoGroup.add(inimigo)
        spawner = 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()

