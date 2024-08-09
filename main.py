import pygame,random   # importando o modulo, ativo em config > modulos
from pygame.locals import *

SCREEN_LARGURA = 400     # largura tela
SCREEN_ALTURA = 800     # altura tela,, 
SPEED = 10      # velocidade 10
GRAVITY = 1
GAME_SPEED = 20

GROUND_LARGURA = 2 * SCREEN_LARGURA
GROUND_ALTURA = 100

LARGURA_PIPE = 80
ALTURA_PIPE = 500

ESPACO_PIPE = 200

class Bird(pygame.sprite.Sprite): # Criando a classe passaro. (POO)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Primeira coisa a se fazer ao criar uma classe no Python.

        self.images = [pygame.image.load('redbird-upflap.png').convert_alpha(),
                       pygame.image.load('redbird-midflap.png').convert_alpha(),
                       pygame.image.load('redbird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('redbird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[1] = SCREEN_ALTURA / 2
        self.rect[0] = SCREEN_LARGURA / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        # Update height
        self.rect[1] += self.speed
        self.speed += GRAVITY
    def bump(self):
            self.rect[1] -= 5
            self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LARGURA_PIPE, ALTURA_PIPE))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_ALTURA - ysize

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (GROUND_LARGURA, GROUND_ALTURA))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_ALTURA - GROUND_ALTURA

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_canos_random(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_ALTURA - size - ESPACO_PIPE)
    return (pipe, pipe_inverted)

clock = pygame.time.Clock()

pygame.init() # Inicializa todos os modulos do pygame
screen = pygame.display.set_mode((SCREEN_LARGURA, SCREEN_ALTURA)) # Inicializa uma janela ou um uma tela para exibicao

BACKGROUND = pygame.image.load('background-day.png') # Carregando o backgroud
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_LARGURA, SCREEN_ALTURA)) # estamos escalando o background, passando a imagem e as as dimensoes.

bird_group = pygame.sprite.Group() # Realizado para melhor gerenciamento de objeto
bird = Bird() # Vamos criar um objeto
bird_group.add(bird) # Vamos add o bird no grupo

ground_group = pygame.sprite.Group()


for n in range(2):
    ground = Ground(GROUND_LARGURA * n)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for x in range(2):
    pipes = get_canos_random(SCREEN_LARGURA * x + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


while True:                 # Looping infinito para execucao do jogo
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        pygame.display.update()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))  #atualizacao de frames a cada nova alteracao.

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_LARGURA - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_canos_random(SCREEN_LARGURA * 2 )

        pipe_group.add(pipes[0],pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group.draw(screen)



    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):

        break # Gameover

    pygame.display.update()

    #This code will be update


