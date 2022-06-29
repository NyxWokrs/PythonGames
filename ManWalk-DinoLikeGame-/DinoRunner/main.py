import pygame,random
from pygame.locals import *

pygame.init()

#Tela
screenWidith = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidith, screenHeight))
pygame.display.set_caption("Dino Game")

#Sistema
run = True
clock = pygame.time.Clock()
fps = 60
gameover = False


#Font
font = pygame.font.SysFont('Impact',20)
color = ((0, 0, 0))


#Game
spawnObs = random.randint(30,60)
spawnCloud = 60
score = 0
speed = 4
count = 0
#Classes
class Clouds():
    def __init__(self,x,y):
        self.image = pygame.image.load(f'Sprites/Cloud{random.randint(1,2)}.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global clouds,spawnCloud,speed
        screen.blit(self.image,(self.rect.x,self.rect.y))
        self.rect.x -= speed -2
        for x in clouds:
           if x == clouds[-1]:
               if x.rect.x < -100:
                    clouds.clear()
                    spawnCloud = 60

class Player():
    def __init__(self,x,y):
        self.images = []
        self.grav = 1
        self.pulo = False
        for frame in range(1, 5):
            img = pygame.image.load(f"Sprites/Guy{frame}.png")
            self.images.append(img)
        self.image = self.images[0]
        self.index = 0
        self.animSpeed = 3
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        #Animação
        self.animSpeed -= 1
        if self.animSpeed == 0:
            if self.index < 3:
                self.index += 1
            else:
                self.index = 0
            self.animSpeed = 5

        self.image = self.images[self.index]

        #Gravidade
        self.rect.y += self.grav

        if self.rect.y > screenHeight / 2 + 45:
            self.grav = 0
            self.pulo = False
        elif self.grav < 15:
            self.grav += 1

        #Pulando
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.pulo == False:
            self.grav = -15
            self.pulo = True

        #Colisão
        global obstacles,gameover,count,score
        if len(obstacles):
            for obs in obstacles:
                if self.rect.colliderect(obs.rect):
                    gameover = True
        #Pontos
        if len(obstacles):
            for obs in obstacles:
                if self.rect.x > obs.rect.x:
                    if obs.value ==1:
                        score+=1
                        count+=1
                        obs.value =0



        #Desenhando
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Obstacles():
    def __init__(self, x, y):
        self.image = pygame.image.load("Sprites/Obstacle1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.value = 1

    def update(self):
        global score,speed,count
        #Movendo
        self.rect.x -= speed

        #Desenhando
        screen.blit(self.image,(self.rect.x, self.rect.y))


        #Destruindo
        if self.rect.x < -10:
            del obstacles[0]

def moooooreeeee():
    global count,speed
    if count == 5:
        speed += 0.5
        count = 0

def drawText(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

def restart():
    global clouds,obstacles,player,score,spawnCloud,spawnObs,gameover,speed,count
    clouds = []
    obstacles = []
    player = Player(100, 100)
    score = 0
    spawnObs = random.randint(30, 60)
    spawnCloud = 60
    speed = 4
    count = 0
    gameover = False


clouds = []
obstacles = []



player = Player(100,100)
while run:
    #BackGround
    screen.fill((255, 255, 209))
    pygame.draw.line(screen, (0, 0, 0), (0, screenHeight / 2 + 80), (screenWidith, screenHeight / 2 + 80), 6)

    if gameover == False:
        #Score
        drawText("Score: " + str(score), font, color, int(screenWidith - 200), 0)  # Desenhando texto na tela
        moooooreeeee()

        #Updates
        player.update()

        if len(obstacles) > 0:
            for obs in obstacles:
                obs.update()

        #Spawners
        spawnCloud -= 1
        spawnObs -=1

        if spawnCloud == 0 or spawnCloud == -50 or spawnCloud == -100:
            cloud = Clouds(screenWidith, random.randint(100, screenHeight - 400))
            clouds.append(cloud)
        if spawnCloud < 0:
            for cloud in clouds:
                cloud.update()

        if spawnObs == 0:
            obstacle = Obstacles(screenWidith, screenHeight / 2 + 70)
            obstacles.append(obstacle)
            spawnObs = random.randint(40, 70)

    else:
        drawText(f"Game Over, Your Score {str(score)}",font,color,screenWidith/2 - 200,screenHeight/2)
        drawText("R to restart", font, color, screenWidith / 2 - 200, screenHeight / 2 + 20)
        if pygame.key.get_pressed()[K_r]:
            restart()



    # Manuseador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

   #Atualziando
    clock.tick(fps)
    pygame.display.update()
pygame.quit()