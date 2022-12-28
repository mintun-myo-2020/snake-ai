
import pygame, sys, time, random
from pygame.surfarray import array3d
from pygame import display

import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

# set up COLORS (constants)
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)

class SnakeEnv(gym.Env):
    
    metadata = {'render.modes':['human']}

    def __init__(self):
        
        self.action_space = spaces.Discrete(4) #UP, DOWN, LEFT, RIGHT
        self.observation_space = spaces.Box(0, 255, shape=(300, 300, 3), dtype=np.uint8)
        self.width = 300
        self.height = 300
        self.game_window = pygame.display.set_mode((self.width, self.height))
        
        # Reset game
        self.reset()
        
        # Set step limit
        self.STEP_LIMIT = 10000
        self.sleep = 0
        
    def reset(self):
        self.game_window.fill(BLACK)
        x_middle = self.width//2
        y_middle = self.height//4
        self.snake_pos = [x_middle, y_middle]
        self.snake_body = [[x_middle, y_middle], [x_middle-10, y_middle], [x_middle-20, y_middle]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        self.direction = "RIGHT"
        self.action = self.direction
        
        self.score = 0
        self.steps = 0
        
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img
        
    @staticmethod
    def change_direction(action, direction):
        if action == 0 and direction != "DOWN":
            direction = "UP"
        if action == 1 and direction != "UP":
            direction = "DOWN"
        if action == 2 and direction != "RIGHT":
            direction = "LEFT"
        if action == 3 and direction != "LEFT":
            direction = "RIGHT"

        return direction
    
    @staticmethod
    def move(direction, snake_pos):
        
        if direction == "UP":
            snake_pos[1] -= 10
        if direction == "DOWN":
            snake_pos[1] += 10
        if direction == "LEFT":
            snake_pos[0] -= 10
        if direction == "RIGHT":
            snake_pos[0] += 10
            
        return snake_pos
        
    def spawn_food(self):                
        return [random.randrange(1, (self.width // 10)) * 10, random.randrange(1, (self.height // 10)) * 10]
    
    def eat(self):
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]
    
    def step(self, action):

        scoreholder = self.score
        reward = 0
        self.direction = SnakeEnv.change_direction(action, self.direction)
        self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
        self.snake_body.insert(0, list(self.snake_pos))

        reward = self.food_handler()

        self.update_game_state() # update env after action
    
        reward, done = self.game_over(reward)

        img = self.get_image_array_from_game() # get observations

        info = {"score" : self.score}
        self.steps += 1
        time.sleep(self.sleep)

        return img, reward, done, info

    def food_handler(self):
        if self.eat():
            self.score += 1
            reward = 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward = 0

        if not self.food_spawn:
            self.food_pos = self.spawn_food()
        self.food_spawn = True

        return reward

    
    def update_game_state(self):
    # Draw Snake
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window,
                            WHITE,
                            pygame.Rect(
                                pos[0],
                                pos[1],
                                10,
                                10))
        
        # Draw FOOD
        pygame.draw.rect(self.game_window, GREEN, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

    def get_image_array_from_game(self):                
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img        


    def game_over(self, reward):
        
        # HIT WALLS
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width - 10:
            # -1 reward, game done
            return (-1, True)
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.height - 10:
            # -1 reward, game done
            return (-1, True)
        
        # HIT SELF
        for pixel in self.snake_body[1:]:
            if self.snake_pos[0] == pixel[0] and self.snake_pos[1] == pixel[1]:
                # -1 reward, game done
                return (-1, True)

        if self.steps >= self.STEP_LIMIT:
            return (0, True)

        return (reward, False)

    def render(self, mode="human"):
        if mode == "human":
            display.update()
    
    def close(self):
        pass