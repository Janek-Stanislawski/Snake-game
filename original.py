import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOUR = (110, 110, 5)


class Apple():
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3
        
    def draw(self):
        
         #draw one image onto another
         
         self.parent_screen.blit(self.image, (self.x, self.y))
         
         #Update the full display Surface to the screen
         pygame.display.flip()
    
    def move(self):
        # Calculate the maximum number of rows and columns that can fit on the screen
        max_rows = self.parent_screen.get_height() // SIZE
        max_columns = self.parent_screen.get_width() // SIZE
        
        # Generate random positions for the apple within the valid range
        
        self.x = random.randint(0, max_columns - 1) * SIZE
        self.y = random.randint(0, max_rows - 1) * SIZE
    
  
class Snake:
    
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'
        
    def increase_lenght(self):
        self.length += 1
        #adds new value at the end of the list
        self.x.append(-1)
        self.y.append(-1)
        
    
    def draw(self):
        
        #draw one image onto another
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        
        #Update the full display Surface to the screen
        pygame.display.flip()
    
    def move_left(self):
        self.direction = 'left'
        
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
        
    def move_down(self):
        self.direction = 'down'
    
    def walk(self):
        #updates last segment with the position of the previous segment
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
            
        #checking if the postion of the head is outside of the border
        max_rows = self.parent_screen.get_height() // SIZE
        max_columns = self.parent_screen.get_width() // SIZE
        
        if self.x[0] < 0:
            self.x[0] = (max_columns - 1) * SIZE
        if self.x[0] >= self.parent_screen.get_width():
            self.x[0] = 0
        if self.y[0] < 0:
            self.y[0] = (max_rows - 1) * SIZE
        if self.y[0] >= self.parent_screen.get_height():
            self.y[0] = 0
            
        
        self.draw()
        
    
class Game:
    def __init__(self):
        pygame.init()
        #initialize soundboard
        pygame.mixer.init()
        self.play_background_music()
        #Creates the game window
        self.surface = pygame.display.set_mode((1000, 800))
        #Fills the game window with the background color (RGB: 110, 110, 5).
        self.surface.fill(BACKGROUND_COLOUR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def play_background_music(self):
        #plays music constatnly
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        #playing music and setting infinite repeat
        pygame.mixer.music.play(-1)
    
    def play_sound(self, sound):
        #plays sound as event related occurance
        sound_to_play = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound_to_play)
        
    def render_background(self):
       bg = pygame.image.load("resources/background.jpg")
       self.surface.blit(bg, (0,0))
       
    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_lenght()
            self.apple.move()
        
        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "game over"
        
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        #this is refreshing UI
        pygame.display.flip()
        pygame.mixer.music.pause()
            
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        
    
    
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))
        
        
    def run(self):
    # event loop for the UI to stay active
        run = True
        pause = False
        
        while run:
            for event in pygame.event.get():
                #Handles keyboard input
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                            
                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        
                elif event.type == QUIT:
                    run = False
           
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                
            time.sleep(0.2)
            
            
            
if __name__ == "__main__":
    #initialize all imported pygame modules
    game = Game()
    game.run()
        


            
    
            
            

