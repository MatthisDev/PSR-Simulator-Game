import pygame
from random import randint
from time import sleep

def verif_numbers(numbers):
    if (numbers%3) == 0:
        return numbers
    else: 
        print(f"log -> verif_numbers : {numbers} is not a multiple of 3 !")
        return ((numbers//3)*3)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
NUMBERS_OBJECTS = verif_numbers(600)


class Game_Object(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        
        self.type = type
        self.image = pygame.image.load(self.defind_type())
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        self.rect.y = randint(10,700)
        self.rect.x = randint(10,700)
        self.time_program_stop = 0
        self.velocity = int(3)


    def defind_type(self):
        if self.type == "scissors": return 'scissors.png'
        elif self.type == "rocks": return 'rocks.png'
        elif self.type == "papers": return 'papers.png'
        else : print("log -> def_type : TYPE ERROR")

    def collision_check(self, loose_against, win_against, its_group):

        sprite_loose_against = pygame.sprite.spritecollideany(self, loose_against)
        sprite_win_against = pygame.sprite.spritecollideany(self, win_against)

        if sprite_loose_against != None:
            str_png = str(sprite_loose_against.type) + '.png'

            self.image = pygame.image.load(str_png)
            self.image = pygame.transform.scale(self.image, (20, 20))
        
        elif sprite_win_against != None:
            str_png = str(self.type) + '.png'

            sprite_win_against.image = pygame.image.load(str_png)
            sprite_win_against.image = pygame.transform.scale(sprite_win_against.image, (20, 20))
            
            sprite_win_against.type = self.type
            sprite_win_against.kill()
            its_group.add(sprite_win_against)

    def random_move(self):
        # up = 0, down = 1, left = 2, right = 3
        border_bool = True
        while border_bool:
            result = randint(0, 3)

            if result == 0 and not self.border_check((self.rect.y - self.velocity)):
                border_bool = False
                sleep(self.time_program_stop)
                self.rect.y -= self.velocity

            elif result == 1 and not self.border_check((self.rect.y + self.velocity)):
                border_bool = False
                sleep(self.time_program_stop)
                self.rect.y += self.velocity

            elif result == 2 and not self.border_check((self.rect.x - self.velocity)):
                border_bool = False
                sleep(self.time_program_stop)
                self.rect.x -= self.velocity

            elif result == 3 and not self.border_check((self.rect.x + self.velocity)):
                border_bool = False
                sleep(self.time_program_stop)
                self.rect.x += self.velocity

    def border_check(self, coo):
        if coo <= 10 or coo >= 700: return True
        else : return False

def create_objects(scissors, papers, rocks):

    for i in range(0, NUMBERS_OBJECTS):
        if i < (NUMBERS_OBJECTS//3):
            scissors.add(Game_Object(type="scissors"))

        elif (NUMBERS_OBJECTS//3) <= i < ((NUMBERS_OBJECTS//3)*2):
            rocks.add(Game_Object(type="rocks"))

        elif i >= ((NUMBERS_OBJECTS//3)*2):
            papers.add(Game_Object(type="papers"))

        else : print("log -> game_function : ERROR init object : i : ", i)

    return scissors, papers, rocks

def game_update(screen, scissors, papers, rocks):

    for i in scissors:
        i.random_move()

        i.collision_check(loose_against= rocks, win_against= papers, its_group= scissors)
        screen.blit(i.image, i.rect)

    for i in papers:
        i.random_move()

        i.collision_check(loose_against= scissors, win_against= rocks, its_group= papers)
        screen.blit(i.image, i.rect)
    
    for i in rocks:
        i.random_move()

        i.collision_check(loose_against=papers , win_against= scissors, its_group= rocks)
        screen.blit(i.image, i.rect)

def game_function():

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((720, 720))
    backgournd_color = (255, 255, 255)

    group_scissors = pygame.sprite.Group()
    group_papers = pygame.sprite.Group()
    group_rocks = pygame.sprite.Group()

    create_objects(group_scissors, group_papers, group_rocks)

    running = True

    while running :
        clock.tick(60)
        screen.fill(backgournd_color)

        game_update(screen, group_scissors, group_papers, group_rocks)

        # update background
        pygame.display.flip()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("fermeture du jeu")

game_function()