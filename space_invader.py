from collections import namedtuple
import pygame
import random

pygame.init()

Point = namedtuple("Point", "x,y,hit")
BLOCK_SIZE = 20
SPEED = 60

class SpaceInvader:

    def __init__(self, height=640, width=480) -> None:
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")
    
        self.reset()

    
    def reset(self):
        self.clock = pygame.time.Clock()

        self.is_game_over = False
        self.font = pygame.font.SysFont("Ariel", 25)
        self.player = Point(self.width/2, self.height - BLOCK_SIZE, 0)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.least_enemy_count = 7
        self.populate_enemies()
    
    def populate_enemies(self, x_val = 0):
        x = 20
        for _ in range(10):
            self.enemies.append([
                Point(x, 0, 0),
                Point(x + 15, 0, 0),
                Point(x, 15, 0),
                Point(x + 15, 15, 0)
            ])
            x += 45
        
    def update_enemies(self):
        rand = random.randint(0, 2)
        rand = random.choice([rand, -rand])
        count = 0
        for enemy in self.enemies:
            if not self.is_game_over:
                try:
                    idx = self.enemies.index(enemy)
                    if not self.check_hit(enemy):
                        if rand + enemy[0].x > 0 and rand + enemy[0].x < self.width - rand:
                            for box in enemy:

                                if box.y >= self.player.y:
                                    self.show_game_over()

                                box_idx = enemy.index(box)
                                pt = Point(rand + box.x, box.y + 0.5, 0)
                                enemy[box_idx] = pt
                                self.enemies[idx] = enemy
                            count += 1
                    if count == 5:
                        count = 0
                        rand = random.randint(0, 2)
                        rand = random.choice([rand, -rand])
                except Exception as e:
                    print(e)
                
        
    

    def check_hit(self, enemy) -> bool:
        for bullet in self.bullets:
            for box in enemy:
                if bullet.x <= box.x + 10 and bullet.x >= box.x:
                    if bullet.y <= box.y + 10 and bullet.y >= box.y:
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.score += 1
                        return True
        
        
        
        if len(self.enemies) < self.least_enemy_count:
            self.populate_enemies()
            self.least_enemy_count += 1

        return False

    def show_game_over(self):
        self.is_game_over = True
        text_surface = self.font.render("Press space bar to play again", True, (255,255,255))
        self.display.blit(text_surface, (self.width / 2, self.height * 7 / 8))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    self.reset()
                    done = True
                    break
                else:
                    done = True
                    pygame.quit()
                    quit()

                    



    def play(self):
        self.clock.tick(SPEED)
        if not self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move("l")
                    elif event.key == pygame.K_RIGHT:
                        self.move("r")
                    elif event.key == pygame.K_SPACE:
                        self.shoot()
                    elif event.key == pygame.K_UP:
                        self.reset()
                    
            self.update_bullet()
            self.update_enemies()
            self.update_ui()
    
    def move(self, direction):
        if direction == "l":
            if self.player.x - BLOCK_SIZE >= 0:
                self.player = Point(self.player.x - BLOCK_SIZE, self.player.y, 0)
        elif direction == "r":
            if self.player.x + BLOCK_SIZE <= self.width - BLOCK_SIZE:
                self.player = Point(self.player.x + BLOCK_SIZE, self.player.y, 0)
    

    def shoot(self):
        x = self.player.x
        y = self.player.y + 10

        self.bullets.append(Point(x + (BLOCK_SIZE * 2 / 1.5), y, 0))
    
    def update_bullet(self):
        for bullet in self.bullets:
            if bullet.y <= 0:
                self.bullets.remove(bullet)
            else:
                idx = self.bullets.index(bullet)
                point = Point(bullet.x, bullet.y - 5,0)
                self.bullets[idx] = point
     


    def update_ui(self):
        self.display.fill((0,0,0))

        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(self.player.x, self.player.y,BLOCK_SIZE * 3,BLOCK_SIZE * 2))

        for bullet in self.bullets:
            pygame.draw.rect(self.display, (200, 0, 0), pygame.Rect(bullet.x, bullet.y,BLOCK_SIZE - 10,BLOCK_SIZE - 10))

        for enemy in self.enemies:
            for box in enemy:
                pygame.draw.rect(self.display, (255, 255, 0), pygame.Rect(box.x, box.y,10,10))

        
        text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.display.blit(text, (0,0))
        
        pygame.display.flip()


if __name__ == "__main__":
    game = SpaceInvader()

    while True:
        game.play()
    
pygame.quit()