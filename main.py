import pygame
import os
import imageio.v2 as imageio
import random
import string

from time import sleep
from enum import Enum


def verif_numbers(numbers):
    if (numbers%3) == 0:
        return numbers
    else: 
        print(f"log -> verif_numbers : {numbers} is not a multiple of 3 !")
        return ((numbers//3)*3)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
NUMBERS_OBJECTS = verif_numbers(180)

class Choice(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

png_files_names = ["rock.png","paper.png", "scissors.png"]

class Game_Object(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        
        self.type = type
        self.image = pygame.image.load(self.defind_type())
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        self.rect.y = random.randint(10,700)
        self.rect.x = random.randint(10,700)
        self.time_program_stop = 0
        self.velocity = 7

    def defind_type(self):

        try :
            if self.type == Choice.SCISSORS : return png_files_names[2]
            elif self.type == Choice.ROCK : return png_files_names[0]
            elif self.type == Choice.PAPER: return png_files_names[1]

        except IndexError:
            raise Exception(f"Wrong type {self.type} given")

    def collision_check(self, loose_against, win_against, its_group):

        sprite_loose_against = pygame.sprite.spritecollideany(self, loose_against)
        sprite_win_against = pygame.sprite.spritecollideany(self, win_against)

        if sprite_loose_against != None:
            str_png = self.convert_enum_str(sprite_loose_against.type)

            self.image = pygame.image.load(str_png)
            self.image = pygame.transform.scale(self.image, (20, 20))
        
        elif sprite_win_against != None:
            str_png = self.convert_enum_str(self.type)

            sprite_win_against.image = pygame.image.load(str_png)
            sprite_win_against.image = pygame.transform.scale(sprite_win_against.image, (20, 20))
            
            sprite_win_against.type = self.type
            sprite_win_against.kill()
            its_group.add(sprite_win_against)
    
    def convert_enum_str(self, enum):
        try :
            if enum == Choice.PAPER: return "paper.png"
            elif enum == Choice.ROCK: return "rock.png"
            elif enum == Choice.SCISSORS: return "scissors.png"
        except IndexError :
            raise Exception(f"convert_enum_str : sprite.type = {enum} wrong value")

    def random_move(self):
        # up = 0, down = 1, left = 2, right = 3
        border_bool = True
        while border_bool:
            result = random.randint(0, 3)

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
        try :
            if i < (NUMBERS_OBJECTS//3):
                scissors.add(Game_Object(type=Choice.SCISSORS))

            elif (NUMBERS_OBJECTS//3) <= i < ((NUMBERS_OBJECTS//3)*2):
                rocks.add(Game_Object(type=Choice.ROCK))

            elif i >= ((NUMBERS_OBJECTS//3)*2):
                papers.add(Game_Object(type=Choice.PAPER))
        except IndexError :
            raise Exception(f"game_function : var i = {i} wrong value")

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


    if dectect_winner(len(rocks), len(scissors), len(papers)):
        return False
    else : return True

def dectect_winner(len_rocks, len_scissors, len_papers):

    count_loosers = 0
    if len_rocks == 0:
        count_loosers += 1
    if len_scissors == 0:
        count_loosers += 1
    if len_papers == 0:
        count_loosers += 1

    if count_loosers == 2:
        return True
    else : return False

def game_image_save(screen, i, image_count):
    if (i%7) == 0:
        if image_count < 10:
            file_name = "image_save/image" + "000000" +str(image_count) + ".png"
        elif image_count < 100:
            file_name = "image_save/image" + "00000" +str(image_count) + ".png"
        elif image_count < 1000:
            file_name = "image_save/image" + "0000" +str(image_count) + ".png"
        elif image_count < 10000:
            file_name = "image_save/image" + "000" +str(image_count) + ".png"
        elif image_count < 100000:
            file_name = "image_save/image" + "00" +str(image_count) + ".png"
        elif image_count < 1000000:
            file_name = "image_save/image" + "0" +str(image_count) + ".png"
        else :
            file_name = "image_save/image" + str(image_count) + ".png"
        image_count += 1
        pygame.image.save(screen, file_name)
    return image_count

def create_gifs():

    files = os.listdir('image_save')
    
    image_path = [os.path.join('image_save', file) for file in files]
    images = []
    for image in image_path:
        images.append(imageio.imread(image))
    
    name = 'gifs_storage/' + name_generator() + '.gif'
    
    imageio.mimwrite(name, images, fps=15)

    for i in files:
        path = 'image_save/' + i
        os.remove(path)

    return name

def game_function():

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags = pygame.HIDDEN)
    backgournd_color = (255, 255, 255)
    image_count = 0

    group_scissors = pygame.sprite.Group()
    group_papers = pygame.sprite.Group()
    group_rocks = pygame.sprite.Group()

    create_objects(group_scissors, group_papers, group_rocks)

    running = True
    winner = 0
    i = 0

    while running :
        i += 1
        clock.tick(400)
        screen.fill(backgournd_color)

        running = game_update(screen, group_scissors, group_papers, group_rocks)
        if running == False:
            if len(group_scissors) == NUMBERS_OBJECTS:
                winner = "scissors"
            elif len(group_papers) == NUMBERS_OBJECTS:
                winner = "papers"
            elif len(group_rocks) == NUMBERS_OBJECTS:
                winner = "rocks"

        # update background
        pygame.display.flip()
        image_count = game_image_save(screen, i, image_count)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("fermeture du jeu")

    name = create_gifs()
    return winner, name

# return path/name.gif
def name_generator():
    output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    return output_string