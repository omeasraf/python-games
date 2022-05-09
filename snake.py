from enum import Enum
import random
import pygame
from collections import namedtuple

pygame.init()

Point = namedtuple("Point", "x,y")
BLOCK_SIZE = 20
SPEED = 10

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    def __init__(self, height=640, width=480) -> None:
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.reset()
        
    

    def reset(self):
        self.font = pygame.font.SysFont("Ariel", 25)
        self.direction = Direction.RIGHT
        self.food = None
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self._place_food()
        self.score = 0


    def play(self):
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if self.head.x >= 0 and self.head.x <= self.width and self.head.y >= 0 and self.head.y <= self.height:
                    if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
        
        # move
        
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # check if game over

        if self._is_collision():
            pygame.quit()
            quit()

        #     self.show_game_over()

            
        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)
    
    def _is_collision(self):
        # hits boundary
        self.is_hidden = True
        if self.head.x > self.width - BLOCK_SIZE:
            self.head = Point(-BLOCK_SIZE, self.head.y)
        elif self.head.x < 0:
            self.direction = Direction.LEFT
            self.head = Point(self.width, self.head.y)
        elif self.head.y > self.height - BLOCK_SIZE:
            self.head = Point(self.head.x, -BLOCK_SIZE)
        elif self.head.y < 0:
            self.head = Point(self.head.x, self.height)
        else:
            self.is_hidden = False

            # return True
        
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

        print(self.head, self.food)
    
    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self.score += 1
            self._place_food()
            self.clock.tick(SPEED + (self.score // 2))
    
        

    
    def update_ui(self):
        self.display.fill((0,0,0))

        for point in self.snake:
            pygame.draw.rect(self.display, (0, 205, 0), pygame.Rect(point.x, point.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(point.x + 4, point.y + 4,BLOCK_SIZE - 8,BLOCK_SIZE - 8))
        
        pygame.draw.rect(self.display, (200, 200, 0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.display.blit(text, (0,0))
        
        pygame.display.flip()




if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game.play()
    
pygame.quit()